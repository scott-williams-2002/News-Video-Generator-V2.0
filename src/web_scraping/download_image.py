import requests
import os
from PIL import Image
import io
from image_filtering.Image_Filter import Image_Filter

#downloads image to a file path location and returns true if sucessful and false if not
def download_image(url, file_path):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)

        # Check if the image can be identified and is in a compatible format
        if image.format not in ["JPEG", "PNG"]:
            print(f"Skipping image with unsupported format: {url}")
            return False

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        return True
    except Exception as e:
        return False


# takes in the list of dictionaries with video segment data and appends image file locations based on where the images are stored. 
def validate_and_download_images(video_data):
    #prompts user for directory name and then saves image in that directory
    dirname = str(input("Enter a directory to place the image files into: ")) 
    new_dir_path = os.path.abspath(dirname)
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    
    #instantiate image filter moduel
    img_filter = Image_Filter()
    #loops through image url list for each dictionary
    img_counter = 0
    for vid_chunk in video_data:
        vid_chunk['image_location'] = []
        for url in vid_chunk['images']:
            #adds file name to path
            full_path = os.path.join(new_dir_path,f"img{img_counter}.jpg")

            # if vision module returns true (meaning image is relevant to text) download and store file path
            if img_filter.filter_image(url,vid_chunk['script_chunk']):
                if download_image(url, full_path):
                    img_counter += 1
                    vid_chunk['image_location'].append(full_path)
    
    #after appending image paths to data structure, return list of dicts
    return video_data

# returns true if image is corrupted and false if not
def is_image_corrupted(image_path):
    try:
        # Attempt to open the image
        with Image.open(image_path) as img:
            # Check if the image can be loaded
            img.load()
            return False  # Image is not corrupted
    except Exception as e:
        # An error occurred while trying to open the image, indicating corruption
        print(f"Error: {e}")
        return True  # Image is corrupted


                



