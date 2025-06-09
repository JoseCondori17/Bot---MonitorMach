from fastapi import HTTPException
from pathlib import Path
from .pokeapi_service import PokeAPIService
from .stats_service import StatsService
from .image_service import ImageService
from ..utils.logger import CustomLogger
from ..utils.monitoring import monitor

logger = CustomLogger("PokeSearch")

class SearchService:
    def __init__(self):
        self.pokeapi = PokeAPIService()
        self.stats = StatsService()
        self.images = ImageService()
    
    def search_pokemon(self, pokemon_name: str):
        start_time = logger.log("search", "search_pokemon", f"Searching for {pokemon_name}")
        try:
            # Obtener datos de PokeAPI
            api_data = self.pokeapi.get_pokemon(pokemon_name)
            
            # Obtener stats del CSV
            stats_data = self.stats.get_stats(pokemon_name)
            
            # Obtener lista de imágenes
            pokemon_folder = Path("images") / pokemon_name.lower()
            image_urls = []
            if pokemon_folder.exists():
                image_urls = sorted([
                    f"/api/images/{pokemon_name}/{img.stem}"
                    for img in pokemon_folder.glob("*.jpg")
                ])
            
            # Construir respuesta unificada
            response = {
                "name": api_data.name,
                "stats": stats_data.dict(),
                "images": image_urls
            }
            
            monitor.log_request("PokeSearch", "search_pokemon", 200,
                              int((logger.log("search", "search_pokemon", "Search completed", start_time) - start_time) * 1000))
            return response
            
        except HTTPException as he:
            monitor.log_request("PokeSearch", "search_pokemon", he.status_code, 0)
            raise he
        except Exception as e:
            monitor.log_request("PokeSearch", "search_pokemon", 500, 0)
            logger.log("search", "search_pokemon", f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))