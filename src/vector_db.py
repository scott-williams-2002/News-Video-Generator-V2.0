import numpy as np
from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec
import time

from web_scraping.embed import embed_string



class Vector_DB:
    def __init__(self):
        load_dotenv()
        self.index_name = "video-db"

        #check correct database
        correct_db = str(input(f"Is {self.index_name} the correct index? (Yy/Nn): "))
        if(correct_db.lower() == "n"):
            self.index_name = str(input("Enter the correct index_name: "))

        #set api key, dimensions, and serverless specs
        self.pc = Pinecone(api_key= os.getenv("PINECONE_API_KEY"))
        self.vector_dimension = 1536
        self.spec = spec = ServerlessSpec(cloud="aws", region="us-west-2")
    
    def create_database(self):
        #create index if does not exist already
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                self.index_name,
                dimension=self.vector_dimension,  # dimensionality of text-embed-3-small
                metric='dotproduct',
                spec=self.spec
            )

        #sleep while waiting for db to be set up
        while not self.pc.describe_index(self.index_name).status['ready']:
            time.sleep(1)
        
        # set current index to created index
        self.index = self.pc.Index(self.index_name)
        time.sleep(1)

    def populate(self, value, id, article_text, article_source, article_url):
        #formats and inserts values into the vector db
        try:
            self.index.upsert(vectors=[{"id": str(id), "values": value, "metadata": {"text":str(article_text), "source": str(article_source), "url": str(article_url)}}])
        except:
            print(f"Alert ->>>>>> There was an error upserting the following data: {article_text}")

    #given a passed in vector embedding, return the k nearest vectors
    def make_query(self, query_vector, k):
        try:
            #returns a json of results if possible
            res = self.index.query(vector= query_vector, top_k=k, include_metadata=True)
            return res
        except:
            print(f"Alert ->>>>>> There was an error when making a query with a k of {k}")
            return {"nul":"nul"} #returns a json of nul values if there is an issues

    