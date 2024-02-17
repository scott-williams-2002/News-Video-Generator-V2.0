from text_to_speech.TTS_Wrapper import TTS_Wrapper

def generate_speech(script_data):
    #prompt user for a folder to store the audio files in
    dirname = str(input("Enter a directory to place the audio files into: ")) 

    #loop through text chunks
    for i in range(len(script_data)):
        current_script_chunk = script_data[i]['script_chunk'] #script's text to be made into speech
        #instantiate TTS
        tts = TTS_Wrapper()
        tts.set_audio_config()
        tts.set_voice()

        #generate speech and save as dirname
        tts.generate_speech(current_script_chunk)
        output_file_location = tts.write_to_file(file_name=f"audio{i}.mp3", directory_name=dirname)  #mp3 files are name sequentially
        print(f"Audio {i} written to: {output_file_location}")
              
        #save absolute path to data structure
        script_data[i]['audio'] = output_file_location
    
    #returns data structure with audio locations added
    return script_data



        

