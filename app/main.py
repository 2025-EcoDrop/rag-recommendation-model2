from fastapi import FastAPI
from app.routes import chat

# uvicorn app.main:app --reload --port 8000

app = FastAPI()
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}