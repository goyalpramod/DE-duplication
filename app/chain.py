import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from app.vectorstores import InitialisePinecone
from langchain.schema import Document
import json 
load_dotenv(find_dotenv())
       
def fetch_data():
    """
    :params: dict
    :return: dict

    fetches the data from the text file and returns a Langchain Document Object
    """
    try:
        file_path = "data\dummy.json"
        with open(file_path, 'r') as file:
            data = json.load(file)
        docs = []

        for document in data:
            # page_content is a concatenation of description and title
            page_content = document["description"] + " " + document["title"]
            
            # Metadata should contain the rest, so we need to exclude description and title from the document dict
            metadata = {key: value for key, value in document.items() if key not in ['description', 'title']}
            
            final_doc = Document(page_content=page_content, metadata=metadata)
            docs.append(final_doc)
        return docs
    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return None
    
class MakeChain():
    def __init__(self) -> None:
        self.openai_api_key = os.environ["OPENAI_API_KEY"]

    def choose_embeddings(self, embeddings:str = "openai") -> None:
        """
        :params: str
        :return: None

        takes the embeddings to use for the chain

        """
        try:
            if embeddings == "openai":
                self.embeddings = OpenAIEmbeddings()
            else:
                return None
        except Exception as e:
            print(f"Error occurred while choosing embeddings: {e}")

    def choose_vectorstore(self, vectorstore:str = "pinecone", index_name:str = "pod-index"):
        """
        :params: str
        :return: retriever

        takes the vectorstore to use for the chain and returns the retriever
        """
        try:
            if vectorstore == "pinecone":
                pinecone = InitialisePinecone()
                index_created = pinecone.make_index()
                if index_created:
                    docs = fetch_data()
                    self.docsearch = PineconeVectorStore.from_documents(docs, self.embeddings, index_name=index_name)
                else:
                    self.docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=self.embeddings)
            else:
                return None
        except Exception as e:
            print(f"Error occurred while choosing vectorstore: {e}")
            return None

    def get_retriever(self):
        retriever = self.docsearch.as_retriever(
            search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.9}
        )
        return retriever

    def make_prompt(self):
        """
        :params: None
        :return: str

        returns the prompt to be used for the chain
        """
        try:
            template = """You are responsible for determining whether a new task is a duplicate of other tasks or not, or if similar tasks exists. 
            you will be provided with the information on the current tasks and relevant info inside <tasks> </tasks> tags, if the tags are empty that means the new task does not have any similar tasks present in the current tasks,
            but if some tasks are present inside the tags, then you have to determine whether the new task is a duplicate of the tasks present inside the tags or not.
            you will be given the new task inside <new_task> </new_task> tags. Only Reply with the id of tasks which you have determined are a copy or duplication of the new task. If no such tasks exist, reply with 0.
            <tasks> {context}</tasks>
            <new_task>{question}</<new_task>>"""
            prompt = ChatPromptTemplate.from_template(template)
            return prompt
        except Exception as e:
            print(f"Error occurred while making prompt: {e}")
            return None

    def choose_model(self, model:str = "gpt-4-1106-preview"):
        """
        :params: str
        :return: model

        takes the model to use for the chain and returns the model
        """
        try:
            if model == "gpt-4-1106-preview":
                model = ChatOpenAI(temperature=0, model=model)
            else:
                return None
            return model
        except Exception as e:
            print(f"Error occurred while choosing model: {e}")
            return None

# Make the chain
chain_obj = MakeChain()
chain_obj.choose_embeddings()
chain_obj.choose_vectorstore()
retriever = chain_obj.get_retriever()
prompt = chain_obj.make_prompt()
model = chain_obj.choose_model() 

chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)