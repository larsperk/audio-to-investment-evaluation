import openai
import numpy as np
import os
import whisper
import json

import email_utils_2

from dotenv import load_dotenv

SAMPLE_RATE = 44100
CHANNELS = 1
DATA_TYPE = np.int16

RAW_FILENAME_BASE = "recorded_audio"
SUMMARY_FILENAME = "summary.txt"
EVALUATION_FILENAME = "evaluation.txt"
TRANSCRIPTION_FILENAME = "transcription.txt"

OPENAI_MODEL = 'gpt-4'      # 'gpt-3.5-turbo'
TEMPERATURE = 0.5
CHUNK_SIZE = 10000

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
email_pass = os.getenv('EMAIL_PASS')
email_user = "investmentevaluator@gmail.com"


def get_unique_audio_filename():
    filename_base = RAW_FILENAME_BASE
    i = 0
    filename = filename_base + "_" + str(i)
    while os.path.isfile(filename):
        i += 1
        filename = filename_base + "_" + str(i)

    return filename


def transcribe_audio(raw_audio_file, transcription_file):
    model = whisper.load_model("base")
    audio = raw_audio_file
    result = model.transcribe(audio)

    with open(transcription_file, "w", encoding="utf-8") as txt:
        txt.write(result["text"])

    return result["text"]


def chunk_text(raw_text):
    chunk_size = CHUNK_SIZE
    chunk_overlap = 200

    chunked_text = []
    while len(raw_text) > 0:
        chunked_text.append(raw_text[:chunk_size])
        temp = raw_text[(chunk_size-chunk_overlap):]
        raw_text = temp

    return chunked_text


def ask_questions_of_text(prelude, prompt_list, prompts, text):
    aggregate_questions = ""
    for prompt in prompt_list:
        aggregate_questions += prompts[prompt] + ". Please put the answer under the heading " + prompt + "" + "\r"

    messages = [
        {"role": "system", "content": prelude + '\r\r\"' + text},
        {"role": "user", "content": aggregate_questions},
    ]
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=TEMPERATURE
    )

    chat_response = response.choices[0]['message']['content'] + '\r'

    return chat_response


def evaluate_business_for_investment(prelude, company_summary):
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": prelude},
            {"role": "user", "content": company_summary},
        ],
        temperature=TEMPERATURE
    )
    chat_response = response.choices[0]['message']['content'] + '\r'

    return chat_response


def consolidate_answers(chunk_answers):
    prelude = "The supplied documents are\r" \
            + "summaries of conversations with an entrepreneur about a new business.\r" \
            + "Please act as a helpful AI agent."

    i = 1
    documents = ""
    for chunk_answer in chunk_answers:
        documents += "Document "+ str(i) + '\r\n'
        documents += chunk_answer + '\r\n\r\n'
        i += 1
    documents += "Please consolidate\r" \
                 + "the information in the preceding " + str(len(chunk_answers)) + " documents into a single document\r" \
                 + "preserving section headings and eliminating duplicate information\r\n"

    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": prelude},
            {"role": "user", "content": documents},
        ],
        temperature=TEMPERATURE
    )
    chat_response = response.choices[0]['message']['content'] + '\r'

    return chat_response


def check_for_work_to_do():
    work_to_do_dir = email_utils_2.WORK_TO_DO_DIR
    if not os.path.exists(work_to_do_dir):
        os.mkdir(work_to_do_dir)

    files = [os.path.join(email_utils_2.WORK_TO_DO_DIR, filename)
         for filename in os.listdir(email_utils_2.WORK_TO_DO_DIR)]

    return files


def main():
    print("audio-to-investment-summary started")
    prelude = 'The following is a transcript between an interviewer and an entrepreneur,\r' \
              + 'who is starting a business and discussing their business and their product.\r' \
              + 'Please refer to the entrepreneur "they" rather than "the entrepreneur"\r' \
              + 'please answer as a helpful ai agent' \
              + 'please be as detailed as possible. if you don\'t know the answer, please answer "unknown",' \
              + 'try not to say "the information is not in the supplied transcript", just answer "unknown"\r'

    prompt_list = ["NAME", "PROBLEM", "SOLUTION", "WHY", "TEAM", "CTO", "TEAM EXPERIENCE", "TRACTION", "FUNDING",
                   "TECH", "TAM", "TIMING", "COMPETITION", "LEISURE"]

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
        "LEISURE": 'what do the founders and cofounders do in their spare time for hobbies, avocations and interests, sports'
    }

    evaluation_prelude = 'the following is a summary of a business that is being considered for investment.\r' \
                         + 'The positive characteristics of a business that is good to invest in are:\r' \
                         + ' 1. significant traction in terms of waitlist, customers, and revenue\r' \
                         + ' 2. an experienced founding team who either together or individually have founded other businesses\r' \
                         + ' 3. a large potential market greater than 500 million in size\r' \
                         + ' 4. a team that has worked together before, preferably at a company with an exit\r' \
                         + ' 5. Proprietary differentiated technology\r' \
                         + ' 6. Team members are involved in competitive sports or other disciplined activities in their free time\r' \
                         + ' 7. They have raised at least 250000 in funding\r' \
                         + ' 8. They been in business for less than three years\r' \
                         + ' 9. They more than one founder\r' \
                         + ' 10. All founders working full-time for the business\r' \
                         + 'Please evaluate the business from the summary and enumerate the points above as they \r' \
                         + 'apply to the presented business. Also give your overall conclusion about whether this\r' \
                         + 'business is a good candidate for investment.'

    while True:
        files = check_for_work_to_do()

        if len(files) == 0:
            email_utils_2.check_email_and_download()
            files = check_for_work_to_do()

        files_by_create_date = sorted(files, key=lambda x: os.path.getctime(x), reverse=True)

        for work_file in files_by_create_date:
            with open(work_file, "r") as f:
                work_task = json.load(f)

            raw_text = work_task["text"]
            from_email = work_task["from"]

            chunked_text = chunk_text(raw_text)

            consolidated_answers = ''
            for chunk in chunked_text:
                if chunk:
                    answers = (ask_questions_of_text(prelude, prompt_list, prompts, chunk))
                    consolidated_answers += answers
            print("Summary complete")

            if len(chunked_text) > 1:
                summary_of_summaries = ask_questions_of_text(prelude, prompt_list, prompts, consolidated_answers)
            else:
                summary_of_summaries = consolidated_answers

            evaluation = evaluate_business_for_investment(evaluation_prelude, summary_of_summaries)
            print("Evaluation complete")

            if from_email:
                with open(TRANSCRIPTION_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(raw_text)

                with open(SUMMARY_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(summary_of_summaries)

                with open(EVALUATION_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(evaluation)

                email_utils_2.send_email(
                    from_email, "Investment evaluation", "See attachments",
                    [TRANSCRIPTION_FILENAME, SUMMARY_FILENAME, EVALUATION_FILENAME]
                )
                email_utils_2.send_email(
                    "lars@larsperkins.com", f"Evaluation processed for {from_email}", "See attachments",
                    [TRANSCRIPTION_FILENAME, SUMMARY_FILENAME, EVALUATION_FILENAME]
                )
                print("Reply sent")
                os.remove(work_file)


if __name__ == "__main__":
    main()

