from typing import Optional
from pydantic import BaseModel

class ReferenceLetterRequest(BaseModel):
    name: str
    description: Optional[str] = None