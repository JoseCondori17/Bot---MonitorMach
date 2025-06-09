import requests
from fastapi import HTTPException
from ..utils.logger import CustomLogger
from ..utils.monitoring import monitor
from ..models.pokemon import Pokemon

logger = CustomLogger("PokeAPI")

class PokeAPIService:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
    
    def get_pokemon(self, identifier):
        start_time = logger.log("pokeapi", "get_pokemon", "Fetching Pokemon data")
        try:
            response = requests.get(f"{self.BASE_URL}{identifier}")
            if response.status_code == 200:
                pokemon_data = response.json()
                pokemon = Pokemon(
                    id=pokemon_data['id'],
                    name=pokemon_data['name'],
                    base_experience=pokemon_data['base_experience'],
                    height=pokemon_data['height'],
                    weight=pokemon_data['weight'],
                    abilities=pokemon_data['abilities'],
                    sprites=pokemon_data['sprites']
                )
                monitor.log_request("PokeAPI", "get_pokemon", 200, 
                                  int((logger.log("pokeapi", "get_pokemon", "Data fetched", start_time) - start_time) * 1000))
                return pokemon
            else:
                monitor.log_request("PokeAPI", "get_pokemon", response.status_code, 0)
                raise HTTPException(status_code=response.status_code, detail="Pokemon not found")
        except Exception as e:
            monitor.log_request("PokeAPI", "get_pokemon", 500, 0)
            logger.log("pokeapi", "get_pokemon", f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))