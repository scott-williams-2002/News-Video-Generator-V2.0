from openai import OpenAI
from dotenv import load_dotenv

#class to filter relevant and irrelevant images to a string of text
class Image_Filter:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def filter_image(self, img_url, text):
        #asks for a yes or no if image is related to text
        try:    
            response = self.client.chat.completions.create(
              model="gpt-4-vision-preview",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {"type": "text", "text": f"Respond by saying either yes or no. Is this image related to this piece of text in any way: {text}?"},
                    {
                      "type": "image_url",
                      "image_url": {
                        "url": img_url,
                      },
                    },
                  ],
                }
              ],
              max_tokens=1,
            )

            if "y" in str(response.choices[0]).lower():
                return True
            else:
                return False
        #if error with model or image url return false cause not accessible
        except:
            print(f"error analyzing the image: {img_url}") #alert which image threw an error
            return False

