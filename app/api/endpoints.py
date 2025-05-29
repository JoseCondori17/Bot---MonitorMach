from fastapi import APIRouter, HTTPException
from app.models.schemas import PokemonResponse
from app.services.poke_api import get_pokemon_data
from app.services.stats import stats_service
from app.services.images import get_pokemon_images

router = APIRouter()

@router.get("/pokemon/{pokemon_name}", response_model=PokemonResponse)
async def get_pokemon_info(pokemon_name: str):
    try:
        # Obtener datos básicos de PokeAPI
        poke_data = await get_pokemon_data(pokemon_name)
        
        # Obtener estadísticas adicionales
        stats = stats_service.get_pokemon_stats(pokemon_name)
        if not stats:
            raise HTTPException(status_code=404, detail="Pokémon stats not found")
        
        # Obtener imágenes locales
        images = get_pokemon_images(pokemon_name)
        
        return {
            "name": poke_data["name"],
            "types": poke_data["types"],
            "abilities": poke_data["abilities"],
            "height": poke_data["height"],
            "weight": poke_data["weight"],
            "stats": stats,
            "images": images
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))