from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.chain import chain as check_duplicate_chain
from app.chain import MakeChain

chain_obj = MakeChain()
chain_obj.choose_embeddings()
chain_obj.choose_vectorstore()
retriever = chain_obj.get_retriever()

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, check_duplicate_chain, path="/check-duplicate")
add_routes(app, retriever, path="/retrieve-relevant-docs")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
