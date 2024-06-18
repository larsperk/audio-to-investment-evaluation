summary_prelude = {
    "DEFAULT": 'Please answer as a helpful ai agent.\n'
               + 'The following is a transcript between an interviewer and an entrepreneur,\n'
               + 'who is starting a business and discussing their business and their product.\n'
               + 'The interviewer will make some points and deliver opinions after the interview is over.\n'
               + 'Refer to the entrepreneur as "they" rather than "the entrepreneur."\n'
               + 'Be as detailed as possible when answering the questions."\n'
               + 'If you don\'t know the answer, please answer "unknown"',
    "TECHSTARS": 'Please answer as a helpful AI agent.\n'
               + 'The following is a transcript between an interviewer and an entrepreneur,\n'
               + 'who is starting a business and discussing their business and their product.\n'
               + 'The interviewer will make some points and deliver opinions after the interview is over.\n'
               + 'Refer to the entrepreneur as "they" rather than "the entrepreneur."\n'
               + 'Be as detailed as possible when answering the questions."\n'
               + 'If you don\'t know the answer, please answer "unknown"',
    "SUMMARY": '{outline=True}Please answer as a helpful AI agent.',
    "SUMMARY_WITH_MEMO": '{outline=True}Please answer as a helpful AI agent.',
    "DISCHARGE": 'Please act as a helpful AI agent.\n'
                 'The following is a letter describing a patient who has received medical care.\n'
                 'The author is a doctor and is written to a general practitioner who will be responsible\n'
                 'for the patient\'s care after they are discharged',
    "VESPER": 'Please answer as a helpful AI agent helping to summarize'
              ' information related to a business seeking investment.\n',
    "GENERAL": 'Please answer as a helpful AI agent helping to summarize'
               ' information related to a business seeking investment. \n',
    "2ND": 'Please answer as a helpful AI agent helping to summarize '
           'information related to a business seeking investment. \n',
    "VC": 'Please answer as a helpful AI agent helping to summarize '
          'information related to a business seeking investment. \n',
    "TECH DILIGENCE": 'Please answer as a helpful AI agent helping to summarize '
          'technical information discussed in a conversation. \n',
    "MEDICAL": 'Please answer as a helpful AI agent helping to summarize '
               'information in the attached annual medical report. \n',
}


summary_prompts = {
    "DEFAULT": {
        "NAME": 'what is the name of the company that the entrepreneur '
                'is talking about, where is it located, and how long has it been in business?',
        "PROBLEM": 'what problems are they solving, and what customers have these problems?',
        "SOLUTION": 'how does their product solve the problem',
        "WHY": 'what is their primary motivation for building the business',
        "BUSINESS MODEL": 'what is their business model, '
                          'how do they make money, and what is their pricing?',
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
        "BIGGEST RISK": 'what are the biggest risks to the company\'s success'
                        ' and how are they mitigating those risks',

        "PROGRAMS": 'has the company attended any other accelerator, incubator, or similar program',
        "INTERVIEWER NOTES": "Please summarize points that the interviewer enumerated "
                             "at the end of the interview",
         },
    "TECHSTARS": {
        "NAME": 'what is the name of the company that the entrepreneur '
                'is talking about, where is it located, and how long has it been in business?',
        "PROBLEM": 'what problems are they solving, and what customers have these problems?',
        "SOLUTION": 'how does their product solve the problem',
        "WHY": 'what is their primary motivation for building the business',
        "BUSINESS MODEL": 'what is their business model, '
                          'how do they make money, and what is their pricing?',
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
        "BIGGEST RISK": 'what are the biggest risks to the company\'s success'
                        ' and how are they mitigating those risks',

        "PROGRAMS": 'has the company attended any other accelerator, incubator, or similar program',
        "EXPECTED VALUE FROM TECHSTARS": 'what does the company hope to get out of attending the Techstars accelerator',
        "ATTENDANCE": 'Are the founders available to attend the 13 week accelerator program in person',
        "DEAL": 'do the founders understand the Techstars deal terms and are they willing to accept them',
        "INTERVIEWER NOTES": "Please summarize points that the interviewer enumerated "
                             "at the end of the interview",
         },
    "SUMMARY": {
        "SUMMARY": "You are an AI agent who is an expert at summarizing documents by creating outlines."
                   "Outline the major points of this document in {detail_level} outline headings or fewer."
                   "Under each major outline heading, use subheadings to provide detail on the major point. "
                   "Use as many subheadings as necessary to describe the point in as much detail as possible."
                   "indent each subheading to show its relationship to the point above it.\n\n"
                   "For example:\n\n"
                   "1. Major heading describing major point covered in the document\n"
                   "   1.1 Sub heading providing detail on the major point (1)\n"
                   "   1.2 Sub heading providing more detail on the major point (1)\n"
                   "      1.2.1 Sub heading providing more detail on the minor point (1.2)\n\n"
        },
    "SUMMARY_WITH_MEMO": {
        "SUMMARY": "You are an AI agent who is an expert at summarizing documents by creating outlines."
                   "Outline the major points of this document."
                   "Under each major outline heading, use subheadings to provide detail on the major point. "
                   "Use as many subheadings as necessary to describe the point in as much detail as possible."
                   "indent each subheading to show its relationship to the point above it.\n\n"
                   "For example:\n\n"
                   "1. Major heading describing major point covered in the document\n"
                   "   1.1 Sub heading providing detail on the major point (1)\n"
                   "   1.2 Sub heading providing more detail on the major point (1)\n"
                   "      1.2.1 Sub heading providing more detail on the minor point (1.2)\n\n"
                   "After creating the outline, write a one-page prose memo describing the document's main "
                   "points. Under each major point in the memo, write two to three sentences describing the point. "
                   "At the end, suggest questions to ask the author to clarify any unclear points."
    },
    "DISCHARGE": {
        "STORY": "tell the story of why the patient was initially hospitalized.",
        "ACTIONS PERFORMED": "list the actions performed while the patient was in the hospital",
        "ACTIONS REQUESTED": "list the actions that the physician is requesting from the general "
                             "practitioner and whether they are indicated or contraindicated given the patient's story."
    },
    "VESPER": {
        "NAME": 'what is the name of the company?',
        "SECTOR": "what sector is the company in?"
                  " e.g. media; Content; financial services; professional services;"
                  "sports, fintech, healthtech, edtech, etc.",
        "PROBLEM": 'what problems are they solving, and what customers have these problems?',
        "SOLUTION": 'how does their product solve the problem',
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
        "BUSINESS MODEL": "what is their business model, "
                          "how do they make money, and what is their pricing?",
        "TEAM": 'what are the names and roles of the executive team',
        "EXPERIENCE": 'what is the executive team\'s experience?',
        "TRACTION": 'how many customers do they have and what is their annual revenue?',
        "TECH": 'what technologies are they using in their product',
        "TAM": 'how big is the market they\'re addressing both in numbers of customers and dollar size',
        "COMPETITION": "who are the company's competitors and what are their weaknesses",
        "INVESTMENT SIZE": "what size investment are they looking for?",
        "INVESTMENT USE": "what will they use the investment for?",
    },
    "2ND": {
        "NAME": 'what is the name of the company that the entrepreneur is speaking about?',
        "SUMMARY": "Provide a general summary of the business",
        "TEAM": 'what are the names, roles, and equity ownership of founders and co-founders '
                '(CEO, CTO, COO, and any other C-level executives) and are they working full time on the company?',
        "CAP TABLE": 'besides the founding team, who else is on the cap table?',
        "TAM": 'how big is the market they\'re addressing both in numbers of customers and dollar size'
               'what is the service addressable market (SAM) and service obtainable market (SOM)?',
        "COMPETITION": "who are the company's competitors, how big are they, how have they been funded"
                       " and what are their weaknesses? please be as detailed as possible",
        "TECH": 'provide a detailed description of what technologies are used'
                ' in their product and what makes those technologies unique',
        "PRODUCT": 'provide a detailed description of the product\'s features and benefits',
        "DEVELOPMENT STATUS": "what is the status of the product's development?",
        "IP": "is there proprietary intellectual property and how is it protected?",
        "TRACTION": 'provide a detailed list of what customers, pilots, and design partners the company has',
        "GO TO MARKET": "what is the company's go to market strategy?",
        "TECHSTARS": "specifically and in detail, what do they hope to get out of attending the Techstars accelerator?",
        "CONVERTIBLE NOTE": "Would the company want the $100,000 convertible note Techstars offers?",
        "REFERENCE": 'Who would the founder provide if asked to provide a reference?',
        "INTERVIEWER NOTES": "Please summarize points that the interviewer enumerated "
                             "at the end of the interview",
    },
    "VC": {
        "NAME": 'what is the name of the company that the entrepreneur is speaking about?',
        "SUMMARY": "provide a summary of this conversation with key points."
                   "Focus the key points as if you were a venture capitalist trying to explain the "
                   "main parts of the business including team, technology, market, and traction. Include "
                   "information, if available, on funding the company has already received. Each point should be under"
                   "its own heading. For example, when describing the team, the heading would be "
                   "'TEAM' and underneath would be a description of the team.  WHen describing the technology, "
                   "the heading would be 'TECHNOLOGY', etc. Also include a section on future"
                   "plans and long-term vision. This should be under the heading 'FUTURE PLANS'."
                   "Lastly, include a section on their competitive moat, i.e. what will prevent others"
                   "from easily competing with them. This should be under the heading 'COMPETITIVE MOAT'.",
        "INTERVIEWER NOTES": "Please summarize points that the interviewer enumerated "
                             "at the end of the interview",
        "QUESTIONS": "As an investor, what questions should be asked of the entrepreneur to validate that this"
                     "is a good investment? Keep in mind that determining the likelihood of an investment\'s success'"
                     "requires understanding team, timing, business maturity, traction, product readiness, competition,"
                     "market size, technology, intellectual property, and funding, among other factors."
    },
    "TECH DILIGENCE": {
        "NAME": 'what is the name of the company that is being discussed, and on what date did this conversation occur?',
        "PRODUCTS": "Describe the company and the products or services it offers in a few sentences.",
        "PRODUCT AND TECHNOLOGY OVERVIEW": "What are the components of the company's product suite or service?",
        "TECHNOLOGY STACK": "What technologies are used in the company's product?",
        "TECHNOLOGY TEAM": "Who are the key members of the technology team and what are their roles?",
        "CONCERNS": "List any concerns discussed abou tthe technology or team.",
        "RECOMMENDATIONS": "List any recommendations for further investigation or due diligence.",
        "SUMMARY": "Summarize the key points of the conversation, including any comments identified as summary points.",
    },
    "MEDICAL": {
        "DATE": 'what is the date of the medical report?',
        "NAME": 'what is the name, gender, and age of the patient?',
        "HISTORY": 'what is the patient\'s medical history?',
        "MEDICATIONS": 'what medications is the patient currently taking?',
        "ALLERGIES": 'what allergies does the patient have?',
        "DIAGNOSIS": "what is the diagnosis of the patient?",
        "BLOOD WORK": "what are the results of the patient's blood work, both currently and over time?",
        "CARDIAC": "what are the results of the patient's cardiac tests?",
        "IMAGING": "what are the results of the patient's imaging studies?",
        "TREATMENT": "what treatment was provided to the patient?",
        "FOLLOWUP": "what follow-up care is recommended for the patient?",
        "INTERVIEWER NOTES": "Please summarize points that the interviewer enumerated "
                             "at the end of the interview",
    },
}
# Consolidate Answers

consolidate_prelude = "The supplied documents are summaries of conversations. Act as a helpful AI agent."

consolidate_prompt = "Consolidate the information in the preceding {number_docs} documents into a single document,\n" \
                     "preserving section headings and eliminating duplicate information.\n" \
                     "Be as detailed as possible.\n"

evaluation_prelude = {
    "DEFAULT": 'Below is a summary of a business that is being considered for investment.\n'
               'Evaluate the business from the summary and list how well the business meets\n'
               'each of these positive characteristics. List each characteristic, and indicate \n'
               'whether or not the company has met it by\n'
               'putting "MET or "NOT MET" or "PARTIALLY MET" on the same line as each characteristic.\n\n'
               'Ensure that the funding amount used in the evaluation is funds already raised, '
               'not the amount they are trying to raise now. If the funding details state various departments or uses\n'
               'for the funds, that indicates it is the desired funding and not the amount that has \n'
               'already been raised.\n\n'
               ' 1. Significant traction in terms of waitlist and/or customers, and/or revenue '
               '- MET or NOT MET or PARTIALLY MET\n'
               ' 2. An experienced founding team who either together or individually '
               'have founded other businesses.  - MET or NOT MET or PARTIALLY MET\n'
               ' 3. A large potential market greater than 1 billion in size - MET or NOT MET\n'
               ' 4. A team that has worked together before - MET or NOT MET or PARTIALLY MET\n'
               ' 5. Proprietary differentiated technology - MET or NOT MET or PARTIALLY MET\n'
               ' 6. Already raised at least 250,000 dollars in funding - MET or NOT MET or PARTIALLY MET\n'
               ' 7. Have been in business for less than three years - MET or NOT MET or PARTIALLY MET\n'
               ' 8. More than one founder - MET or NOT MET or PARTIALLY MET\n'
               ' 9. All founders working full-time for the business - MET or NOT MET or PARTIALLY MET\n\n'
               'After listing all the characteristics, under the heading "BUSINESS MODEL:"\n'
               'indicate whether the business is a B2B SaaS business, a marketplace, a consumer software company,\n'
               'a hardware company without an ongoing subscription, or a hardware company with an '
               'ongoing subscription. If the business model is not clear, indicate that as well.\n'
               'Under the heading "OVERALL SCORE:" on a single line, count the number of positive characteristics '
               'that are met, not met, and partially met.\n'
               'Under the heading "SUGGESTED QUESTIONS:", suggest questions to be asked to elicit '
               'information on the unknown characteristics.\n'
               'Under the heading "OVERALL CONCLUSION:", give your overall conclusion about whether '
               'this business is a good candidate for investment.\n Please answer as a helpful AI agent. \n\n',
    "TECHSTARS": 'Below is a summary of a business that is being considered for investment.\n'
               'Evaluate the business from the summary and list how well the business meets\n'
               'each of these positive characteristics. List each characteristic, and indicate \n'
               'whether or not the company has met it by\n'
               'putting "MET or "NOT MET" or "PARTIALLY MET" on the same line as each\n'
               'characteristic.\n'
               'Ensure that the funding amount used in the evaluation is funds already raised, '
               'not the amount they are trying to raise now. If the funding details state various departments or uses\n'
               'for the funds, that indicates it is the desired funding and not the amount that has \n'
               'already been raised.\n\n'
               ' 1. Significant traction in terms of waitlist and/or customers, and/or revenue '
               '- MET or NOT MET or PARTIALLY MET\n'
               ' 2. An experienced founding team who either together or individually '
               'have founded other businesses - MET or NOT MET or PARTIALLY MET\n'
               ' 3. A large potential market greater than 1 billion in size - MET or NOT MET or PARTIALLY MET\n'
               ' 4. A team that has worked together before - MET or NOT MET or PARTIALLY MET\n'
               ' 5. Proprietary differentiated technology - MET or NOT MET or PARTIALLY MET\n'
               ' 6. Already raised at least 250,000 dollars in funding - MET or NOT MET or PARTIALLY MET\n'
               ' 7. Have been in business for less than three years - MET or NOT MET or PARTIALLY MET\n'
               ' 8. More than one founder - MET or NOT MET or PARTIALLY MET\n'
               ' 9. All founders working full-time for the business - MET or NOT MET or PARTIALLY MET\n\n'
               'After listing all the characteristics, under the heading "OVERALL SCORE:"\n'
               'Count the number of positive characteristics that are met, not met, and partially met \n'
               'and list those three categories on a single line.\n'
               'Under the heading "SUGGESTED QUESTIONS:" suggest questions to be asked to elicit\n'
               'information on the unknown characteristics.\n'
               'Under the heading "OVERALL CONCLUSION:", give your overall conclusion about whether\n'
               'this business is a good candidate for investment.\n'
               'Please answer as a helpful AI agent. \n\n',
    "DISCHARGE": '',
    "SUMMARY": '',
    "SUMMARY_WITH_MEMO": '',
    "VESPER": '',
    "GENERAL": '',
    "2ND": '',
    "VC": '',
    "TECH DILIGENCE": '',
    "MEDICAL": '',
}

