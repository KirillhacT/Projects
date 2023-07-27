from pydantic import BaseModel
from datetime import date
from typing import Optional

class SPosts(BaseModel):
    id: int
    title: str
    description: str
    release_date: date
    series_count: int
    genre: str
    image_id: Optional[int]

    class Config:
        orm_mode = True
        