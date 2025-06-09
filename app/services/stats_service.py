import csv
from fastapi import HTTPException
from pathlib import Path
from ..utils.logger import CustomLogger
from ..utils.monitoring import monitor
from ..models.pokemon import PokemonStats

logger = CustomLogger("PokeStats")

class StatsService:
    def __init__(self):
        self.data = []
        self.csv_path = Path("data/pokemon_stats.csv")
        self._load_data()
    
    def _load_data(self):
        start_time = logger.log("stats", "_load_data", "Loading CSV data")
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.data = [PokemonStats.from_csv_row(row) for row in reader]
            logger.log("stats", "_load_data", "CSV data loaded", start_time)
        except Exception as e:
            logger.log("stats", "_load_data", f"Error loading CSV: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to load stats data")
    
    def get_stats(self, identifier):
        start_time = logger.log("stats", "get_stats", "Fetching Pokemon stats")
        try:
            result = None
            if identifier.isdigit():
                result = next((item for item in self.data if item.id == int(identifier)), None)
            else:
                result = next((item for item in self.data if item.name.lower() == identifier.lower()), None)
            
            if result:
                monitor.log_request("PokeStats", "get_stats", 200, 
                                  int((logger.log("stats", "get_stats", "Stats fetched", start_time) - start_time) * 1000))
                return result
            else:
                monitor.log_request("PokeStats", "get_stats", 404, 0)
                raise HTTPException(status_code=404, detail="Pokemon stats not found")
        except Exception as e:
            monitor.log_request("PokeStats", "get_stats", 500, 0)
            logger.log("stats", "get_stats", f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))