# RPi Smart Assistant 

Welcome to RPi Smart Assistant, a voice assistant SDK designed for embedded systems and beyond. This Python-based toolkit enables seamless integration of advanced voice recognition and processing capabilities into your projects. Whether you're building a smart home device, an interactive kiosk, or experimenting with AI, RPi Smart Assistant offers a versatile and powerful solution. 

Key Features: 

- Wake-word detection with Porcupine
- Speech-to-intent processing using Rhino
- Offline text-to-speech capabilities with Vosk
- Advanced conversational AI with ChatGPT integration


### Supported Languages

​	Our current stack depends on Picovoice and OpenAI languages. Combining these two we can fully support smart assaistant scenario on these languages: English, Arabic, Dutch, Farsi, French, German, Hindi, Italian, Japanese, Korean, Mandarin, Polish, Portuguese, Russian, Spanish, Swedish, and Vietnamese

### Telegram Bot

Telegram API is used to interact with clients, send collected data from sensors and handling user-scenarion callbacks.

### Configuring the Environment 

To get started with RPi Smart Assistant, follow these steps: 

1. Clone the repository:

   ```bash
   git clone https://github.com/demianzenkov/RPi-Smart-Assistant.git
   ```

2. Install the required dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

### Preparing Wake Word and Intent Models

1. **Wake Word Model (Porcupine):**
   - Visit [Picovoice Console](https://console.picovoice.ai/) to create and download your wake word model.
   - Place the model file in the `models/wake_word/` directory.
2. **Intent Model (Rhino):**
   - Generate your intent model using the Picovoice Console.
   - Save the model into the `modules/spotter` folder

### Integrating ChatGPT

To integrate ChatGPT:

1. Obtain an API key from OpenAI.
2. Set the API key in your environment variables or configuration file.
3. Use the `modules/chatgpt/chat.py` module to interface with ChatGPT.

### Introduction to Hardware

As part of our ongoing commitment to enhance and evolve the RPi Smart Assistant, we are excited to announce our plans to develop a range of custom Raspberry Pi hats. These hardware extensions are designed to seamlessly integrate with your Raspberry Pi, bringing a new dimension of functionality and interactivity to your smart assistant projects. 

#### Suported sensors:

- NMEA GPS receiver, serial connection

#### Upcoming Hardware Modules

1. **Microphone Array Hat**:
    - High-quality audio capture for clear voice recognition.   
    - Advanced noise cancellation for use in various environments. 
2. **GPS Navigation Hat**:
   - Precise location tracking for location-based services. 
   - Integration with mapping and geospatial applications. 
3.  **Smart Home Sensor Hat**:
   - A suite of sensors for monitoring temperature, humidity, light, and more. 
   - Enable your assistant to interact with and control smart home devices. 

### Work in progress

- Self-hosted speech-to-intent engine
- Spotter model trainer
- NLP models web configurator
- Wide range of sensors support

### Contributing to RPi Smart Assistant 

We welcome contributions! If you'd like to help improve RPi Smart Assistant, please follow these steps: 

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear, descriptive messages.
4. Push the branch and open a pull request.

### Contact Us 

For support, feedback, or collaboration, feel free to reach out to us: 

- Email: [demianzenkov@gmail.com](mailto:demianzenkov@gmail.com)
- Discord: [Join our community](https://discord.gg/XEEKEUyc)
