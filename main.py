import openai
import os
import json
import whisper
from datetime import datetime
import assemblyai as aai

import email_utils
import constants

from dotenv import load_dotenv

RAW_FILENAME_BASE = "recorded_audio"
SUMMARY_FILENAME = "summary.txt"
EVALUATION_FILENAME = "evaluation.txt"
TRANSCRIPTION_FILENAME = "transcription.txt"

OPENAI_MODEL = 'gpt-3.5-turbo'      # 'gpt-4'
TEMPERATURE = 0.5
CHUNK_SIZE = 10000
CHUNK_OVERLAP = 200

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
email_pass = os.getenv('EMAIL_PASS')
email_user = "investmentevaluator@gmail.com"
aai.settings.api_key = os.getenv('AAI_API_KEY')


def transcribe_audio_using_whisper(raw_audio_file, transcription_file):
    model = whisper.load_model("tiny")
    audio = raw_audio_file
    log_message(f"transcribe {raw_audio_file} -> {transcription_file}")
    result = model.transcribe(audio)
    log_message(f"transcribe {transcription_file} complete")

    with open(transcription_file, "w", encoding="utf-8") as txt:
        txt.write(result["text"])

    return result["text"]


def transcribe_audio_using_aai(raw_audio_file, transcription_file):

    transcriber = aai.Transcriber()

    log_message(f"transcribe {raw_audio_file} -> {transcription_file}")
    result = transcriber.transcribe(raw_audio_file)
    log_message(f"transcribe {transcription_file} complete")

    with open(transcription_file, "w", encoding="utf-8") as txt:
        txt.write(result.text)

    return result.text


def chunk_text(raw_text):
    chunk_size = CHUNK_SIZE
    chunk_overlap = CHUNK_OVERLAP

    chunked_text = []
    while len(raw_text) > 0:
        chunked_text.append(raw_text[:chunk_size])
        raw_text = raw_text[(chunk_size-chunk_overlap):]

    return chunked_text


def ask_questions_of_text(categories, prelude, prompt_list, prompts, text):
    aggregate_questions = ""
    chat_responses = ""

    for category in categories:
        for prompt in prompt_list[category]:
            aggregate_questions += prompts[category][prompt] + \
                                   ". Please put the answer under the heading " + prompt + "\r"

        messages = [
            {"role": "system", "content": prelude + '\r\r\"' + text},
            {"role": "user", "content": aggregate_questions},
        ]
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=TEMPERATURE
        )

        chat_response = response.choices[0].message.content + '\r'
        chat_responses += chat_response

    return chat_responses


def evaluate_business_for_investment(prelude, company_summary):
    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": prelude},
            {"role": "user", "content": company_summary},
        ],
        temperature=TEMPERATURE
    )
    chat_response = response.choices[0].message.content + '\r'

    return chat_response


def consolidate_answers(chunk_answers):
    i = 1
    documents = ""
    for chunk_answer in chunk_answers:
        documents += "Document " + str(i) + '\r\n'
        documents += chunk_answer + '\r\n\r\n'
        i += 1
    documents += constants.consolidate_prompt_1 + str(len(chunk_answers)) + constants.consolidate_prompt_2

    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": constants.consolidate_prelude},
            {"role": "user", "content": documents},
        ],
        temperature=TEMPERATURE
    )
    chat_response = response.choices[0]['message']['content'] + '\r'

    return chat_response


def get_name_of_company(input_line):
    messages = [
        {"role": "system", "content": "Consider the following sentence and answer "
                                      "as a helpful AI agent with only the name of the company"},
        {"role": "user", "content": f'"{input_line}"\n"What is the name of the company?' },
    ]
    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.0
    )
    chat_response = response.choices[0].message.content
    if chat_response[-1:] == ".":
        chat_response = chat_response[:-1]

    return chat_response


def check_for_work_to_do():
    work_to_do_dir = email_utils.WORK_TO_DO_DIR
    if not os.path.exists(work_to_do_dir):
        os.mkdir(work_to_do_dir)

    files = [
        os.path.join(email_utils.WORK_TO_DO_DIR, filename)
        for filename in os.listdir(email_utils.WORK_TO_DO_DIR)
    ]

    return files


def log_message(message):
    print(f"{datetime.now()} : {message}\r\n")
    with open("log_IE.txt", "a") as myfile:
        myfile.write(f"{datetime.now()} : {message}\r\n")

    return


def main():
    log_message("audio-to-investment-summary started")
    # docx_filename = email_utils.convert_txt_to_docx(SUMMARY_FILENAME, EVALUATION_FILENAME)
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
                    log_message("Summary start")
                    summary = ask_questions_of_text(
                        constants.summary_prompt_categories,
                        constants.summary_prelude,
                        constants.summary_prompt_list,
                        constants.summary_prompts,
                        chunk
                    )

                    consolidated_summary += summary
            log_message("Summary complete")

            if len(chunked_text) > 1:
                summary_of_summaries = ask_questions_of_text(
                    constants.summary_prompt_categories,
                    constants.summary_prelude,
                    constants.summary_prompt_list,
                    constants.summary_prompts,
                    consolidated_summary
                )
            else:
                summary_of_summaries = consolidated_summary

            log_message("Evaluation start")
            evaluation = evaluate_business_for_investment(
                constants.evaluation_prelude,
                summary_of_summaries
            )
            log_message("Evaluation complete")

            if from_email:
                with open(TRANSCRIPTION_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(raw_text)

                with open(SUMMARY_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(summary_of_summaries)

                with open(EVALUATION_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(evaluation)

                docx_filename = email_utils.convert_txt_to_docx(SUMMARY_FILENAME, EVALUATION_FILENAME)

                email_utils.send_email(
                    from_email, docx_filename, "See attachments",
                    [TRANSCRIPTION_FILENAME, docx_filename]
                )
                email_utils.send_email(
                    "lars@larsperkins.com", f"Evaluation processed for {from_email}", "See attachments",
                    [TRANSCRIPTION_FILENAME, docx_filename]
                )
                log_message("Reply sent")
                os.remove(work_file)


if __name__ == "__main__":
    main()
