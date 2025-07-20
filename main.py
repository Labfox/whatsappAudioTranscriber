# Whatsapp Audio Transcriber - A simple bot to transcribe vocal messages
# Copyright (C) 2025 Labfox

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

from whatsfly import WhatsApp
import time
import whisper
import pprint
import os

model = whisper.load_model("medium") # possible options: base, medium, large

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