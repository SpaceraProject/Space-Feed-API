# pylint: disable=all
from pydantic import BaseModel

class Article(BaseModel):
    title: str
    link: str
    summary: str
    text: str

    class Config:
        from_attributes = True
