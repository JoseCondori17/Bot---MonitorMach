from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PokemonStat(BaseModel):
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    total: int
    type1: str
    type2: Optional[str]

class PokemonResponse(BaseModel):
    name: str
    types: List[str]
    abilities: List[str]
    height: int
    weight: int
    stats: PokemonStat
    images: List[str]