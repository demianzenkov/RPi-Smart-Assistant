# main.py
import sys
import os
from dotenv import load_dotenv
from collections import deque
import threading
from threading import Event, Thread
from queue import Queue

# Path to the modules directory
examples_dir = os.path.dirname(os.path.dirname(__file__))
root_dir = os.path.join(examples_dir, "..")
modules_dir = os.path.join(root_dir, "modules")
sensors_dir = os.path.join(root_dir, "sensors")
sys.path.append(modules_dir)
sys.path.append(sensors_dir)


# Import spotter_thread from the spotter module
from spotter import spotter
from video_capture import capture
from telegram_bot import bot
from gps_serial import nmea
from audio_recorder import recorder
from voice_handler import voice_handler


# Main function or other logic
def main():
    flask_thread = Thread(target=bot.run_flask_app)
    flask_thread.start()

    frame_buffer = deque()
    audio_queue = Queue()

    wake_word_event = Event()
    intent_ready_event = Event()
    capture_photo_event = Event()  # Updated key name
    capture_video_event = Event()
    send_video_event = Event()
    send_photo_event = Event()
    save_location_event = Event()

    events = {
        'wake_word_event': wake_word_event,
        'intent_ready_event': intent_ready_event,
        'capture_photo_event': capture_photo_event,  # Updated key name
        'capture_video_event': capture_video_event,
        'send_video_event': send_video_event,
        'send_photo_event': send_photo_event,
        'save_location_event': save_location_event,
    }

    recorder_thread = Thread(target=recorder.audio_recorder_thread, args=(audio_queue, events, True))
    voice_handler_thread = Thread(target=voice_handler.voice_handler_thread, args=(audio_queue, events, ))
    video_capture_thread = threading.Thread(target=capture.video_capture_thread, args=(frame_buffer, events))
    spotter_thread = threading.Thread(target=spotter.spotter_thread, args=(audio_queue, events, ))
    gps_thread = threading.Thread(target=nmea.read_gps_data, args=(events, ))

    recorder_thread.start()
    video_capture_thread.start()
    spotter_thread.start()
    voice_handler_thread.start()
    gps_thread.start()
    bot.start_telegram_bot(events)


if __name__ == "__main__":
    main()
