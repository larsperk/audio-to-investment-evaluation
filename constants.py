# Ask questions of text

summary_prelude = {
    "DEFAULT": 'Please answer as a helpful ai agent.\n'
               + 'The following is a transcript between an interviewer and an entrepreneur,\n'
               + 'who is starting a business and discussing their business and their product.\n'
               + 'Refer to the entrepreneur as "they" rather than "the entrepreneur."\n'
               + 'Be as detailed as possible when answering the questions."\n'
               + 'If you don\'t know the answer, please answer "unknown"',
    "SUMMARY": 'Please answer as a helpful AI agent.',
    "DISCHARGE": 'Please act as a helpful AI agent.\n'
                 'The following is a letter describing a patient who has received medical care.\n'
                 'The author is a doctor and is written to a general practitioner who will be responsible\n'
                 'for the patient\'s care after they are discharged'


}

summary_prompt_list = {
    "DEFAULT": [
        "NAME", "PROBLEM", "SOLUTION", "WHY", "TEAM", "CTO", "TEAM EXPERIENCE", "TRACTION", "FUNDING",
        "TECH", "TAM", "TIMING", "COMPETITION", "LEISURE", "PROGRAMS",
        ],
    "SUMMARY": [
        "SUMMARY"
        ],
    "DISCHARGE": [
        "STORY", "ACTIONS PERFORMED", "ACTIONS REQUESTED",
        ],
}


summary_prompts = {
    "DEFAULT": {
        "NAME": 'what is the name of the company that the entrepreneur '
                'is talking about and how long has it been in business?',
        "PROBLEM": 'what problems are they solving, and what customers have these problems?',
        "SOLUTION": 'how does their product solve the problem',
        "WHY": 'what is their primary motivation for building the business',
        "TEAM": 'what are the names and roles of founders and co-founders '
                '(CEO, CTO, COO, and any other C-level executives) and are they working full time on the company?',
        "CTO": 'who is the chief technology officer and what are his/her qualifications?',
        "TEAM EXPERIENCE": 'has the CEO founded any other company, '
                           'and is this the first time the founders have worked together',
        "TRACTION": 'how many customers do they have and what is their revenue?, '
                    'and what are the names of their customers and prospects, including those on their waitlist',
        "FUNDING": 'how has the company been funded to-date, is it bootstrapped, self-funded, '
                   'or has it received friends and family investment or professional investment '
                   'and how much has been raised',
        "TECH": 'what technologies are they using in their product and what makes those technologies unique',
        "TAM": 'how big is the market they\'re addressing both in numbers of customers and dollar size',
        "TIMING": 'is there something happening in technology or the market or society '
                  'that makes this more relevant or more possible right now',
        "COMPETITION": "who are the company's competitors and what are their weaknesses",
        "LEISURE": 'what do the founders and co-founders do in their spare time '
                   'for hobbies, avocations and interests, or sports',
        "PROGRAMS": 'has the company attended any other accelerator, incubator, or similar program'
         },
    "SUMMARY": {
        "SUMMARY": "Please summarize the major points of this transcript in {detail_level} bullets or less."
        },
    "DISCHARGE": {
        "STORY": "tell the story of why the patient was initially hospitalized.",
        "ACTIONS PERFORMED": "list the actions performed while the patient was in the hospital",
        "ACTIONS REQUESTED": "list the actions that the physician is requesting from the general "
                             "practitioner and whether they are indicated or contraindicated given the patient's story."
    }
}


# Consolidate Answers

consolidate_prelude = "The supplied documents are summaries of conversations\n" \
                      + "Please act as a helpful AI agent."

consolidate_prompt = "Please consolidate the information in the preceding {number_docs} " \
                     "documents into a single document\n " \
                     "preserving section headings and eliminating duplicate information.\n" \
                     "Please be as detailed as possible.\n"

# Evaluation

evaluation_prelude = {
    "DEFAULT": 'The following is a summary of a business that is being considered for investment.\n'
               'The positive characteristics of a business that is good to invest in are:\n'
               ' 1. Significant traction in terms of waitlist, customers, and revenue\n'
               ' 2. An experienced founding team who either together or individually '
               'have founded other businesses\n'
               ' 3. A large potential market greater than 500 million in size\n'
               ' 4. A team that has worked together before, preferably at a company '
               'that had an IPO or was acquired\n'
               ' 5. Proprietary differentiated technology\n'
               ' 6. Already raised (not the amount they are trying to raise now) '
               'at least 250,000 dollars in funding\n'
               ' 7. Have been in business for less than three years\n'
               ' 8. More than one founder\n'
               ' 9. All founders working full-time for the business\n'
               'Please evaluate the business from the summary and enumerate the points above as they \n'
               'apply to the presented business. Count the number of points that they meet.\n'
               'Also give your overall conclusion about whether '
               'this business is a good candidate for investment. Also, after the preceding overview, '
               'under the heading "SUGGESTED QUESTIONS:" suggest questions to be asked to elicit information'
               ' on the unknown characteristics.\n',
    "DISCHARGE": '',
    "SUMMARY": ''
}

