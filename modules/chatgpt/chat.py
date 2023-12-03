# chat.py
from vosk import Model, KaldiRecognizer
import os
import pygame
import openai
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def audio_init():
    pygame.mixer.init()


def audio_load_sound(sound_path):
    pygame.mixer.music.load(sound_path)


def audio_play_sound():
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for audio to finish playing
        pygame.time.Clock().tick(10)


def process_with_chatgpt(messages):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )
    print(completion.choices[0].message)
    return completion.choices[0].message


def process_response_tts(message):
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=message.content,
    )
    response.stream_to_file("output.mp3")
    response.stream_to_file(os.path.join(CURRENT_DIR, "output.mp3"))


def init_voice_recognizer(sample_rate):
    vosk_model = Model(lang="en-us")
    recognizer = KaldiRecognizer(vosk_model, sample_rate)
    return recognizer, vosk_model


def process_voice_recognition(recognizer, pcm):
    if recognizer.AcceptWaveform(pcm):
        result = recognizer.Result()
        print(result)
        return result
    else:
        return None


if __name__ == "__main__":
    msgs = [
        {"role": "user",
         "content": "Hello how are you?"}
    ]
    answer = process_with_chatgpt(msgs)

    process_response_tts(answer)

    audio_init()
    audio_load_sound(os.path.join(CURRENT_DIR, "output.mp3"))
    audio_play_sound()

