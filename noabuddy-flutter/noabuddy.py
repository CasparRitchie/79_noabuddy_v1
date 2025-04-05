import sys
import os
from pathlib import Path

# Add backend folder to path so we can import voice_agent
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.append(str(backend_path))

from "voice_agent" import list_audio_devices, get_response_from_audio

def main():
    print("🎧 NoaBuddy CLI – Voice-to-Text + Ollama\n")

    list_audio_devices()
    response = get_response_from_audio()

    print("\n🧠 NoaBuddy Response:\n")
    print(response)

if __name__ == "__main__":
    main()
