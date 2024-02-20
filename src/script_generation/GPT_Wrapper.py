from dotenv import load_dotenv
import os
from openai import OpenAI
import json

class GPT_Wrapper:
    def __init__(self):
        load_dotenv() 
        self.client = OpenAI() #key in .env has name OPENAI_API_KEY, so no need to specify key in api call
    def model_call_text(self, prompt, temp, model_choice="gpt-3.5-turbo-0125", max_token=70):
        response = self.client.chat.completions.create(
            model=model_choice,
            response_format={ "type": "text" },
            temperature = temp,
            messages=prompt,
            max_tokens = max_token
        )
        return response.choices[0].message.content

    # given a prompt message and temp, return all json output from model
    def model_call_json(self, prompt, temp):
        try:
            response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            temperature = temp,
            messages=prompt,
            max_tokens = 50,
            )
            return json.loads((response.choices[0].message.content))
        except:
            print(f"error with this prompt:{prompt}")
            return " "
