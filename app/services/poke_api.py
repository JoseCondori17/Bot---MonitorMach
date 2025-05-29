import requests
from fastapi import HTTPException

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

async def get_pokemon_data(pokemon_name: str):
    try:
        response = requests.get(f"{POKEAPI_URL}{pokemon_name.lower()}")
        response.raise_for_status()
        data = response.json()
        
        return {
            "name": data["name"],
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "height": data["height"],
            "weight": data["weight"]
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=404, detail=f"Pokémon not found in PokeAPI: {str(e)}")