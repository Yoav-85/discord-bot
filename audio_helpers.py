import os

import speech_recognition as sr
from pydub import AudioSegment

recognizer = sr.Recognizer()


def is_supported_audio_extension(filename: str) -> bool:
    return filename.endswith((".wav", ".mp3", ".m4a", ".ogg"))


# Convert audio file to text
def audio_to_text(file_path: str) -> str:
    # Convert to WAV if not already in that format
    if not file_path.endswith(".wav"):
        current_path = os.path.abspath(os.getcwd())
        file_full_path = os.path.join(current_path, file_path)
        audio = AudioSegment.from_file(file_full_path)
        file_path = "converted_audio.wav"
        audio.export(file_path, format="wav")

    # Use SpeechRecognition to transcribe audio
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Use Google Web Speech API for transcription
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition; {e}"
