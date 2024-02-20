import moviepy.editor as mp
from moviepy.video.fx.resize import resize
#from pytube import YouTube


# creates a video object and saves it in an mp4
class Video_Editor:
    #sets the class member variables such as the list of audio files and video elements
    def __init__(self, video_file, duration):
        self.movie_clip = mp.VideoFileClip(video_file).subclip(0,duration).set_position(("bottom"))
        self.background = mp.ColorClip(size=(self.movie_clip.w, int(self.movie_clip.w * (16/9))), color=(0,0,0), duration=duration)
        self.video_elements = [self.background, self.movie_clip]
        self.audio_elements = []
    
    #column layout of images with top inserted in this function
    def add_top_image(self, image_file_location, start_time, duration, position=("center","top")):
        img = mp.ImageClip(image_file_location).set_start(start_time).set_duration(duration).margin(top=150, opacity=0).set_pos(position)
        img = resize(img,width=(0.7 * self.movie_clip.w))
        self.video_elements.append(img)

    #column layout of images with bottom inserted in this function
    def add_bottom_image(self, image_file_location, start_time, duration, position=("center","center")):
        img = mp.ImageClip(image_file_location).set_start(start_time).set_duration(duration).set_pos(position)
        img = resize(img,width=(0.7 * self.movie_clip.w))
        self.video_elements.append(img)

    #adds the text for the channel name at top center of screen
    def add_top_text(self, text_content, video_length):
        txt = mp.TextClip(text_content,font='Ariel', fontsize = 150, color = 'white', method="label").set_duration(video_length).margin(top=30,opacity=0).set_pos(("center","top"))
        self.video_elements.append(txt)

    # adds an audio file to list of audio
    def add_audio(self, audio_file_location, total_audio):
        audioclip = mp.AudioFileClip(audio_file_location).set_start(total_audio)
        self.audio_elements.append(audioclip)
        
    # concatenates all video elements and audio files
    def create_video(self):
        self.video = mp.CompositeVideoClip(self.video_elements)
        self.video.audio = mp.CompositeAudioClip(self.audio_elements)
    #writes to a specified mp4 file (this takes a very long time so ultrafast is used to be less spatially efficient. can be resized in clipchamp)
    def write_to_file(self, out_file_name):
        if out_file_name[len(out_file_name)-4:len(out_file_name)] != ".mp4":   
            out_file_name += ".mp4"
        self.video.write_videofile(out_file_name, threads=6, preset='ultrafast', logger='bar')

    

