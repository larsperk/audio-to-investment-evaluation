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
SUMMARY_FILENAME = "summary.md"
EVALUATION_FILENAME = "evaluation.md"
TRANSCRIPTION_FILENAME = "transcription.txt"

# OPENAI_MODEL = 'gpt-4-turbo-2024-04-09'      # 'gpt-4'
OPENAI_MODEL = 'gpt-4o'      # 'gpt-4'
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


def main():
    log_message("investment evaluator started")
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
            subject = work_task.get("subject") or "DEFAULT"
            detail_level = str(work_task.get("detail_level"))

            subject = subject or "DEFAULT"

            chunked_text = chunk_text(raw_text)

            summary_prompts = {k: v.replace("{detail_level}", detail_level)
                               for k, v in constants.summary_prompts[subject].items()}

            consolidated_summary = []
            outline = False
            for chunk in chunked_text:
                if chunk:
                    log_message("Summary start")
                    prelude = constants.summary_prelude[subject]

                    p = prelude.find("{INCLUDE:")
                    if p != -1:
                        q = prelude.find("}", p)
                        if q > p:
                            include_file = prelude[p+9:q].replace(" ", "")
                            _, extension = os.path.splitext(include_file.lower())
                            if extension == ".txt":
                                with open(include_file, "r", encoding="utf-8") as txt:
                                    prelude = prelude[:p] + txt.read() + prelude[q+1:]
                            elif extension == ".pdf":
                                prelude = prelude[:p] + email_utils.convert_pdf_to_txt(include_file) + prelude[q+1:]
                            else:
                                pass

                    if "{outline=True}" in prelude:
                        prelude = prelude.replace("{outline=True}", "")
                        outline = True
                    summary = ask_questions_of_text(
                        prelude,
                        constants.summary_prompts[subject].keys(),
                        summary_prompts,
                        chunk
                    )

                    consolidated_summary.append(summary)
            log_message("Summary complete")

            summary_of_summaries = ""
            if len(chunked_text) == 1:
                summary_of_summaries = consolidated_summary[0]
            elif len(chunked_text) > 1:
                summary_of_summaries = consolidate_answers(consolidated_summary)

            log_message("Evaluation start")
            evaluation_text = ""
            if constants.evaluation_prelude[subject]:
                evaluation_text = evaluate_business_for_investment(
                    constants.evaluation_prelude[subject],
                    summary_of_summaries
                )
            log_message("Evaluation complete")

            if from_email:
                with open(TRANSCRIPTION_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(raw_text)

                with open(SUMMARY_FILENAME, "w", encoding="utf-8") as txt:
                    txt.write(summary_of_summaries)

                if evaluation_text:
                    has_evaluation = True
                    with open(EVALUATION_FILENAME, "w", encoding="utf-8") as txt:
                        txt.write(evaluation_text)
                else:
                    has_evaluation = False

                files_to_send, email_body_text = email_utils.convert_markdown_to_docx(
                    subject, has_evaluation, outline
                )

                email_utils.send_email(
                    from_email, files_to_send[0], email_body_text, files_to_send
                )
                email_utils.send_email(
                    "lars@larsperkins.com", f"Evaluation processed for {from_email}", email_body_text,
                    files_to_send
                )
                log_message("Reply sent")
                os.remove(work_file)


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
    chat_response = response.choices[0].message.content + '\r'

    return chat_response


def determine_subject_name(subject, input_line):
    if subject in constants.summary_prelude.keys():
        chat_response = []
        if input_line:
            source_line = input_line[1] + '\n' + input_line[2] + '\n' + input_line[3] + '\n' + input_line[4]
            messages = [
                {"role": "system", "content": "Consider the provided information and answer "
                                              "as a helpful AI agent with only the name of the company:\n\n"},
                {"role": "user", "content": f'"{source_line}"\n\n"What is the name of the company.'
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
                "SORRY",
                "DOES NOT",
                "DON'T HAVE",
                "NOT PROVIDED",
                "YOU DID NOT",
            ]

            name_unknown = [True for words in disqualifier_words if words in chat_response]
        else:
            name_unknown = True

        if not name_unknown:
            name_to_use = chat_response[:32]
        else:
            name_to_use = "Unknown"
    else:
        name_to_use = "Unknown"

    return name_to_use or "Unknown"


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


if __name__ == "__main__":
    main()
