import os
import pygame
from pathlib import Path
import logging
from time import sleep

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

pygame.mixer.init()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class TTSConfig:
    def __init__(self, audio_dir="audio", file_ext=".m4a", delay=0.1, generate_missing=False):
        self.audio_dir = Path(audio_dir)
        self.file_ext = file_ext
        self.delay = delay
        self.generate_missing = generate_missing and GTTS_AVAILABLE

def play_audio(file_path):
    file_path = Path(file_path)
    logger.info(f"Attempting to play: {file_path}")
    if not file_path.exists():
        logger.error(f"File does not exist: {file_path}")
        return False
    try:
        pygame.mixer.music.load(str(file_path))
        pygame.mixer.music.play()
        return True
    except pygame.error as e:
        logger.error(f"Error playing {file_path}: {e}")
        return False

def generate_audio(word, file_path):
    if not GTTS_AVAILABLE:
        logger.warning("gTTS not installed. Cannot generate audio.")
        return
    try:
        tts = gTTS(text=word, lang='en')
        tts.save(str(file_path))
        logger.info(f"Generated audio for '{word}' at {file_path}")
    except Exception as e:
        logger.error(f"Failed to generate audio for '{word}': {e}")

def aggmtts(words_str, config=None):
    config = config or TTSConfig()
    if not config.audio_dir.exists():
        logger.error(f"Audio directory '{config.audio_dir}' does not exist.")
        return
    if not config.audio_dir.is_dir():
        logger.error(f"'{config.audio_dir}' is not a directory.")
        return
    if not isinstance(words_str, str):
        logger.error("Input must be a string.")
        return
    words_str = ''.join(e for e in words_str if e.isalnum() or e.isspace()).lower()
    audio_queue = []
    word_buffer = []
    for char in words_str:
        if char.isdigit():
            if word_buffer:
                audio_queue.append(''.join(word_buffer))
                word_buffer = []
            audio_queue.append(char)
        elif char.isalpha():
            word_buffer.append(char)
        elif char.isspace() and word_buffer:
            audio_queue.append(''.join(word_buffer))
            word_buffer = []
    if word_buffer:
        audio_queue.append(''.join(word_buffer))
    for word in audio_queue:
        file_path = config.audio_dir / f"{word}{config.file_ext}"
        if not file_path.exists() and config.generate_missing:
            generate_audio(word, file_path)
        if file_path.exists():
            if play_audio(file_path):
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                sleep(config.delay)
        else:
            logger.warning(f"Audio file for '{word}' not found: {file_path}")

def speak(text):
    config = TTSConfig(
        audio_dir="audio",
        file_ext=".m4a",
        delay=0.2,
        generate_missing=GTTS_AVAILABLE
    )
    logger.info("Starting text-to-speech conversion...")
    aggmtts(text, config)
    logger.info("Text-to-speech conversion completed.")

if __name__ == "__main__":
    speak("hello, how can I help?")