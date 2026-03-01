from enum import Enum
from pydantic import BaseModel
from typing import Dict, List, Any

class SearchField(Enum):
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    ID = "id"

class SearchMetadata(BaseModel):
    searched_by: str
    searched_value: str

class Pagination(BaseModel):
    total_matches: int
    showing: int
    offset: int
    limit: int

class SearchResponse(BaseModel):
    metadata: SearchMetadata
    pagination: Pagination
    results: List[Dict[str, Any]]

