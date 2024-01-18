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

OPENAI_MODEL = 'gpt-4-1106-preview'      # 'gpt-4'
TEMPERATURE = 0.0
CHUNK_SIZE = 16384
CHUNK_OVERLAP = 200

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
email_pass = os.getenv('EMAIL_PASS')
email_user = "investmentevaluator@gmail.com"
aai.settings.api_key = os.getenv('AAI_API_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


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
    chunked_text = []
    while len(raw_text) > 0:
        chunked_text.append(raw_text[:CHUNK_SIZE])
        raw_text = raw_text[(CHUNK_SIZE-CHUNK_OVERLAP):]

    return chunked_text


def ask_questions_of_text(prelude, prompt_list, prompts, text):
    aggregate_questions = ""
    chat_responses = ""

    for prompt in prompt_list:
        aggregate_questions += prompts[prompt] + \
                               ". Please put the answer underneath the heading " + prompt + ":\n\n"

    messages = [
        {"role": "system", "content": prelude + '\n\n' + text},
        {"role": "user", "content": aggregate_questions},
    ]
    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=TEMPERATURE
    )

    chat_response = response.choices[0].message.content + '\n'
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
        documents += "Document " + str(i) + '\n'
        documents += chunk_answer + '\n\n'
        i += 1
    documents += constants.consolidate_prompt.replace("{number_docs}", str(i-1))

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


def determine_subject_name(subject, input_line):
    if subject == "DEFAULT" or subject == "VESPER" or subject == "GENERAL" or subject == "2ND" or subject == "VC":
        if input_line:
            messages = [
                {"role": "system", "content": "Consider the following sentence and answer "
                                              "as a helpful AI agent with only the name of the company:\n\n"},
                {"role": "user", "content": f'"{input_line[1]}"\n\n"What is the name of the company.'
                                            f' Answer with only the name of the company?'},
            ]
            response = openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.0
            )
            chat_response = response.choices[0].message.content.strip().upper()
            if chat_response[:26] == 'THE NAME OF THE COMPANY IS':
                chat_response = chat_response[27:]
            if chat_response[-1:] == ".":
                chat_response = chat_response[:-1]

            disqualifier_words = [
                "I'M SORRY",
                "DOES NOT",
                "DON'T HAVE",
                "NOT PROVIDED"
            ]

            name_unknown = [True for words in disqualifier_words if words in chat_response]
        else:
            name_unknown = True

        if not name_unknown:
            name_to_use = chat_response[:32]
        else:
            name_to_use = "Unknown"

    elif subject == "DISCHARGE":
        name_to_use = "Discharge"

    else:
        name_to_use = "Summary"

    return name_to_use


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
    print(f"{datetime.now()} : {message}")
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

            raw_text = work_task.get("text")
            from_email = work_task.get("from")
            subject = work_task.get("subject")
            detail_level = str(work_task.get("detail_level"))

            subject = subject or "DEFAULT"

            chunked_text = chunk_text(raw_text)

            summary_prompts = {k: v.replace("{detail_level}", detail_level)
                               for k, v in constants.summary_prompts[subject].items()}

            consolidated_summary = ''
            for chunk in chunked_text:
                if chunk:
                    log_message("Summary start")
                    summary = ask_questions_of_text(
                        constants.summary_prelude[subject],
                        constants.summary_prompt_list[subject],
                        summary_prompts,
                        chunk
                    )

                    consolidated_summary += summary
            log_message("Summary complete")

            if len(chunked_text) > 1:
                summary_of_summaries = ask_questions_of_text(
                    constants.summary_prelude[subject],
                    constants.summary_prompt_list[subject],
                    summary_prompts,
                    consolidated_summary
                )
            else:
                summary_of_summaries = consolidated_summary

            log_message("Evaluation start")
            evaluation = ""
            if constants.evaluation_prelude[subject]:
                evaluation = evaluate_business_for_investment(
                    constants.evaluation_prelude[subject],
                    summary_of_summaries
                )
            log_message("Evaluation complete")

            if from_email:
                with open(TRANSCRIPTION_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(raw_text)

                with open(SUMMARY_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(summary_of_summaries)

                if evaluation:
                    with open(EVALUATION_FILENAME, "w", encoding="utf-8") as txt:
                        txt.write(evaluation)

                summary_docx, evaluation_docx = email_utils.convert_txt_to_docx(
                    subject, SUMMARY_FILENAME, EVALUATION_FILENAME
                )

                files_to_send = [TRANSCRIPTION_FILENAME, summary_docx]
                if evaluation:
                    files_to_send.append(evaluation_docx)

                email_utils.send_email(
                    from_email, summary_docx, "See attachments",
                    files_to_send
                )
                email_utils.send_email(
                    "lars@larsperkins.com", f"Evaluation processed for {from_email}", "See attachments",
                    files_to_send
                )
                log_message("Reply sent")
                os.remove(work_file)


if __name__ == "__main__":
    main()
