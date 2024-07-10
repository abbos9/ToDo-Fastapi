from pydantic import  BaseModel
from datetime import datetime

from config import Tashkent_tz

class CrudAssignmentSchema(BaseModel):
    title: str
    description:str
    priority:str
    the_nadir:str
    is_complete:bool
    created_at:datetime = datetime.now(tz=Tashkent_tz)
    updated_at:datetime = datetime.now(tz=Tashkent_tz)
    class Config:
        orm_mode=True

class ResponseAssignmentSchema(BaseModel):
    id:int
    title: str
    description:str
    priority:str
    the_nadir:str
    is_complete:bool


    class Config:
        orm_mode=True


class UpdateAssignmentSchema(BaseModel):
    title: str
    description:str
    priority:str
    the_nadir:str
    is_complete:bool
    updated_at:datetime = datetime.now(tz=Tashkent_tz)

    class Config:
        orm_mode=True