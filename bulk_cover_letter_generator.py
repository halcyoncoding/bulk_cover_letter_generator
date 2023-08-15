import os
import time

import pandas as pd
from langchain import PromptTemplate, LLMChain
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import SimpleMemory

from apikey import OPENAI_API_KEY
from resumes import analytics_resume, operations_resume, pm_resume, skills #create a .py file containing string variables for each resume you plan on using. Additionally, include all of your skills in a variable. 

#setup
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


def generate_cover_letter_text(resume, company, job_title, job_description):

    #prompt templates
    #these will take your dataframe inputs and insert them directly into the prompts
    resume_condense_template = PromptTemplate(
        input_variables = ['resume', 'job_title', 'job_description'], 
        template = 'You are an expert career advisor with over 20 years of experience. Your job is to make your client sound as qualified as possible. You will list bullet points from the resume that are relevant to the job description.\n\nRESUME: {resume}\n\nJOB TITLE: {job_title}\n\nJOB DESCRIPTION: {job_description}'
    )

    cover_letter_generation_template = PromptTemplate(
        input_variables = ['condensed_resume', 'job_title', 'job_description', 'company', 'skills'], 
        template = """You are an expert career advisor with over 20 years of experience, writing a cover letter for your client.  Your job is to make them sound as qualified as possible. You can slightly stretch the truth or exaggerate, but you cannot write anything completely made up. 
    Your goals:
    -Personalize the cover letter to best fit what the job description requires
    -Write persuasively in a way that showcases how your client would be successful at this job
    -Provide good structure and narrative flow, grouping together similar thoughts into paragraphs
    -FOCUS ON THE SKILLS AND EXPERIENCE OF THE CLIENT, fitting it to meet the job description
    -highlight the skills of the client that meet the job description
    -reframe the client's experience in a way that makes it applicable to the job description
    -Write action oriented sentences (example: instead of "As an individual comfortable with x, I possess a strong skill set  in y and z", write "I possess a strong skill set in y and z"
    -do not directly quote more than a few words at a time from the cover letter
    -keep the cover letter less than one page long

    CANDIDATE EXPERIENCE: SKILLS {skills}\n\nRESUME {condensed_resume}

    COMPANY: {company}
    JOB TITLE: {job_title}
    JOB DESCRIPTION: {job_description}"""
    )

    #create llm. Using gpt-4 at middling temperature produces highest success
    llm = ChatOpenAI(temperature=.4,model_name='gpt-4')
    
    verbose = False #change to true if needed for troubleshooting
    
    #simple chains
    resume_condense_chain = LLMChain(llm=llm, prompt=resume_condense_template, output_key='condensed_resume', verbose=verbose)
    cover_letter_generation_chain = LLMChain(llm=llm, prompt=cover_letter_generation_template, output_key='cover_letter', verbose=verbose)
    
    #combine simple chains
    overall_chain = SequentialChain(
        memory = SimpleMemory(memories={'company': company, 'skills': skills}), #input_variables used in chains past the first
        chains=[resume_condense_chain, cover_letter_generation_chain], #list of chains in order
        input_variables=['resume', 'job_title', 'job_description'], #inputs to the first chain
        output_variables=['cover_letter'], #output from the last chain (output_key)
        verbose=verbose
    )

    #returns dictionary
    response = overall_chain({'job_title': job_title, 'job_description': job_description, 'resume': resume})

    #get only activities from dictionary
    return (response['cover_letter'].strip())

def get_cover_letters(dataframe, resumes_dict, skills):
    for index, row in dataframe.iterrows():
        resume_name = row['resume']
        resume = resumes_dict.get(resume_name, resume_name)
        company = row['company']
        job_title = row['job_title']
        job_description = row['job_description']
        cover_letter = row['cover_letter']
        
        # Set up visual process output
        index_text = str(index) + ' ' * (5 - len(str(index)))
        job_text = company+' '+job_title
        job_text = str(job_text) + (' ' * (50 - len(str(job_text))))
        print(f"Processing row {index_text} {job_text}({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())})")
        
        # Skip row if data has already been scraped
        if not (pd.isna(row['cover_letter']) or row['cover_letter'] == ''):
            print(f"Skipping row {index} as there is already a value in the specified location.")
            continue

        try:
            cover_letter_text = generate_cover_letter_text(resume, company, job_title, job_description)
            dataframe.at[index, 'cover_letter'] = cover_letter_text             

            dataframe.to_pickle('cover_letters.pkl')
            
        #if an error is encountered, this row will be skipped. Combined with the previous block, a dataframe can be run multiple times without incurring significant additional cost to correct for errors
        except Exception as e:
            print(f"Error for row {index_text} {job_text}({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}): {e}")
            continue

    complete_dt = f"{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}"
    
    dataframe.to_csv(f"cover_letters_processed_{complete_dt}.csv")
    
    
    
#set up and run    

#you will need to create a dictionary to match your resumes to the string provided from the .csv import
resumes_dict = {
    'analytics_resume': analytics_resume,
    'operations_resume': operations_resume,
    'pm_resume': pm_resume,
}

df_cl_raw_import = pd.read_csv('cover_letter_automation_example.csv') #replace this with your .csv, containing the following columns: 'job_title', 'company', 'job_description', 'link', 'resume', 'cover_letter'. 'cover_letter' should be an empty field. 

get_cover_letters(df_cl_raw_import,resumes_dict,skills)