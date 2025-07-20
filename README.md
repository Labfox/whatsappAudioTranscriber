# WhatsApp Audio Transcriber

A bot for WhatsApp that listens for audio messages and transcribe them if you ask.

Only ~30 LOC, so easily verifiable.

Based on my version of the [whatsfly](https://github.com/Labfox/whatsfly) library and OpenAI's [Whisper](https://github.com/openai/whisper).

## Dependencies

If running on Windows, you'll need to have ffmpeg. Every other dependency is listed in the requirements.txt.

You can change the whisper model by changing line 7 in main.py: 
```python
model = whisper.load_model("medium") # possible options: base, medium, large
```

## How to use

First, install the dependencies:

```shell
pip install -r requirements.txt
```

After, launch the bot: 

```shell
python3 main.py
```

The program will start by downloading the WhatsApp-enabling binary (or building it if you have Go installed locally), which is around 6 MB. Then it will download the Whisper model (about 1.4 GB, unless you've chosen a different one). After that, a QR code will be displayed; scan it using the Linked Devices section in WhatsApp *(Open WhatsApp → Menu → Linked Devices → Link a Device → Scan QR code)*. Once linked, the program will download your message history. When WhatsApp indicates that the device has finished syncing, all new incoming messages will be downloaded (text to ```whatsapp/wapp.db```, media to ```media/```), and the bot will begin listening for new messages.