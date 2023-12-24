
from typing import List, Dict, Optional
from pydantic import BaseModel


class IntentModel(BaseModel):
    history: Optional[List] = []
    question: str
