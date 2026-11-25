
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.rag_service import ask_question

router = APIRouter(prefix="/api/questions", tags=["Questions"])


class QuestionRequest(BaseModel):
    document_id: str
    question: str


@router.post("/ask")
def ask_document_question(request: QuestionRequest):

    try:
        result = ask_question(
            document_id=request.document_id,
            question=request.question
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate answer"
        ) from error
