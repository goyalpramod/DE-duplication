import os
import time
from dotenv import load_dotenv, find_dotenv
from pinecone import Pinecone, PodSpec
load_dotenv(find_dotenv())

class InitialisePinecone():
    def __init__(self) -> None:
        self.pinecone_env = os.environ["PINECONE_ENV"]   
        self.pinecone_api_key = os.environ["PINECONE_API_KEY"]
        self.pc = Pinecone(api_key=self.pinecone_api_key,
             environment=self.pinecone_env)
        
    def make_index(self,index_name:str = "pod-index") -> None:
        existing_indexes = [
            index_info["name"] for index_info in self.pc.list_indexes()
        ]
        if index_name not in existing_indexes:
            # if does not exist, create index
            self.pc.create_index(
                name= index_name,
                dimension=1536,
                metric="cosine",
                spec=PodSpec(
                environment="gcp-starter"
                )
            )
            # wait for index to be initialized
            while not self.pc.describe_index(index_name).status['ready']:
                time.sleep(1)