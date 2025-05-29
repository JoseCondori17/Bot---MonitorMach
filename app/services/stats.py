import pandas as pd
from pathlib import Path
from fastapi import HTTPException

class PokemonStatsService:
    def __init__(self):
        self.df = self._load_stats()
    
    def _load_stats(self):
        try:
            csv_path = Path(__file__).parent.parent.parent / "data" / "pokemon_stats.csv"
            df = pd.read_csv(csv_path)
            
            # Limpieza de nombres con formas alternativas (Mega, etc.)
            df['Name'] = df['Name'].str.replace(r'Mega\s.*|Primal\s.*|.*Forme|.*Mode', '', regex=True)
            df['Name'] = df['Name'].str.strip()
            
            return df
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading stats CSV: {str(e)}")
    
    def get_pokemon_stats(self, pokemon_name: str):
        try:
            # Buscar por nombre (case insensitive)
            pokemon_stats = self.df[self.df['Name'].str.lower() == pokemon_name.lower()]
            
            if pokemon_stats.empty:
                return None
                
            # Tomar la primera coincidencia (ignorando formas alternativas)
            stats = pokemon_stats.iloc[0].to_dict()
            
            return {
                "hp": stats["HP"],
                "attack": stats["Attack"],
                "defense": stats["Defense"],
                "sp_attack": stats["Sp. Atk"],
                "sp_defense": stats["Sp. Def"],
                "speed": stats["Speed"],
                "total": stats["Total"],
                "type1": stats["Type 1"],
                "type2": stats["Type 2"] if pd.notna(stats["Type 2"]) else None
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

stats_service = PokemonStatsService()