from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.schemas import QueryRequest, QueryResponse
from app.rag import search_knowledge_base

from app.database import deps
import os

router = APIRouter()
IS_TEST = os.getenv("TEST_ENV") == "true"

if not IS_TEST:
    @router.post("/recommend", response_model=QueryResponse)
    async def chat(request: QueryRequest, db: Session = Depends(deps.get_db)):
        query = request.query
        user_id = request.user_id

        answer = [[]]

        try:
            if user_id is not None:
                answer = await search_knowledge_base(db, query, user_id)
            else:
                answer = await search_knowledge_base(db, query)
        except Exception as e:
            print("Something went wrong")
            print(e)
            raise

        return QueryResponse(
            answer=answer
        )