# rhino.py
import pvrhino
import os
from dotenv import load_dotenv
import struct
import numpy as np
import pygame

load_dotenv()

speech_to_intent_dir = os.path.dirname(os.path.abspath(__file__))
PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY')
RHINO_MODEL_FILE_PATH = os.path.join(speech_to_intent_dir, os.getenv('RHINO_MODEL_FILE_PATH'))


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


def rhino_thread(frame_queue, events=None):
    rhino = pvrhino.create(
        access_key=PORCUPINE_ACCESS_KEY,
        context_path=RHINO_MODEL_FILE_PATH
    )

    intent_in_process = False

    try:
        while True:
            if intent_in_process is not True:
                events['wake_word_event'].wait()
                events['wake_word_event'].clear()
                intent_in_process = True
                print("Wakeword activated, listening for intent...")

            # Read audio frame from the recorder
            pcm = frame_queue.get()

            # Process the audio frame with Porcupine
            is_finalized = rhino.process(pcm)

            if is_finalized:
                # get inference if is_finalized is true
                inference = rhino.get_inference()
                if inference.is_understood:
                    audio_play_sound()
                    # use intent and slots if inference was understood
                    intent = inference.intent
                    slots = inference.slots
                    # print(intent)
                    if intent == 'saveMedia':
                        if slots['media'] == 'video':
                            print("save video intent recognised. setting capture_video_event")
                            events['capture_video_event'].set()
                        elif slots['media'] == 'photo':
                            print("save photo intent recognised. setting capture_photo_event")
                            events['capture_photo_event'].set()
                    elif intent == 'saveLocation':
                        events['save_location_event'].set()
                        print("save location")
                    elif intent == 'saveMediaAndLocation':
                        events['save_location_event'].set()
                        if slots['media'] == 'video':
                            print("save video intent recognised. setting capture_video_event")
                            events['capture_video_event'].set()
                        elif slots['media'] == 'photo':
                            print("save photo intent recognised. setting capture_photo_event")
                            events['capture_photo_event'].set()
                        print("save media and location")

                    intent_in_process = False
                    events['intent_ready_event'].set()

    except KeyboardInterrupt:
        print("Stopping")

    finally:
        # Clean up resources
        rhino.delete()


