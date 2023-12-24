from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.module.intent_component.intent_detect import IntentComponent
from src.models.intent_model import IntentModel

router = APIRouter(prefix="/api/conversation", tags=["gpt"])
intent_component = IntentComponent()


@router.post(path="/getAnswer")
async def detect_intent(req: IntentModel) -> JSONResponse:

    return intent_component.detect_from_sender_histories(sender_data=req.question,
                                                         conversation_history=req.history)
