# bulk_cover_letter_generator
Bulk generate highly personalized cover letters using LangChain and GPT-4

# OVERVIEW

Following the public release of ChatGPT, and especially GPT-4, significant discussion has been had about cover letters. It is, at least in my circles, basically expected that you will use ChatGPT to write your cover letter, then edit it, all under human oversight via the GUI with final edits done by a human. Any number of "solutions" have popped up which are often low quality, restricted in number, and quite expensive. Before the release of ChatGPT publically, I was using one of these solutions myself, based on, I believe, OpenAI's text-davinci-002 model. It took the process from 30 minutes for a good cover letter to 15, but as you can imagine, the quality was not great.


On the release of GPT-4 API, I sat down to create a quicker, better process that could write cover letters in volumes without all the tedious hand-holding required with the typical GUI tools. 


A good friend of mine, close to the space pointed out "They haven't been reading the cover letters. And now the social contract has shifted. They use robots to read the cover letters, so we use robots to write them."

# GOAL

The goal of this project is to democratize those robots, to provide at cost commensurate to your use (i.e., API costs) in a highly customizable format (if you use this, please change the prompting to meet exactly your needs. For example, in the resume writing prompt: "You are an expert career advisor with over 20 years of experience, writing a cover letter for your client.", for my own use, I change to "You are an expert career advisor with 15 years of experience, and you were previously a technical recruiter for Google, writing a cover letter for your client.").

# FEATURES

–Expert Career Advice: The tool uses prompts that make the GPT-4 model act as an expert career advisor and writing coach.

–Sequential Processing: Combines a series of prompt templates and processing chains to first condense the resume and then generate the cover letter, providing a tight, focused cover letter 

–Error Handling: If an error occurs during the cover letter generation for a specific row, the row is skipped, allowing the remaining rows to be processed. Each row overwrites a .pkl file you can use or re-run from if needed. Fire and forget for hundreds of cover letters at a time.

–Output Saving: Cover letters are saved in .csv format with timestamps for easy reference.

# GETTING STARTED

Prerequisites
Ensure that you have the following libraries installed:

    pandas
    langchain
    openai

You should also have an OpenAI API key to access the GPT-4 model. (https://platform.openai.com/account/api-keys)

Setup

–Create a .py file containing string variables for each resume you plan on using. Additionally, include all of your skills in a variable. Example file: resumes.py.

–Map your resumes in a dictionary. It is suggested you use the same names in your CSV and resumes.py file. Example: 

    resumes_dict = {
        'analytics_resume': analytics_resume,
        'operations_resume': operations_resume,
        'pm_resume': pm_resume,
        'product_resume': product_resume
    }

–Replace the file path 'cover_letter_automation_example.csv' with your CSV file. This CSV should contain columns: 'job_title', 'company', 'job_description', 'link', 'resume', 'cover_letter'. The 'cover_letter' field should be empty initially.

–Run the script.

# HOW IT WORKS

The tool takes the following steps to generate a cover letter:

–Reading the CSV: The CSV file containing job details is read into a pandas dataframe.

–Mapping Resumes: The script checks for the resume type associated with each job application from a predefined dictionary.

–Cover Letter Generation: For each row in the CSV:

  Relevant details like company name, job title, and job description are extracted.
    
  These details are passed to a function that uses a series of prompts to first condense the resume and then generate a cover letter.
  
  The generated cover letter is saved back to the dataframe.
  
–Saving the Output: Once all rows have been processed, the dataframe is saved in .csv formats.

# FUTURE IMPROVEMENTS

Improvements could be made in several areas:

Resume Condensing:
The resume condensing chain performs adequately, but changing it to a few-shot template would be helpful for performance. Unfortunately, proper examples here would include multiple iterations of full resumes and full job descriptions, and this becomes a very expensive operation quickly, as well as quite slow. Research into how a few-shot template could be made that uses partial examples would be valuable.

Scraping and Interpretation:
In its current version, the .csv is still a human labor-intensive process, involving significant cutting and pasting of data. Ideally, the user should only have to paste the link in to the spreadsheet, and all data could be scraped. Using the scraped data as an input, a LangChain function could be written to interpret that data and output it as a string in dictionary format using ast.literal_eval(). This has its own challenges, as it is difficult to wrangle LLMs to output the correct information in that format; it often involves multiple layers of hallucination correction via an agent to dampen hallucinations (to be clear, the formatting will be correct, but often not the data in it). This increases costs significantly, and if looped until correct can run up against API rate limits. Testing is required to assess if this gets to "good enough" without the hallucination dampening.

Company Personalization:
Job descriptions often lack the flowery copy of PR output, mission statements, etc. This text provides a great way to indicate a closer personal connection to the company, and a buy-in to the company ethos. Using the url provided, and repurposing much of my previous work without the onerous GUI automation aspects could provide for a corporate psychographic inference to drive this personalization. It would likely take additional lines in the cover letter prompt template as well.

Resumes Dictionary:
Rather than building a resumes dictionary, a LangChain function could be written to read the job description and title, and choose the best resume for it. That resume would then be passed in to get_cover_letters(). 

Layers of Experts:
Because this process is non-deterministic, and different iterations, temperatures, etc. provide very different outputs, it could be valuable to run the same cover letter through multiple temperatures, then provide a LangChain function to either choose the best, or ideally combine the best elements of each into a single cover letter. Additionally, other elements could be added to the chain to correct for grammar, restructure, provide and respond to rhetorical critique. Each of these adds cost and time to the process, but demonstrably increases output quality.

Formatting for Send:
Providing an input template such as a word file, which the results of this would be pasted in, then converted to .pdf would close the loop, providing for a completely hands-off proces of cover letter creation.
    
# CONTRIBUTIONS AND FEEDBACK

Feel free to fork this repository, contribute to enhance its capabilities, or adapt it to your needs. Feedback, issues, and pull requests are highly appreciated!
