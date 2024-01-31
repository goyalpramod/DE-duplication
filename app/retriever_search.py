from langchain_community.vectorstores import Pinecone as PineconeVectorstore
from langchain_openai import OpenAIEmbeddings
from typing import List, Tuple
from langchain_core.documents.base import Document
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def retrieve_relevant_docs(query:str) -> List[Tuple[Document, float]]:
    """
    :param: str
    :return: List[Tuple[Document, float]]
    takes in the query and responds with the relevant documents present in the database
    """
    index_name = "pod-index"
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeVectorstore.from_existing_index(index_name = index_name, embedding = embeddings)
    docs = docsearch.similarity_search_with_relevance_scores(query)
    return docs