from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.chain import chain as check_duplicate_chain
from langchain_core.runnables import RunnableLambda
from app.chain import MakeChain
from app.main import search_duplicate

chain_obj = MakeChain()
chain_obj.choose_embeddings()
chain_obj.choose_vectorstore()
retriever_chain = chain_obj.get_retriever()

app = FastAPI()

search_duplicate_chain = RunnableLambda(search_duplicate)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, check_duplicate_chain, path="/check-duplicate")
add_routes(app, retriever_chain, path="/retrieve-relevant-docs")
add_routes(app, search_duplicate_chain, path="/search-duplicate")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
