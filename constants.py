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
                 'for the patient\'s care after they are discharged',
    "VESPER": 'Please answer as a helpful AI agent helping to summarize'
              ' information related to a business seeking investment.\n',
    "GENERAL": 'Please answer as a helpful AI agent helping to summarize'
               ' information related to a business seeking investment. \n',
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
    "VESPER": [
        "NAME",
        "PROBLEM",
        "SOLUTION",
        "SECTOR",
        "RISK",
        "DISRUPTION",
        "CYCLICALITY",
        "US-BASED",
        "EBITDA",
        "EV",
        "OPERATING HISTORY",
        "GROWTH",
        "MARGIN",
        "REVENUE CONCENTRATION",
        "SUPPLIER CONCENTRATION",
        "ROLLUP",
        "OWNERSHIP",
        "CONFLICT OF INTEREST",
        "VALUE ADD",
        "INVESTMENT SIZE",
        "RETURN PROFILE",
        "DEBT",
        "MANAGEMENT CONTINUITY",
        "BILATERAL PATH",
        "TIMING",
        "CULTURE",
        "EXPERIENCE",
        "STRATEGY",
        "COMPETITION"
    ],
    "GENERAL": [
        "NAME",
        "SECTOR",
        "PROBLEM",
        "SOLUTION",
        "TEAM",
        "TRACTION",
        "TECH",
        "TAM",
        "COMPETITION",
        "INVESTMENT SIZE",
        "INVESTMENT USE"
    ]
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
    },
    "VESPER": {
        "NAME": 'what is the name of the company?',
        "PROBLEM": 'what problems are they solving, and what customers have these problems?',
        "SOLUTION": 'how does their product solve the problem',
        "SECTOR": "what sector is the company in?"
                  " e.g. Content; financial services; tech-enabled & professional services",
        "RISK": "are there regulatory or reimbursement risks for the company or associated with its sector?",
        "DISRUPTION": "is the company or sector at risk of being disrupted by tech innovation?",
        "CYCLICALITY": "is the company or sector cyclical?",
        "US-BASED": "is the company US-based or its revenue majority US-based?",
        "EBITDA": "what is the company's earnings before interest, taxes, depreciation, and amortization?",
        "EV": "approximately what is the company's enterprise value?",
        "OPERATING HISTORY": "how long has the company been in business?",
        "GROWTH": "what is the company's growth rate?",
        "MARGIN": "what is the company's gross margin?",
        "REVENUE CONCENTRATION": "is the company\'s revenue concentrated in a few customers?",
        "SUPPLIER CONCENTRATION": "is the company\'s supply chain concentrated in a few suppliers?",
        "ROLLUP": "is the company part of a rollup?",
        "OWNERSHIP": "what is the ownership structure of the company?",
        "CONFLICT OF INTEREST": "is there a conflict of interest with other Vesper investments?",
        "VALUE ADD": "what value add can Vesper provide to the company?",
        "INVESTMENT SIZE": "what is the size of the investment?",
        "RETURN PROFILE": "what is the expected return profile of the investment?",
        "DEBT": "what is the company's debt?",
        "MANAGEMENT CONTINUITY": "will management remain with the company post investment?",
        "BILATERAL PATH": "is there a bilateral path to exit?",
        "TIMING": "is there enough time to run a 3-month investment process?",
        "CULTURE": "is the company's culture a good fit with Vesper's culture?",
        "EXPERIENCE": "does management have industry experience and knowledge?",
        "STRATEGY": "is there a relevant and clear value creation strategy?",
        "COMPETITION": "is there a clear competitive differentiation and/or moat?",
    },
    "GENERAL": {
        "NAME": 'what is the name of the company?',
        "SECTOR": "what sector is the company in?"
                  " e.g. Content; financial services; tech-enabled & professional services",
        "PROBLEM": 'what problems are they solving, and what customers have these problems?',
        "SOLUTION": 'how does their product solve the problem',
        "TEAM": 'what are the names and roles of the executive team',
        "TRACTION": 'how many customers do they have and what is their annual revenue?',
        "TECH": 'what technologies are they using in their product',
        "TAM": 'how big is the market they\'re addressing both in numbers of customers and dollar size',
        "COMPETITION": "who are the company's competitors and what are their weaknesses",
        "INVESTMENT SIZE": "what size investment are they looking for?",
        "INVESTMENT USE": "what will they use the investment for?",
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
    "SUMMARY": '',
    "VESPER": '',
    "GENERAL": '',
}

