from pydantic import BaseModel


class Translation(BaseModel):
    source: str = ''
    translate: str = ''
