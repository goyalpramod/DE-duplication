from langchain_community.vectorstores import Pinecone as PineconeVectorstore
from langchain_openai import OpenAIEmbeddings
from app.vectorstores import InitialisePinecone
from app.chain import chain,fetch_data
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def search_duplicate(query:str) -> str:
    """
    :param: str
    :return: List[Tuple[Document, float]]
    takes in the query and responds with whether there are any duplicate documents present in the database
    """
    index_name = "pod-index"
    embeddings = OpenAIEmbeddings()
    pinecone = InitialisePinecone()
    index_created = pinecone.make_index()
    if index_created:
        docs = fetch_data()
        docsearch = PineconeVectorstore.from_documents(docs, embeddings, index_name=index_name)
    else:
        docsearch = PineconeVectorstore.from_existing_index(index_name=index_name, embedding=embeddings)
    docs = docsearch.similarity_search_with_relevance_scores(query)
    context_docs = []
    for doc_tuple_list in docs:
        if doc_tuple_list[-1] > 0.98:
            return "This is an exact duplicate of -> {task}. which has been assigned to {assignee}, with a task ID of {id}".format(task = doc_tuple_list[0].page_content, assignee = doc_tuple_list[0].metadata['assigned'], id = doc_tuple_list[0].metadata['Id'])
        elif doc_tuple_list[-1] > 0.9:
            context_docs.append(doc_tuple_list)
    if len(context_docs) > 0:
        return chain.invoke(query)
    else:
        return "No similar documents found"