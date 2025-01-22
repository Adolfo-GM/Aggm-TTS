import os
import wave
import pyaudio

def play_audio(file_path):
    with wave.open(file_path, 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        stream.stop_stream()
        stream.close()
        p.terminate()

def aggmtts(words_str):
    audio_dir = "audio"
    words_str = ''.join(e for e in words_str if e.isalnum() or e.isspace()).lower()

    for char in words_str:
        if char.isdigit():  
            file_path = os.path.join(audio_dir, f"{char}.wav")
            if os.path.exists(file_path):
                play_audio(file_path)
            else:
                print(f"Audio file for '{char}' not found: {file_path}")
        elif char.isalpha():
            file_path = os.path.join(audio_dir, f"{char}.wav")
            if os.path.exists(file_path):
                play_audio(file_path)
            else:
                print(f"Audio file for '{char}' not found: {file_path}")
        elif char.isspace():
            continue
        else:
            print(f"Invalid character ignored: {char}")

aggmtts("!123")
