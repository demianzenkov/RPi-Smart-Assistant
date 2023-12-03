# RPi Smart Assistant 

Simple and fully functional voice assistant SDK for embedded (and other) platforms. Written fully in Python it allows you to cover full assistant interaction scenario: wake-word recognition, speech-to-intent processing and voice chatting with the most advanced language model - OpenAI GPT. 

#### NLP libraries used in project:

- Wake Word
  - Porcupine (Picovoice): commercial, offline, requires generated model
- Text-To-Intent
  - Rhino (Picovoice): commercial, offline, requires generated model
- Text-To-Speech
  - Vosk Speech Recognition Toolkit: open-source, offline, requires downloaded model (or downloads itself)
- Chat
  - ChatGPT (OpenAI-API)

#### Supported Languages

​	Our current stack depends on Picovoice and OpenAI languages. Combining these two we can fully support smart assaistant scenario on these languages: English, Arabic, Dutch, Farsi, French, German, Hindi, Italian, Japanese, Korean, Mandarin, Polish, Portuguese, Russian, Spanish, Swedish, and Vietnamese

#### Telegram Bot

Telegram API is used to interact with clients, send collected data from sensors and handling user-scenarion callbacks.

#### Suported sensors:

- NMEA GPS receiver, serial connection

###### 

### Configuring enviroment

### Preparing Wake Word model

### Preparing Intent model

### Integrating ChatGPT



##### <u>Work in progress:</u>

- Self-hosted speech-to-intent engine
- Spotter model trainer
- NLP models web configurator
- Wide range of sensors support

[Discord](https://discord.gg/XEEKEUyc)

