from dotenv import load_dotenv
from openai import OpenAI 
import numpy as np

#given a string, embed the string as a vector
def embed_string(text):
    #load env and openai client
    load_dotenv() 
    client = OpenAI()
    # get response from embedding model
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    #return vector of length 1536
    return response.data[0].embedding








