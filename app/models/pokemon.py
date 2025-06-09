from pydantic import BaseModel
from typing import List, Optional

class Ability(BaseModel):
    name: str
    url: str

class PokemonAbility(BaseModel):
    ability: Ability
    is_hidden: bool
    slot: int

class PokemonSprites(BaseModel):
    front_default: Optional[str] = None
    front_shiny: Optional[str] = None


class Pokemon(BaseModel):
    id: int
    name: str
    base_experience: int
    height: int
    weight: int
    abilities: List[PokemonAbility]
    sprites: PokemonSprites


class PokemonStats(BaseModel):
    id: int
    name: str
    type1: str
    type2: Optional[str] = None
    total: int
    hp: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int
    generation: int
    legendary: bool

    @classmethod
    def from_csv_row(cls, row: dict):
        return cls(
            id=int(row['#']),
            name=row['Name'],
            type1=row['Type 1'],
            type2=row['Type 2'] if row['Type 2'] else None,
            total=int(row['Total']),
            hp=int(row['HP']),
            attack=int(row['Attack']),
            defense=int(row['Defense']),
            sp_atk=int(row['Sp. Atk']),
            sp_def=int(row['Sp. Def']),
            speed=int(row['Speed']),
            generation=int(row['Generation']),
            legendary=row['Legendary'].lower() == 'true'
        )