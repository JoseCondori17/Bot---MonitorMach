from pathlib import Path
from typing import List
import os

IMAGE_BASE_PATH = Path("images")

def get_pokemon_images(pokemon_name: str) -> List[str]:
    """Obtiene las rutas de las imágenes de un Pokémon ordenadas numéricamente."""
    pokemon_name = pokemon_name.lower()
    pokemon_folder = IMAGE_BASE_PATH / pokemon_name
    
    if not pokemon_folder.exists():
        return []
    
    # Obtener imágenes ordenadas numéricamente (0.jpg, 1.jpg, etc.)
    images = []
    for i in range(11):  # Del 0 al 10
        for ext in ['.jpg', '.jpeg', '.png', '.gif']:
            image_path = pokemon_folder / f"{i}{ext}"
            if image_path.exists():
                images.append(f"/static/images/{pokemon_name}/{i}{ext}")
                break  # Solo una imagen por número
    
    return images