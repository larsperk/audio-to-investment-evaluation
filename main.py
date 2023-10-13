import os

"""
import wave
import threading
import sounddevice as sd
"""

import whisper
import numpy as np
import openai
from dotenv import load_dotenv
import email_utils
import time

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

MODE = 'EMAIL'  # EMAIL or MICROPHONE or AUDIO or FORCE TEXT

SAMPLE_RATE = 44100
CHANNELS = 1
DATA_TYPE = np.int16

RAW_FILENAME_BASE = "recorded_audio"
SUMMARY_FILENAME = "summary.txt"
EVALUATION_FILENAME = "evaluation.txt"
FORCED_TEXT_FILENAME = "sample-andres.txt"
TRANSCRIPTION_FILENAME = "transcription.txt"

OPENAI_MODEL = 'gpt-4'      # 'gpt-3.5-turbo'
CHUNK_SIZE = 10000

audio_buffer = []


def get_unique_audio_filename():
    filename_base = RAW_FILENAME_BASE
    i = 0
    filename = filename_base + "_" + str(i)
    while os.path.isfile(filename):
        i += 1
        filename = filename_base + "_" + str(i)

    return filename


"""
def recording_callback(indata, frames, time, status):
    audio_buffer.append(indata.copy())


def record_audio():
    # This creates a streaming object that uses our callback.
    # It'll keep recording until we stop it.
    with sd.InputStream(callback=recording_callback, channels=CHANNELS, samplerate=SAMPLE_RATE, dtype=DATA_TYPE):
        while not stop_recording:
            sd.sleep(1000)  # Sleep for 1 second increments and then check for the stop flag

    global raw_audio_data
    raw_audio_data = np.concatenate(audio_buffer, axis=0)


def save_audio(raw_audio_data, filename):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 2 bytes for int16
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(raw_audio_data.tobytes())
    print(f"Saved to {filename}")

    return
"""


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
        aggregate_questions += prompts[prompt] + ". Please put the answer under the heading '" + prompt + "'" + "\r"

    messages = [
        {"role": "system", "content": prelude + '\r\r\"' + text},
        {"role": "user", "content": aggregate_questions},
    ]
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.9
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
        temperature=0.9
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
        temperature=0.9
    )
    chat_response = response.choices[0]['message']['content'] + '\r'

    return chat_response


def main():
    print("audio-to-investment-summary started")
    while True:
        prelude = 'The following is a transcript between an interviewer and an entrepreneur,\r'\
            + 'who is starting a business and discussing their business and their product.\r'\
            + 'Please refer to the entrepreneur "they" rather than "the entrepreneur"\r'\
            + 'please answer as a helpful ai agent'\
            + 'please be as detailed as possible. if you don\'t know the answer, please answer "unknown",' \
            + 'try not to say "the information is not in the supplied transcript", just answer "unknown"\r'

        prompt_list = ["NAME", "PROBLEM", "SOLUTION", "TEAM", "TRACTION", "CTO", "FUNDING", "TECH", "TAM", "TIMING",
                       "COMPETITION", "WHY", "LEISURE", "TEAM EXPERIENCE", "FIRST TIME FOUNDER"]

        prompts = {
                    "NAME": 'what is the name of the company that the entrepreneur is talking about and how long has it been in business?',
                    "PROBLEM": 'what problems are they solving, and what customers have these problems?',
                    "SOLUTION": 'how does their product solve the problem',
                    "TEAM": 'what are the names and roles of founders and co-founders of (CEO, CTO, COO, and any other C-level executives) and are they working full time on the company?',
                    "TRACTION": 'how many customers do they have and what is their revenue?, and what are the names of their customers and prospects, including those on their waitlist',
                    "CTO": 'Who is the chief technology officer and what are his/her qualifications?',
                    "FUNDING": 'how has the company been funded to-date, is it bootstrapped, self-funded, or has it received friends and family investment or professional investment. and how much has been raised',
                    "TECH": 'what technologies are they using in their product and what makes those technologies unique',
                    "TAM": 'how big is the market they\'re addressing both in numbers of customers and dollar size',
                    "TIMING": 'is there something happening in technology or the market or society that makes this more relevant or more possible right now',
                    "COMPETITION": "who are the company's competitors and what are their weakneseses",
                    "WHY": 'What is their primary motivation for building the business',
                    "LEISURE": 'what do the founders and cofounders do in their spare time for hobbies, avocations and interests, sports',
                    "TEAM EXPERIENCE": 'is this the first time the founders have worked together or do they have prior experience together',
                    "FIRST TIME FOUNDER": 'has the ceo fonded any other company? with the other members of the founding team?'
                }

        evaluation_prelude = 'the following is a summary of a business that is being considered for investment.\r'\
                            + 'The positive characteristics of a business that is good to invest in are:\r'\
                            + ' 1. significant traction in terms of waitlist, customers, and revenue\r'\
                            + ' 2. an experienced founding team who either together or individually have founded other businesses\r'\
                            + ' 3. a large potential market\r'\
                            + ' 4. a team that has worked together before, preferably at a company with an exit\r'\
                            + ' 5. Proprietary differentiated technology\r'\
                            + ' 6. The team members have been involved in competitive sports or other disciplined activities in their free time\r'\
                            + ' 7. They have raised at least 250000 in funding\r'\
                            + ' 8. The company has been in business for less than three years\r'\
                            + ' The negative characteristics of a business that is not a good investment candidate are:\r'\
                            + ' 1. There is only one founder without other co-founders\r'\
                            + ' 2. They have been in business longer than 5 years\r'\
                            + ' 3. They have a small potential market that is less than 500 million dollars in total size\r'\
                            + ' 4. They have no clear differentiation from their competition\r'\
                            + ' 5. There is not much technology in their solution or there is no proprietary technology\r'\
                            + ' 6. The founders are not working full-time for the business\r'\
                            + 'please evaluate the business from the summary and give your conclusion as to whether\r' \
                            + ' it is a good investment. Please enumerate the points above as they apply to the presented business'

        audio_filename = ""
        from_email = None
        """
        if MODE == "MICROPHONE":
            global stop_recording
            stop_recording = False

            recording_thread = threading.Thread(target=record_audio)
            recording_thread.start()

            input("Press Enter to stop recording...")
            stop_recording = True
            recording_thread.join()
            audio_filename = get_unique_audio_filename()
            save_audio(raw_audio_data, audio_filename)
        """
        if MODE == "EMAIL":
            from_email, audio_filename = email_utils.check_email_and_download()
            print(f"Email received from: {from_email}")
        elif MODE == "AUDIO":
            audio_filename = "54 Clay Brook Rd 2.m4a"
        elif MODE == "FORCE TEXT":
            audio_filename = FORCED_TEXT_FILENAME

        if audio_filename.endswith(".txt"):
            text_filename = TRANSCRIPTION_FILENAME #fix
            with open(text_filename, "r") as file:
                raw_text = file.read()
        else:
            raw_text = transcribe_audio(audio_filename, TRANSCRIPTION_FILENAME)

        chunked_text = chunk_text(raw_text)
        print("Transcription complete")

        evaluation = []
        consolidated_answers = ''
        for chunk in chunked_text:
            if chunk:
                answers = (ask_questions_of_text(prelude, prompt_list, prompts, chunk))
                consolidated_answers += answers

        print("Summary complete")

        summary_of_summaries = ask_questions_of_text(prelude, prompt_list, prompts, consolidated_answers)
        evaluation = evaluate_business_for_investment(evaluation_prelude, summary_of_summaries)
        print("Evaluation complete")

        if from_email:
            with open(SUMMARY_FILENAME, "w", encoding="utf-8") as txt:
                txt.write(summary_of_summaries)

            with open(EVALUATION_FILENAME, "w", encoding="utf-8") as txt:
                txt.write(evaluation)

            email_utils.send_email(from_email, [TRANSCRIPTION_FILENAME, SUMMARY_FILENAME, EVALUATION_FILENAME])
            print("Reply sent")


if __name__ == "__main__":
    main()
