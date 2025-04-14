from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uuid
import json
import wave
import subprocess
import ollama
import vosk
import sys
import os

# --- Optional pyttsx3 for local TTS ---
tts_engine = None
try:
    if os.getenv("HEROKU_DEPLOYED") != "true":
        import pyttsx3
        if sys.platform == 'darwin':
            try:
                import objc
                import pyttsx3.drivers.nsss
                pyttsx3.drivers.nsss.objc = objc
            except ImportError as e:
                print("❌ pyobjc or pyttsx3 not installed correctly:", e)
                raise
        tts_engine = pyttsx3.init()
except ImportError:
    print("⚠️ pyttsx3 not available — skipping local TTS.")



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
    if not tts_engine:
        return
    tts_engine.setProperty('rate', 175)
    tts_engine.say(text)
    tts_engine.runAndWait()



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
