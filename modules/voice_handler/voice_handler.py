import pvrhino
import os
from dotenv import load_dotenv
import struct
import numpy as np
import pygame
import time
from vosk import Model, KaldiRecognizer

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY')
RHINO_MODEL_FILE_PATH = os.path.join(current_dir, os.getenv('RHINO_MODEL_FILE_PATH'))
ACTIVE_DIALOG_SESSION_TIME = 10  # seconds

def voice_handler_thread(frame_queue, events=None):
    rhino = pvrhino.create(
        access_key=PORCUPINE_ACCESS_KEY,
        context_path=RHINO_MODEL_FILE_PATH
    )
    vosk_model = Model(lang="en-us")
    recognizer = KaldiRecognizer(vosk_model, 16000)

    intent_in_process = False
    recognized_text = ""
    try:
        start_time = 0
        while True:
            if not intent_in_process:
                events['wake_word_event'].wait()
                events['wake_word_event'].clear()
                intent_in_process = True
                recognized_text = ""  # Reset recognized text
                print("Wakeword activated, listening for intent...")
                start_time = time.time()  # Start the timer

            if time.time() - start_time > ACTIVE_DIALOG_SESSION_TIME:
                if recognized_text:  # If there is recognized text
                    print(recognized_text)  # Process the text with ChatGPT
                intent_in_process = False
                events['intent_ready_event'].set()
                continue

            # Read audio frame from the recorder
            pcm = frame_queue.get()
            pcm_bytes = pcm.tobytes()  # Convert numpy array to bytes

            if recognizer.AcceptWaveform(pcm_bytes):
                result = recognizer.Result()
                recognized_text += result

            # Process the audio frame with Porcupine
            is_finalized = rhino.process(pcm)
            if is_finalized:
                # get inference if is_finalized is true
                inference = rhino.get_inference()
                if inference.is_understood:
                    process_intent(inference.intent, inference.slots, events)
                    intent_in_process = False
                    events['intent_ready_event'].set()

    except KeyboardInterrupt:
        print("Stopping")


def process_intent(intent, slots, events):
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