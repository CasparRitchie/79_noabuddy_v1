# voice_agent.py
import sounddevice as sd
import queue
import vosk
import json
import wave
import ollama
import numpy as np
import time
import os

MODEL_PATH = os.path.abspath("../vosk_model/vosk-model-small-en-us-0.15")
SAMPLE_RATE = 16000
DEVICE_INDEX = None
AUDIO_FILENAME = "recorded.wav"
SILENCE_THRESHOLD = 300
SILENCE_DURATION = 2.0

q = queue.Queue()


def get_best_microphone():
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if "JBL" in device["name"]:
            return i
    return sd.default.device["input"]


def callback(indata, frames, time, status):
    if status:
        print(f"⚠️ Recording Error: {status}")
    q.put(indata.copy())


def is_silent(audio_chunk):
    volume_norm = np.linalg.norm(np.frombuffer(audio_chunk, dtype=np.int16))
    return volume_norm < SILENCE_THRESHOLD


def save_audio(data_chunks):
    with wave.open(AUDIO_FILENAME, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(data_chunks))


def transcribe_and_return_text():
    print("📥 Loading Vosk model...")
    model = vosk.Model(MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    device_index = DEVICE_INDEX if DEVICE_INDEX is not None else get_best_microphone()
    recorded_audio = []
    full_text = ""

    print(" Recording... Speak now!")

    with sd.InputStream(samplerate=SAMPLE_RATE, device=device_index, channels=1, dtype="int16", callback=callback):
        last_audio_time = time.time()

        try:
            while True:
                data = q.get()
                recorded_audio.append(data)

                if is_silent(data):
                    if time.time() - last_audio_time > SILENCE_DURATION:
                        break
                else:
                    last_audio_time = time.time()

                if recognizer.AcceptWaveform(data.tobytes()):
                    result = json.loads(recognizer.Result())["text"]
                    if result:
                        full_text += result + " "
                else:
                    partial_result = json.loads(recognizer.PartialResult())["partial"]
                    if partial_result:
                        print(f"⏳ {partial_result}", end="\r")

        except KeyboardInterrupt:
            print(" Stopped manually")

    save_audio(recorded_audio)
    return full_text.strip()


def transcribe_uploaded_audio(path_to_wav):
    print("📥 Loading Vosk model for uploaded file...")
    model = vosk.Model(MODEL_PATH)
    rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    wf = wave.open(path_to_wav, "rb")
    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            results.append(res.get("text", ""))
    final = json.loads(rec.FinalResult())
    results.append(final.get("text", ""))
    return " ".join(results).strip()


def send_to_ollama(text):
    import time
    print("🔄 Sending to Ollama...")
    start = time.time()

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "system",
                "content": "You are Noa, a relationship guidance assistant..."
            },
            {"role": "user", "content": text}
        ]
    )

    duration = time.time() - start
    print(f"⏱️ Ollama took {duration:.2f} seconds to respond")
    return response['message']['content']



def get_response_from_audio():
    try:
        print("🎙 Starting transcription...")
        transcript = transcribe_and_return_text()
        print(f"📝 Transcript: {transcript}")

        if not transcript:
            return "I didn’t catch anything. Could you repeat that?"

        print(" Sending transcript to Ollama...")
        response = send_to_ollama(transcript)
        print(f" Ollama responded: {response}")
        return response

    except Exception as e:
        print(f"Error during processing: {e}")
        return "Something went wrong while processing your voice."
