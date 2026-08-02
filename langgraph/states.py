import os

#1) typed DICT

from typing import TypedDict

class State(TypedDict):
    topic: str
    summary: str
    score: int

#2) pydantic apporach
# it is good at data validation and type chekcing at runtime

from pydantic import BaseModel, field_validator

class State(BaseModel):
    topic: str
    score: int
    summary: str = ""

    @field_validator("score")
    def score_positive(cls, v):
        if v < 0:
            raise ValueError("Score must be positive")

# python dataclass

#standered python dataclass but it is used rarely

from dataclasses import dataclass, field

@dataclass
class State:
    topic : str = ""
    summary : str = ""
    messages : list = field(default_factory=list)

#from langgraph

from langgraph.graph import MessagesState

class State(MessagesState):
    #message filed is alredy included with add_messages reducer
    # just add your extra feilds
    user_name: str
    language: str



