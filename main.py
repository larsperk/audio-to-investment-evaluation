import os

import whisper
import sounddevice as sd
import numpy as np
import wave
import threading
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

SAMPLE_RATE = 44100
CHANNELS = 1
DATA_TYPE = np.int16
RAW_FILENAME = "54 Clay Brook Rd 2.m4a"
# "recorded_audio.wav"

TRANSCRIPTION_FILENAME = "transcription.text"
OPENAI_MODEL = 'gpt-4'


audio_buffer = []


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


def transcribe_audio(raw_audio_file, transcription_file):
    model = whisper.load_model("base")
    audio = raw_audio_file
    result = model.transcribe(audio)

    with open(transcription_file, "w", encoding="utf-8") as txt:
        txt.write(result["text"])

    return result["text"]

def chunk_text(raw_text):
    chunked_text = [raw_text]
    return chunked_text


def ask_questions_of_chunk(prelude, prompt_list, prompts, text):
    aggregate_response = ''
    for prompt in prompt_list:

        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": prelude + '\r\r\"' + text},
                {"role": "user", "content": prompts[prompt]},
            ],
            temperature=0.9
        )

        chat_response = response.choices[0]['message']['content'] + '\r'
        aggregate_response += prompt + '\r' + chat_response + '\r'

    return aggregate_response

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

#, only using information in the supplied text transcript'        + 'of the interview.\r'\
def main():
    prelude = 'The following is a transcript between an interviewer and an entrepreneur,\r'\
        + 'who is starting a business and discussing their business and their product.\r'\
        + 'Please call the entrepreneur "they." rather than "the entrepreneur"\r'\
        + 'please answer as a helpful ai agent'\
        + 'please be as detailed as possible. if you don\'t know the answer, please answer "unknown",' \
        + 'try not to say "the information is not in the supplied transcript", just answer "unknown"\r'

    prompt_list = ["NAME", "PROBLEM", "SOLUTION", "TEAM", "TRACTION", "TECH", "TAM", "TIMING", "COMPETITION", "LEISURE", "TEAM EXPERIENCE", "FIRST TIME FOUNDER?"]

    prompts = {
                "NAME": 'what is the name of the company that the entrepreneur is talking about and how long has it been in business',
                "PROBLEM": 'what problems are they solving, and what customers have these problems',
                "SOLUTION": 'how does their product solve the problem',
                "TEAM": 'what are the names and roles of founders and cofounders of the company and what are their educations and roles. That includes CEO, CTO, COO, and any other C-level executives  and are they working full time',
                "TRACTION": 'how many customers do they have, and what are the names of their customers and prospects, including those on their waitlist',
                "FUNDING": 'how has the company been funded to-date, is it bootstrapped, self-funded, or has it received friends and family investment or professional investment. and how much has been raised',
                "TECH": 'what technologies are they using in their product and what makes those technologies unique',
                "TAM": 'how big is the market they\'re addressing both in numbers of customers and dollar size',
                "TIMING": 'is there something happening in technology or the market or society that makes this more relevant or more possible right now',
                "COMPETITION": "who are the company's competitors and whart are their weakneseses",
                "LEISURE": 'what do the founders and cofounders do in their spare time for hobbies, avocations and interests, sports',
                "TEAM EXPERIENCE": 'is this the first time the founders have worked together or do they have prior experience together',
                "FIRST TIME FOUNDER?": 'has the ceo and other members of the founding team started another startup previously or is this their first company'
            }

    techstars_prelude = 'the following is a summary of a business that is being considered for investment.\r'\
                        + 'The positive characteristics of a business that is good to invest in are:\r'\
                        + ' 1. significant traction in terms of waitlist, customers, and revenue\r'\
                        + ' 2. an experienced founding team who either together or individually have founder other businesses\r'\
                        + ' 3. a large potential market\r'\
                        + ' 4. a team that has worked together before, preferably at a company with an exit\r'\
                        + ' 5. Proprietary differentiated technology\r'\
                        + ' 6. The team members have been involved in competitive sports or other disciplined activities in their free time\r'\
                        + ' 7. They have raised at least 250000 in funding\r'\
                        + ' 8. The company has been in business for less than three years\r'\
                        + ' The negative characteristics of a business that is not a good investment candidate are:\r'\
                        + ' 1. Sole founders without other co-founders\r'\
                        + ' 2. Been in business longer than 5 years\r'\
                        + ' 3. Small market that is less than 500 million dollars\r'\
                        + ' 4. Strong competition without a clear differentiation\r'\
                        + ' 5. Not much technology in their solution or nothing proprietary\r'\
                        + ' 6. Founders who are not working full-time for the business\r'\
                        + 'please evaluate the business from the summary and give your conclusion as to whether\r' \
                        + ' it is a good investment. Please enumerate the points above as they apply to the presented business'


    """
    global stop_recording
    stop_recording = False

    recording_thread = threading.Thread(target=record_audio)
    recording_thread.start()

    input("Press Enter to stop recording...")
    stop_recording = True
    recording_thread.join()

    save_audio(raw_audio_data, RAW_FILENAME)
    """

    raw_text = transcribe_audio(RAW_FILENAME, TRANSCRIPTION_FILENAME)
    chunked_text = chunk_text(raw_text)

    for chunk in chunked_text:
        chunk_answers = ask_questions_of_chunk(prelude, prompt_list, prompts, chunk)

        evalution = evaluate_business_for_investment(techstars_prelude, chunk_answers)
        pass

if __name__ == "__main__":
    main()
