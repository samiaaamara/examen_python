from typing import List, Optional
from pydantic import BaseModel

class ActorCreate(BaseModel):
    actor_name: str

class MovieCreate(BaseModel):
    title: str
    year: int
    director: str
    actors: List[ActorCreate]

class Actor(BaseModel):
    id: int
    actor_name: str

    class Config:
        orm_mode = True

class Movie(BaseModel):
    id: int
    title: str
    year: int
    director: str
    actors: List[Actor]

    class Config:
        orm_mode = True
