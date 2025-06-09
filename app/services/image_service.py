from fastapi import HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from ..utils.logger import CustomLogger
from ..utils.monitoring import monitor

logger = CustomLogger("PokeImages")

class ImageService:
    BASE_PATH = Path("images")
    
    def get_image(self, pokemon_name: str, image_index: int = 0):
        """Obtiene una imagen específica o la primera por defecto"""
        start_time = logger.log("images", "get_image", f"Fetching image {image_index} for {pokemon_name}")
        try:
            pokemon_folder = self.BASE_PATH / pokemon_name.lower()
            if not pokemon_folder.exists():
                monitor.log_request("PokeImages", "get_image", 404, 0)
                raise HTTPException(status_code=404, detail="Pokemon folder not found")
            
            image_path = pokemon_folder / f"{image_index}.jpg"
            if not image_path.exists():
                monitor.log_request("PokeImages", "get_image", 404, 0)
                raise HTTPException(status_code=404, detail=f"Image {image_index}.jpg not found")
            
            monitor.log_request("PokeImages", "get_image", 200, 
                             int((logger.log("images", "get_image", "Image found", start_time) - start_time) * 1000))
            return FileResponse(image_path)
        except Exception as e:
            monitor.log_request("PokeImages", "get_image", 500, 0)
            logger.log("images", "get_image", f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_all_images(self, pokemon_name: str):
        """Lista todas las imágenes disponibles"""
        start_time = logger.log("images", "get_all_images", f"Listing images for {pokemon_name}")
        try:
            pokemon_folder = self.BASE_PATH / pokemon_name.lower()
            if not pokemon_folder.exists():
                return []
            
            images = sorted([img.name for img in pokemon_folder.glob("*.jpg")])
            monitor.log_request("PokeImages", "get_all_images", 200,
                             int((logger.log("images", "get_all_images", "Images listed", start_time) - start_time) * 1000))
            return images
        except Exception as e:
            monitor.log_request("PokeImages", "get_all_images", 500, 0)
            logger.log("images", "get_all_images", f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))