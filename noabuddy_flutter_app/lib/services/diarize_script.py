import os
import whisperx
import torch
import sys
from dotenv import load_dotenv
import pandas as pd

# Load .env for Hugging Face token
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Set device and model
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "large-v2"

print("⏬ Loading WhisperX model...")
model = whisperx.load_model(MODEL_NAME, device=DEVICE, compute_type="float32")


def diarize_and_transcribe(file_path):
    file_path = os.path.abspath(file_path)
    print(f"\n📁 Using audio file: {file_path}\n")

    # Step 1: Transcribe
    raw_transcript = model.transcribe(file_path)
    print("📝 raw_transcript keys:", raw_transcript.keys())
    print("📝 raw_transcript['segments'] example:", raw_transcript.get("segments", [])[0] if raw_transcript.get("segments") else "❌ No segments found")

    # Step 2: Align words
    model_a, metadata = whisperx.load_align_model(language_code=raw_transcript["language"], device=DEVICE)
    aligned_result = whisperx.align(raw_transcript["segments"], model_a, metadata, file_path, device=DEVICE)
    print("📌 aligned_result keys:", aligned_result.keys())
    print("📌 aligned_result['word_segments'] sample:", aligned_result.get("word_segments", [])[0] if aligned_result.get("word_segments") else "❌ No word_segments")

    # Step 3: Diarize
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device=DEVICE)
    diarize_segments = diarize_model(file_path)
    print(f"🔈 diarize_segments:\n{diarize_segments[:1]}")

    try:
        word_segments_df = pd.DataFrame(aligned_result["word_segments"])
        print("📄 word_segments_df columns:", word_segments_df.columns)

        result_with_speakers = whisperx.assign_word_speakers(
            word_segments_df,  # <- direct DataFrame
            diarize_segments
        )

        print("🗣️ Result with speakers columns:", result_with_speakers.columns)
        print("🗣️ First few rows:\n", result_with_speakers.head())

    except Exception as e:
        print("❌ Error in assign_word_speakers:", e)
        return []

    # Format the messages
    messages = []
    for row in result_with_speakers.itertuples():
        speaker = getattr(row, "speaker", "Unknown")
        word = getattr(row, "word", "")
        messages.append({"speaker": speaker, "text": word.strip()})

    return messages


if __name__ == "__main__":
    file = sys.argv[1]
    messages = diarize_and_transcribe(file)
    for msg in messages:
        print(f"{msg['speaker']}: {msg['text']}")
