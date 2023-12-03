import numpy as np
import struct
from pvrecorder import PvRecorder
import pyaudio
from vosk import Model, KaldiRecognizer
import pvporcupine
import os
import array


# Constants for pyaudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
READ_CHUNK = 512
PV_CHUNK_CONST = 512

GAIN = 5.0
# Constants for pvrecorder
KHADAS_USB_MIC_INDEX = 4
MAC_OS_MIC_INDEX = 0

current_dir = os.path.dirname(os.path.abspath(__file__))
PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY')
PORCUPINE_KEYWORD_FILE_PATH = os.path.join(current_dir, os.getenv('PORCUPINE_KEYWORD_FILE_PATH'))


def init_input_audio_device(use_pyaudio=True):
    if use_pyaudio:
        # Using pyaudio for recording
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=16000,
                            input=True,
                            frames_per_buffer=READ_CHUNK)
        return audio, stream
    else:
        # Using pvrecorder for recording
        recorder = PvRecorder(frame_length=PV_CHUNK_CONST, device_index=MAC_OS_MIC_INDEX)
        return recorder


def read_audio_frame(use_pyaudio=True, stream=None, recorder=None):
    try:
        if use_pyaudio:
            pcm_frames = stream.read(READ_CHUNK, exception_on_overflow=False)
            pcm_frames = np.frombuffer(pcm_frames, dtype=np.int16)
        else:
            pcm_frames = recorder.read()
            if isinstance(pcm_frames, list):
                pcm_frames = np.array(pcm_frames, dtype=np.int16)
            
        pcm_frames_float = pcm_frames.astype(float)
        pcm_frames_float = np.clip(pcm_frames_float * GAIN, -32768, 32767)
        pcm_frames = pcm_frames_float.astype(np.int16)
        
        return pcm_frames
    except Exception as e:
        print(f"Exception: {e}")
        raise e


def audio_recorder_thread(frame_queue, events, use_pyaudio=True):
    stream = None
    recorder = None
    audio = None

    porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keywords=['bumblebee'])

    if use_pyaudio:
        audio, stream = init_input_audio_device(use_pyaudio)
    else:
        recorder = init_input_audio_device(use_pyaudio)
        recorder.start()

    try:
        while True:
            pcm_frames = None
            pcm_frames = read_audio_frame(use_pyaudio, stream, recorder)
            if pcm_frames is not None:
                frame_queue.put(pcm_frames)

    except KeyboardInterrupt:
        print("Keyboard interrupt")

    finally:
        if use_pyaudio:
            print("stopping stream")
            stream.stop_stream()
            stream.close()
            audio.terminate()
        else:
            recorder.stop()
            recorder.delete()
