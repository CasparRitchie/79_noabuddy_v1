# # # from fastapi import FastAPI, UploadFile, File
# # # from fastapi.middleware.cors import CORSMiddleware
# # # import vosk
# # # import wave
# # # import json
# # # import os
# # # import ollama
# # # import pyttsx3  # ✅ for voice playback

# # # app = FastAPI()

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],  # Adjust this in production
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # MODEL_PATH = os.path.abspath("../vosk_model/vosk-model-small-en-us-0.15")
# # # AUDIO_DIR = "uploads"
# # # os.makedirs(AUDIO_DIR, exist_ok=True)

# # # try:
# # #     model = vosk.Model(MODEL_PATH)
# # # except Exception as e:
# # #     print(f"❌ Failed to load Vosk model from {MODEL_PATH}")
# # #     raise


# # # def transcribe_wav(path):
# # #     wf = wave.open(path, "rb")
# # #     if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
# # #         raise ValueError("Audio must be mono WAV with 16kHz, 16-bit")

# # #     rec = vosk.KaldiRecognizer(model, wf.getframerate())
# # #     results = []
# # #     while True:
# # #         data = wf.readframes(4000)
# # #         if len(data) == 0:
# # #             break
# # #         if rec.AcceptWaveform(data):
# # #             results.append(json.loads(rec.Result())["text"])
# # #     results.append(json.loads(rec.FinalResult())["text"])
# # #     return " ".join([r for r in results if r.strip()])


# # # def speak_response(text):
# # #     engine = pyttsx3.init()
# # #     engine.setProperty('rate', 175)
# # #     engine.say(text)
# # #     engine.runAndWait()


# # # def chat_with_ollama(text):
# # #     response = ollama.chat(
# # #         model="mistral",
# # #         messages=[
# # #             {
# # #                 "role": "system",
# # #                 "content": "You are Noa, a warm, succinct, and helpful relationship coach. Keep your answers short (1–2 sentences).",
# # #             },
# # #             {"role": "user", "content": text}
# # #         ]
# # #     )
# # #     reply = response["message"]["content"]
# # #     print(f"🧠 Ollama's Response: {reply}")
# # #     speak_response(reply)  # ✅ speak response aloud
# # #     return reply


# # # @app.post("/api/speak")
# # # async def speak(file: UploadFile = File(...)):
# # #     audio_path = os.path.join(AUDIO_DIR, file.filename)

# # #     audio_data = await file.read()
# # #     with wave.open(audio_path, 'wb') as wf:
# # #         wf.setnchannels(1)
# # #         wf.setsampwidth(2)
# # #         wf.setframerate(16000)
# # #         wf.writeframes(audio_data)

# # #     transcript = transcribe_wav(audio_path)
# # #     if not transcript.strip():
# # #         return {"transcript": "", "response": "No speech detected."}

# # #     reply = chat_with_ollama(transcript)
# # #     return {"transcript": transcript, "response": reply}


# # from fastapi import FastAPI, UploadFile, File
# # from fastapi.middleware.cors import CORSMiddleware
# # import pyttsx3.drivers
# # import vosk
# # import wave
# # import json
# # import os
# # import ollama
# # # 🛠 Workaround for pyttsx3 + pyobjc import bug on macOS
# # import pyttsx3
# # import sys

# # if sys.platform == 'darwin':
# #     import objc  # manually load objc before nsss driver tries
# #     pyttsx3.drivers.objc = objc  # monkey patch it
# # import subprocess
# # import uuid

# # app = FastAPI()

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # MODEL_PATH = os.path.abspath("../vosk_model/vosk-model-small-en-us-0.15")
# # AUDIO_DIR = "uploads"
# # os.makedirs(AUDIO_DIR, exist_ok=True)

# # try:
# #     model = vosk.Model(MODEL_PATH)
# # except Exception as e:
# #     print(f"❌ Failed to load Vosk model from {MODEL_PATH}")
# #     raise


# # def convert_to_mono_wav(source_path: str, output_path: str):
# #     result = subprocess.run([
# #         "ffmpeg", "-y",
# #         "-i", source_path,
# #         "-ac", "1",
# #         "-ar", "16000",
# #         "-sample_fmt", "s16",
# #         output_path
# #     ], capture_output=True)

# #     if result.returncode != 0:
# #         raise RuntimeError(f"FFmpeg conversion failed:\n{result.stderr.decode()}")


# # def transcribe_wav(path):
# #     wf = wave.open(path, "rb")
# #     if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
# #         raise ValueError("Audio must be mono WAV with 16kHz, 16-bit")

# #     rec = vosk.KaldiRecognizer(model, wf.getframerate())
# #     results = []
# #     while True:
# #         data = wf.readframes(4000)
# #         if len(data) == 0:
# #             break
# #         if rec.AcceptWaveform(data):
# #             results.append(json.loads(rec.Result())["text"])
# #     results.append(json.loads(rec.FinalResult())["text"])
# #     return " ".join([r for r in results if r.strip()])


# # def speak_response(text):
# #     engine = pyttsx3.init()
# #     engine.setProperty('rate', 175)
# #     engine.say(text)
# #     engine.runAndWait()


# # def chat_with_ollama(text):
# #     response = ollama.chat(
# #         model="mistral",
# #         messages=[
# #             {"role": "system", "content": "You are Noa, a warm, succinct, and helpful relationship coach. Keep your answers short (1–2 sentences)."},
# #             {"role": "user", "content": text}
# #         ]
# #     )
# #     reply = response["message"]["content"]
# #     print(f"🧠 Ollama's Response: {reply}")
# #     speak_response(reply)
# #     return reply

# # @app.post("/api/speak")
# # async def speak(file: UploadFile = File(...)):
# #     original_filename = file.filename
# #     base_filename = os.path.splitext(original_filename)[0]  # remove extension
# #     safe_id = uuid.uuid4().hex
# #     raw_audio_path = os.path.join(AUDIO_DIR, f"{safe_id}_{base_filename}.webm")
# #     converted_wav_path = os.path.join(AUDIO_DIR, f"{safe_id}_{base_filename}.wav")

# #     # 🔽 Save raw uploaded file
# #     with open(raw_audio_path, "wb") as f:
# #         f.write(await file.read())

# #     try:
# #         convert_to_mono_wav(raw_audio_path, converted_wav_path)
# #     except Exception as e:
# #         return {"transcript": "", "response": f"Audio conversion failed: {str(e)}"}

# #     transcript = transcribe_wav(converted_wav_path)
# #     if not transcript.strip():
# #         return {"transcript": "", "response": "No speech detected."}

# #     reply = chat_with_ollama(transcript)
# #     return {"transcript": transcript, "response": reply}

# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import sys
# import os
# import uuid
# import json
# import wave
# import subprocess
# import ollama
# import vosk

# # --- App setup ---
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# MODEL_PATH = os.path.abspath("../vosk_model/vosk-model-small-en-us-0.15")
# AUDIO_DIR = "uploads"
# os.makedirs(AUDIO_DIR, exist_ok=True)

# try:
#     model = vosk.Model(MODEL_PATH)
# except Exception as e:
#     print(f"❌ Failed to load Vosk model from {MODEL_PATH}")
#     raise

# # Optional toggle for TTS
# ENABLE_TTS = True


# # --- Helpers ---
# def setup_tts():
#     import pyttsx3
#     if sys.platform == 'darwin':
#         import objc
#         import pyttsx3.drivers.nsss
#         pyttsx3.drivers.nsss.objc = objc
#     return pyttsx3


# def convert_to_mono_wav(source_path: str, output_path: str):
#     result = subprocess.run([
#         "ffmpeg", "-y",
#         "-i", source_path,
#         "-ac", "1",
#         "-ar", "16000",
#         "-sample_fmt", "s16",
#         output_path
#     ], capture_output=True)

#     if result.returncode != 0:
#         raise RuntimeError(f"FFmpeg conversion failed:\n{result.stderr.decode()}")


# def transcribe_wav(path):
#     wf = wave.open(path, "rb")
#     if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
#         raise ValueError("Audio must be mono WAV with 16kHz, 16-bit")

#     rec = vosk.KaldiRecognizer(model, wf.getframerate())
#     results = []
#     while True:
#         data = wf.readframes(4000)
#         if len(data) == 0:
#             break
#         if rec.AcceptWaveform(data):
#             results.append(json.loads(rec.Result())["text"])
#     results.append(json.loads(rec.FinalResult())["text"])
#     return " ".join([r for r in results if r.strip()])


# def speak_response(text):
#     if not ENABLE_TTS:
#         return
#     pyttsx3 = setup_tts()
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 175)
#     engine.say(text)
#     engine.runAndWait()


# def chat_with_ollama(text):
#     response = ollama.chat(
#         model="mistral",
#         messages=[
#             {"role": "system", "content": "You are Noa, a warm, succinct, and helpful relationship coach. Keep your answers short (1–2 sentences)."},
#             {"role": "user", "content": text}
#         ]
#     )
#     reply = response["message"]["content"]
#     print(f"🧠 Ollama's Response: {reply}")
#     speak_response(reply)
#     return reply


# # --- Endpoint ---
# @app.post("/api/speak")
# async def speak(file: UploadFile = File(...)):
#     original_filename = file.filename
#     base_filename = os.path.splitext(original_filename)[0]
#     safe_id = uuid.uuid4().hex
#     raw_audio_path = os.path.join(AUDIO_DIR, f"{safe_id}_{base_filename}.webm")
#     converted_wav_path = os.path.join(AUDIO_DIR, f"{safe_id}_{base_filename}.wav")

#     with open(raw_audio_path, "wb") as f:
#         f.write(await file.read())

#     try:
#         convert_to_mono_wav(raw_audio_path, converted_wav_path)
#     except Exception as e:
#         return {"transcript": "", "response": f"Audio conversion failed: {str(e)}"}

#     transcript = transcribe_wav(converted_wav_path)
#     if not transcript.strip():
#         return {"transcript": "", "response": "No speech detected."}

#     reply = chat_with_ollama(transcript)
#     return {"transcript": transcript, "response": reply}


from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

import sys
import os

# 🧠 Patch pyttsx3 NSSSpeechDriver with objc *before anything else*
if sys.platform == 'darwin':
    try:
        import objc
        import pyttsx3.drivers.nsss
        pyttsx3.drivers.nsss.objc = objc
    except ImportError as e:
        print("❌ pyobjc or pyttsx3 not installed correctly:", e)
        raise

import pyttsx3  # ✅ Safe to import now

import uuid
import json
import wave
import subprocess
import ollama
import vosk

# --- App setup ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.abspath("../vosk_model/vosk-model-small-en-us-0.15")
AUDIO_DIR = "uploads"
os.makedirs(AUDIO_DIR, exist_ok=True)

try:
    model = vosk.Model(MODEL_PATH)
except Exception as e:
    print(f"❌ Failed to load Vosk model from {MODEL_PATH}")
    raise

# Optional toggle for TTS
ENABLE_TTS = True


# --- Helpers ---
def convert_to_mono_wav(source_path: str, output_path: str):
    result = subprocess.run([
        "ffmpeg", "-y",
        "-i", source_path,
        "-ac", "1",
        "-ar", "16000",
        "-sample_fmt", "s16",
        output_path
    ], capture_output=True)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg conversion failed:\n{result.stderr.decode()}")


def transcribe_wav(path):
    wf = wave.open(path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("Audio must be mono WAV with 16kHz, 16-bit")

    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result())["text"])
    results.append(json.loads(rec.FinalResult())["text"])
    return " ".join([r for r in results if r.strip()])


def speak_response(text):
    if not ENABLE_TTS:
        return
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()


def chat_with_ollama(text):
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": "You are Noa, a warm, succinct, and helpful relationship coach. Keep your answers short (1–2 sentences)."},
            {"role": "user", "content": text}
        ]
    )
    reply = response["message"]["content"]
    print(f"🧠 Ollama's Response: {reply}")
    speak_response(reply)
    return reply


# --- Endpoint ---
@app.post("/api/speak")
async def speak(file: UploadFile = File(...)):
    original_filename = file.filename
    base_filename = os.path.splitext(original_filename)[0]
    safe_id = uuid.uuid4().hex
    raw_audio_path = os.path.join(AUDIO_DIR, f"{safe_id}_{base_filename}.webm")
    converted_wav_path = os.path.join(AUDIO_DIR, f"{safe_id}_{base_filename}.wav")

    with open(raw_audio_path, "wb") as f:
        f.write(await file.read())

    try:
        convert_to_mono_wav(raw_audio_path, converted_wav_path)
    except Exception as e:
        return {"transcript": "", "response": f"Audio conversion failed: {str(e)}"}

    transcript = transcribe_wav(converted_wav_path)
    if not transcript.strip():
        return {"transcript": "", "response": "No speech detected."}

    reply = chat_with_ollama(transcript)
    return {"transcript": transcript, "response": reply}
