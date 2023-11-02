# Ask questions of text

prelude = 'Please answer as a helpful ai agent.' \
          + 'The following is a transcript between an interviewer and an entrepreneur,\r' \
          + 'who is starting a business and discussing their business and their product.\r' \
          + 'Refer to the entrepreneur as "they" rather than "the entrepreneur."\r' \
          + 'Be as detailed as possible when answering the questions."\r' \
          + 'If you don\'t know the answer, please answer "unknown",'


prompt_list = ["NAME", "PROBLEM", "SOLUTION", "WHY", "TEAM", "CTO", "TEAM EXPERIENCE", "TRACTION", "FUNDING",
               "TECH", "TAM", "TIMING", "COMPETITION", "LEISURE", "OTHER PROGRAMS"]

prompts = {
    "NAME": 'what is the name of the company that the entrepreneur is talking about and how long has it been in business?',
    "PROBLEM": 'what problems are they solving, and what customers have these problems?',
    "SOLUTION": 'how does their product solve the problem',
    "WHY": 'What is their primary motivation for building the business',
    "TEAM": 'what are the names and roles of founders and co-founders of (CEO, CTO, COO, and any other C-level executives) and are they working full time on the company?',
    "CTO": 'Who is the chief technology officer and what are his/her qualifications?',
    "TEAM EXPERIENCE": 'has the CEO founded any other company, and is this the first time the founders have worked together',
    "TRACTION": 'how many customers do they have and what is their revenue?, and what are the names of their customers and prospects, including those on their waitlist',
    "FUNDING": 'how has the company been funded to-date, is it bootstrapped, self-funded, or has it received friends and family investment or professional investment. and how much has been raised',
    "TECH": 'what technologies are they using in their product and what makes those technologies unique',
    "TAM": 'how big is the market they\'re addressing both in numbers of customers and dollar size',
    "TIMING": 'is there something happening in technology or the market or society that makes this more relevant or more possible right now',
    "COMPETITION": "who are the company's competitors and what are their weaknesses",
    "LEISURE": 'what do the founders and cofounders do in their spare time for hobbies, avocations and interests, or sports',
    "OTHER PROGRAMS": 'Has the company attended any other accelerator, incubator, or similar program'
}

# Consolidate Answers

role_description = "The supplied documents are\r" \
          + "summaries of conversations with an entrepreneur about a new business.\r" \
          + "Please act as a helpful AI agent."

consolidate_postscript_1 = "Please consolidate\r" \
                 + "the information in the preceding "

consolidate_postscript_2 = " documents into a single document\r" \
                 + "preserving section headings and eliminating duplicate information.\r"\
                 + "Please be as detailed as possible.\r\n"


# Evaluation

evaluation_prelude = 'The following is a summary of a business that is being considered for investment.\r' \
                     + 'The positive characteristics of a business that is good to invest in are:\r' \
                     + ' 1. Significant traction in terms of waitlist, customers, and revenue\r' \
                     + ' 2. An experienced founding team who either together or individually have founded other businesses\r' \
                     + ' 3. A large potential market greater than 500 million in size\r' \
                     + ' 4. A team that has worked together before, preferably at a company that had an IPO or was acquired\r' \
                     + ' 5. Proprietary differentiated technology\r' \
                     + ' 6. Already raised (not the amount they are trying to raise now) at least 250,000 dollars in funding\r' \
                     + ' 7. Have been in business for less than three years\r' \
                     + ' 8. More than one founder\r' \
                     + ' 9. All founders working full-time for the business\r' \
                     + 'Please evaluate the business from the summary and enumerate the points above as they \r' \
                     + 'apply to the presented business. Count the number of points that they meet.\r' \
                     + 'Also give your overall conclusion about whether this business is a good candidate for investment.'

