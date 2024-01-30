from app.vectorstores import InitialisePinecone
from app.chain import fetch_data
from langchain_community.vectorstores import Pinecone as PineconeVectorstore
from langchain_openai import OpenAIEmbeddings

index_name = "pod-index"

def retrieve_relevant_docs(query:str = "Perform UAT") -> dict:
    """
    :param: str
    :return: dict
    takes in the query and responds with the relevant documents present in the database
    """
    pinecone = InitialisePinecone()
    pinecone.make_index()
    embeddings = OpenAIEmbeddings()
    docs = fetch_data({"question" : query})
    docsearch = PineconeVectorstore.from_documents(docs["context"], embeddings, index_name=index_name)
    docs = docsearch.similarity_search(docs["question"])
    return docs

print(retrieve_relevant_docs())