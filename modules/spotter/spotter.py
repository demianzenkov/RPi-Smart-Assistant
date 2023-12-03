# spotter.py
import pvporcupine
from pvrecorder import PvRecorder
import os
from dotenv import load_dotenv
import struct
import numpy as np
import pygame

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY')
PORCUPINE_KEYWORD_FILE_PATH = os.path.join(current_dir, os.getenv('PORCUPINE_KEYWORD_FILE_PATH'))


def find_audio_file(audio_filename):
    dir_of_this_script = os.path.dirname(os.path.abspath(__file__))
    path_to_audio_file = os.path.join(dir_of_this_script, 'audio', audio_filename)
    return path_to_audio_file


def audio_init():
    pygame.mixer.init()


def audio_load_sound(sound_path):
    pygame.mixer.music.load(sound_path)


def audio_play_sound():
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for audio to finish playing
        pygame.time.Clock().tick(10)


def spotter_thread(frame_queue, events=None):
    # audio_init()
    # audio_load_sound(find_audio_file('notification-sound.mp3'))

    # porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keyword_paths=[PORCUPINE_KEYWORD_FILE_PATH])
    porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keywords=['bumblebee'])

    print(f"Listening for wake word, sample_rate: {porcupine.sample_rate}")
    try:
        while True:
            # Read audio frame from the recorder
            pcm = frame_queue.get()

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                # audio_file_path = find_audio_file('magic-sound.mp3')
                # audio_play_sound()
                if events:
                    events['wake_word_event'].set()  # Signal that the wake word was detected
                    events['intent_ready_event'].wait()
                    events['intent_ready_event'].clear()
                print("start listening for wake word again...")
                # Handle wake word detection (e.g., activate voice assistant)

    except KeyboardInterrupt:
        print("Stopping")

    finally:
        # Clean up resources
        porcupine.delete()

