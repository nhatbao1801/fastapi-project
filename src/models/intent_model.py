
from typing import List, Dict, Optional
from pydantic import BaseModel


class IntentModel(BaseModel):
    histories: Optional[List[Dict[str, str]]] = []
    question: str
