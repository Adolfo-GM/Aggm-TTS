import os
import whisper
from pydub import AudioSegment
import re

os.makedirs('audio', exist_ok=True)

audio_file = 'voice_audio.mp4'
audio = AudioSegment.from_file(audio_file)

model = whisper.load_model("small")
result = model.transcribe(audio_file, word_timestamps=True)

def clean_filename(word):
    return re.sub(r'[^a-zA-Z0-9]', '', word)

for segment in result['segments']:
    for word in segment['words']:
        word_text = word['word'].strip()
        start = int(word['start'] * 1000)
        end = int(word['end'] * 1000)
        word_audio = audio[start:end]
        safe_filename = clean_filename(word_text)
        word_audio.export(f"audio/{safe_filename}.wav", format="wav")
