from enum import Enum
from pydantic import BaseModel, Field
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

class Marks(BaseModel):
    English: int = Field(..., ge=0, le=100)
    Maths: int = Field(..., ge=0, le=100)
    Science: int = Field(..., ge=0, le=100)

class StudentCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    id: int = Field(..., ge=0, le=100)
    marks: Marks
    
    