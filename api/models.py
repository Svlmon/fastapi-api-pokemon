from pydantic import BaseModel, Field
from typing import List, Optional


class Pokemon(BaseModel):
    id_pokedex: Optional[int] = Field( primary_key=True)
    name: str
    size: float
    weight: float
    stats: float
    image: str
    types: List[int]
    skills: List[int]


class PokemonCreate(Pokemon):
    pass


class Type(BaseModel):
    id: Optional[int] = Field( primary_key=True)
    name: str


class TypeCreate(Type):
    pass


class Skill(BaseModel):
    id: int
    name: str
    description: str
    power: int
    accuracy: int
    pp_max: int
    type_name: str


class SkillCreate(Skill):
    pass
