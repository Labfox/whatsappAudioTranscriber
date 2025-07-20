from whatsfly import WhatsApp
import time
import whisper
import pprint
import os

model = whisper.load_model("medium")

def my_event_callback(whatsapp, event_data):
    if event_data["eventType"] == "Message" and \
        "extendedTextMessage" in event_data["message"] and \
        event_data["message"]["extendedTextMessage"]["text"] == "Transcribe" and \
        "quotedMessage" in event_data["message"]["extendedTextMessage"]["contextInfo"] and \
        "audioMessage"  in event_data["message"]["extendedTextMessage"]["contextInfo"]["quotedMessage"]:

        returnAddress = event_data["info"]["messageSource"].split(" in ")[-1].split("@")[0]
        isGroup = (event_data["info"]["messageSource"].replace(" in ", "") != event_data["info"]["messageSource"])
        if os.path.exists("media/audios/"+event_data["message"]["extendedTextMessage"]["contextInfo"]["stanzaID"]+".oga"):
            whatsapp.sendMessage(returnAddress, "Transcribing your message. Please wait.", group=isGroup)
            transcription = model.transcribe("media/audios/"+event_data["message"]["extendedTextMessage"]["contextInfo"]["stanzaID"]+".oga")
            whatsapp.sendMessage(returnAddress, "Transcription: " + transcription["text"], group=isGroup)
            
        else: 
            whatsapp.sendMessage(returnAddress, "Sorry, message not found in cache", group=isGroup)

if __name__ == "__main__":

    whatsapp = WhatsApp(on_event=my_event_callback, media_path="media")

    whatsapp.connect()

    input("Loaded. Press enter to stop")

    whatsapp.disconnect()