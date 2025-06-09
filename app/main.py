from fastapi import FastAPI, HTTPException
from pathlib import Path
from typing import Optional
from .services.pokeapi_service import PokeAPIService
from .services.stats_service import StatsService
from .services.image_service import ImageService
from .services.search_service import SearchService
from .utils.monitoring import monitor
from datetime import datetime, timedelta

app = FastAPI()
pokeapi_service = PokeAPIService()
stats_service = StatsService()
image_service = ImageService()
search_service = SearchService()
@app.get("/api/pokemon/{identifier}")
async def get_pokemon(identifier: str):
    return pokeapi_service.get_pokemon(identifier)

@app.post("/poke/search/")
async def search_pokemon(request: dict):
    pokemon_name = request.get("pokemon_name")
    if not pokemon_name:
        raise HTTPException(status_code=400, detail="pokemon_name is required")
    return search_service.search_pokemon(pokemon_name)

@app.get("/api/stats/{identifier}")
async def get_stats(identifier: str):
    return stats_service.get_stats(identifier)

@app.get("/api/images/{pokemon_name}")
async def get_pokemon_images(pokemon_name: str, index: Optional[int] = None):
    """Endpoint para obtener imágenes"""
    if index is not None:
        # Devolver imagen específica
        return image_service.get_image(pokemon_name, index)
    else:
        # Devolver lista de imágenes disponibles
        return {"images": image_service.get_all_images(pokemon_name)}

@app.get("/api/images/{pokemon_name}/{image_index}")
async def get_specific_image(pokemon_name: str, image_index: int):
    """Endpoint alternativo para imágenes específicas"""
    return image_service.get_image(pokemon_name, image_index)

# Bot commands endpoints
@app.get("/bot/CheckLatency")
async def check_latency(module: str, start_date: str, end_date: str):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        latency = monitor.get_latency(module, start, end)
        return {"module": module, "start_date": start_date, "end_date": end_date, "latency_ms": latency}
    except Exception as e:
        return {"error": str(e)}

@app.get("/bot/CheckAvailability")
async def check_availability(module: str, days: int):
    try:
        availability = monitor.get_availability(module, days)
        return {"module": module, "days": days, "availability_percentage": availability}
    except Exception as e:
        return {"error": str(e)}

@app.get("/bot/RenderGraph")
async def render_graph(metric: str, module: str, days: int):
    try:
        # This would be more complex in a real implementation
        if metric.lower() == "latency":
            return {"message": "ASCII graph would be rendered here for latency"}
        elif metric.lower() == "availability":
            return {"message": "ASCII graph would be rendered here for availability"}
        else:
            return {"error": "Invalid metric"}
    except Exception as e:
        return {"error": str(e)}