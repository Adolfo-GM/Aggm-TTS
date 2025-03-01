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

    word_buffer = []
    for char in words_str:
        if char.isdigit():
            if word_buffer:
                word_file = ''.join(word_buffer) + ".wav"
                file_path = os.path.join(audio_dir, word_file)
                if os.path.exists(file_path):
                    play_audio(file_path)
                else:
                    print(f"Audio file for word '{word_file}' not found: {file_path}")
                word_buffer = []
            file_path = os.path.join(audio_dir, f"{char}.wav")
            if os.path.exists(file_path):
                play_audio(file_path)
            else:
                print(f"Audio file for '{char}' not found: {file_path}")
        elif char.isalpha():
            word_buffer.append(char)
        elif char.isspace():
            if word_buffer:
                word_file = ''.join(word_buffer) + ".wav"
                file_path = os.path.join(audio_dir, word_file)
                if os.path.exists(file_path):
                    play_audio(file_path)
                else:
                    print(f"Audio file for word '{word_file}' not found: {file_path}")
                word_buffer = []
        else:
            if word_buffer:
                word_file = ''.join(word_buffer) + ".wav"
                file_path = os.path.join(audio_dir, word_file)
                if os.path.exists(file_path):
                    play_audio(file_path)
                else:
                    print(f"Audio file for word '{word_file}' not found: {file_path}")
                word_buffer = []

aggmtts("sputtering of those who do no know hatred.")

