import os
from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from app.vectorstores import InitialisePinecone
load_dotenv(find_dotenv())
       
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
                pinecone.make_index()
                self.vectorstore = PineconeVectorStore.from_existing_index(index_name=index_name,
                                           embedding=self.embeddings)
            else:
                return None
            
            retriever = self.vectorstore.as_retriever()
            return retriever
        except Exception as e:
            print(f"Error occurred while choosing vectorstore: {e}")
            return None

    def make_prompt(self):
        """
        :params: None
        :return: str

        returns the prompt to be used for the chain
        """
        try:
            template = """Answer the question based only on the following context:
                        {context}
                        Question: {question}
                        """
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
        
    
def fetch_data(x):
    """
    :params: dict
    :return: dict

    fetches the data from the text file and returns a dict
    """
    try:
        # TODO find the path using os instead of manually putting it in
        loader = TextLoader(r"data\dummy.txt")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)   
        return {"context": docs, "question": x["question"]}
    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return None

# Make the chain
chain_obj = MakeChain()
chain_obj.choose_embeddings()
retriever = chain_obj.choose_vectorstore()
prompt = chain_obj.make_prompt()
model = chain_obj.choose_model() 

chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | RunnableLambda(fetch_data) 
    | prompt
    | model
    | StrOutputParser()
)