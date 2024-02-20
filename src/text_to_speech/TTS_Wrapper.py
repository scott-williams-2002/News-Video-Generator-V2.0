from google.cloud import texttospeech
from dotenv import load_dotenv
import os

class TTS_Wrapper:
    def __init__(self):
        load_dotenv()
        self.client = texttospeech.TextToSpeechClient()
        
    #defaults to certain voice, pitch, and tone but can be changed when called
    def set_audio_config(self, audio_encoding=texttospeech.AudioEncoding.MP3, pitch = -4.0, speaking_rate=1.2, effects_profile_id = ["handset-class-device"]):
        self.audio_encoding = texttospeech.AudioConfig(audio_encoding=audio_encoding, pitch = pitch, speaking_rate=speaking_rate, effects_profile_id = effects_profile_id)

    def set_voice(self, language_code="en-AU", voice_name="en-AU-Polyglot-1"):
        self.voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)

    def generate_speech(self, input_text):
        synthesis_input = texttospeech.SynthesisInput(text=input_text) #correct input data structure
        self.current_response = self.client.synthesize_speech(input=synthesis_input, voice=self.voice, audio_config=self.audio_encoding)
    
    #writes to output_audio_files folder in source directory
    def write_to_file(self, file_name="output.mp3", directory_name="output_audio"):
        #get output directory path and create directory if doesn't exist already
        new_dir_path = os.path.abspath(directory_name)
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)

        #checks if filename already in use and prompts overwrite or rename option
        file_name_path = os.path.join(new_dir_path, file_name)
        if os.path.exists(file_name_path):
            print(f"A file called {file_name} already exists")
            delete_file = input(f"Do you wish to overwrite {file_name} (y/n): ")
            # if user says yes delete old file
            if delete_file.lower() == "y":
                os.remove(file_name_path)
            #if user doesn't say yes ask for new file name
            else:
                new_file_name = input("Enter a new mp3 file name to write to: ")
                file_name_path = os.path.join(new_dir_path, new_file_name)

        #writes to file with specified criteria
        with open(file_name_path, "wb") as out:
            out.write(self.current_response.audio_content)
            print(f"Audio content written to '{file_name_path}'")

        return file_name_path #to place in script data to access files later
        





  
