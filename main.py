import openai
import numpy as np
import os
import json

import email_utils
import constants

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
    i = 1
    documents = ""
    for chunk_answer in chunk_answers:
        documents += "Document "+ str(i) + '\r\n'
        documents += chunk_answer + '\r\n\r\n'
        i += 1
    documents += constants.consolidate_postscript_1 + str(len(chunk_answers)) + constants.consolidate_postscript_2

    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": constants.role_description},
            {"role": "user", "content": documents},
        ],
        temperature=TEMPERATURE
    )
    chat_response = response.choices[0]['message']['content'] + '\r'

    return chat_response


def check_for_work_to_do():
    work_to_do_dir = email_utils.WORK_TO_DO_DIR
    if not os.path.exists(work_to_do_dir):
        os.mkdir(work_to_do_dir)

    files = [os.path.join(email_utils.WORK_TO_DO_DIR, filename)
         for filename in os.listdir(email_utils.WORK_TO_DO_DIR)]

    return files


def main():
    print("audio-to-investment-summary started")
    while True:
        files = check_for_work_to_do()

        if len(files) == 0:
            email_utils.get_emails_and_create_work_files()
            files = check_for_work_to_do()

        files_by_create_date = sorted(files, key=lambda x: os.path.getctime(x), reverse=True)

        for work_file in files_by_create_date:
            with open(work_file, "r") as f:
                work_task = json.load(f)

            raw_text = work_task["text"]
            from_email = work_task["from"]

            chunked_text = chunk_text(raw_text)

            consolidated_summary = ''
            for chunk in chunked_text:
                if chunk:
                    summary = ask_questions_of_text(
                        constants.prelude, constants.prompt_list, constants.prompts, chunk
                    )

                    consolidated_summary += summary
            print("Summary complete")

            if len(chunked_text) > 1:
                summary_of_summaries = ask_questions_of_text(
                    constants.prelude, constants.prompt_list, constants.prompts, consolidated_summary
                )
            else:
                summary_of_summaries = consolidated_summary

            evaluation = evaluate_business_for_investment(constants.evaluation_prelude, summary_of_summaries)
            print("Evaluation complete")

            if from_email:
                with open(TRANSCRIPTION_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(raw_text)

                with open(SUMMARY_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(summary_of_summaries)

                with open(EVALUATION_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(evaluation)

                email_utils.send_email(
                    from_email, "Investment evaluation", "See attachments",
                    [TRANSCRIPTION_FILENAME, SUMMARY_FILENAME, EVALUATION_FILENAME]
                )
                email_utils.send_email(
                    "lars@larsperkins.com", f"Evaluation processed for {from_email}", "See attachments",
                    [TRANSCRIPTION_FILENAME, SUMMARY_FILENAME, EVALUATION_FILENAME]
                )
                print("Reply sent")
                os.remove(work_file)


if __name__ == "__main__":
    main()

