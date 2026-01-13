from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

class URLRequest(BaseModel):
    url: str
