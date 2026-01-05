from pydantic import BaseModel
from typing import Optional, List

class Trial(BaseModel):
    nct_id: str
    title: str
    condition: List[str]
    phase: Optional[str]
    status: Optional[str]
    locations: Optional[List[str]]
