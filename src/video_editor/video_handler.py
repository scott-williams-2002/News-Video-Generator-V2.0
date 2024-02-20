from video_editor.Video_Editor import Video_Editor
from mutagen.mp3 import MP3

#returns the length of one audio file
def audio_len(audio):
    aud = MP3(audio)
    return aud.info.length

#given a list of audio files, returns the total combined length of the files
def get_audio_length_total(audio_files):
    total_len = 0
    for audio_file in audio_files:
        total_len += audio_len(audio_file)
    return total_len

#returns a list of all the audio file locations
def audio_to_list(video_data):
    out_list = []
    for vid_dict in video_data:
        out_list.append(vid_dict['audio'])
    return out_list




# given video data and a background video file (minecraft parkour, gta gameplay, movie footage) creates an mp4 file based on video data passed in
# such as images and audio from tts model
def load_video_data_and_create(video_data, background_video_file):
    # get list of audio files and total length
    audio_list = audio_to_list(video_data=video_data)
    audio_length_total = get_audio_length_total(audio_list)
    
    #instantiate video editor class
    vid = Video_Editor(background_video_file, duration=audio_length_total)

    #total length of audio added to avoid placing images on top of eachother (sort of like absolute image start time )
    audio_added_len = 0
    # sequentially add audio and their corresponding images
    for segment in video_data:
        # add audio file location to video
        audio_file_loc = segment['audio']
        vid.add_audio(audio_file_location=audio_file_loc)
        audio_length = audio_len(audio_file_loc) #audio file time

        images = segment['image_location']
        images_per_screen = 2
        image_time_ratio = (len(images) % images_per_screen) + (len(images) // images_per_screen) #percentage of audio time image should be displayed by. 
        image_time_increment = audio_length / image_time_ratio # length each screen of images should be displayed for 

        #even number of images case
        if len(images) % 2 == 0:
            image_counter = 0
            for i in range(0,len(images),2): #increments on even (0th is even) indices only to avoid out of bounds
                vid.add_top_image(images[i],start_time=((image_time_increment * image_counter) + audio_added_len), duration=image_time_increment)
                vid.add_bottom_image(images[i+1],start_time=((image_time_increment * image_counter) + audio_added_len), duration=image_time_increment)
                image_counter += 1

        #odd number of images case
        else:
            image_counter = 0
            for i in range(0,len(images),2): #increments on even (0th is even) indices only to avoid out of bounds
                if (i+1) == len(images):
                    vid.add_bottom_image(images[i],start_time=((image_time_increment * image_counter) + audio_added_len), duration=image_time_increment, position=("center","center"))
                else:
                    vid.add_top_image(images[i],start_time=((image_time_increment * image_counter) + audio_added_len), duration=image_time_increment)
                    vid.add_bottom_image(images[i+1],start_time=((image_time_increment * image_counter) + audio_added_len), duration=image_time_increment)
                image_counter += 1
        
        audio_added_len += audio_length # add the time of audio just added to total time of audio added


    #now finish configuring video
    vid.add_top_text("World News Daily", video_length=audio_length_total)
    vid.create_video()
    vid.write_to_file("iran1")

