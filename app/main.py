from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router
from pathlib import Path

app = FastAPI(
    title="Poke/Search API",
    description="API que integra información de Pokémon de múltiples fuentes",
    version="1.0.0"
)

# Configurar archivos estáticos para las imágenes
images_path = Path(__file__).parent.parent / "images"
app.mount("/static", StaticFiles(directory=images_path), name="static")

app.include_router(api_router, prefix="/api/v1")