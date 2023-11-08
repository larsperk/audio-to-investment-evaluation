"""
import wave
import threading
import sounddevice as sd
import numpy as np
"""

"""
SAMPLE_RATE = 44100
CHANNELS = 1
DATA_TYPE = np.int16
"""

"""
def get_unique_audio_filename():
    filename_base = RAW_FILENAME_BASE
    i = 0
    filename = filename_base + "_" + str(i)
    while os.path.isfile(filename):
        i += 1
        filename = filename_base + "_" + str(i)

    return filename

"""

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
