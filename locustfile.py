from locust import HttpUser, task, between
import random

class PokemonUser(HttpUser):
    host = "http://localhost:8000"  
    wait_time = between(1, 3)
    
    # Lista de Pokémon para testing
    POKEMONS = [
        "pikachu", "charizard", "bulbasaur", "mewtwo", "squirtle",
        "eevee", "mew", "ditto", "gyarados", "snorlax"
    ]
    
    def on_start(self):
        """Inicialización para cada usuario virtual"""
        self.pokemon = random.choice(self.POKEMONS)

    @task(4)
    def search_pokemon(self):
        """Test endpoint POST /poke/search/"""
        self.client.post(
            "/poke/search/",
            json={"pokemon_name": self.pokemon},
            name="/poke/search"
        )

    @task(3)
    def get_pokemon_data(self):
        """Test endpoint /api/pokemon/"""
        self.client.get(
            f"/api/pokemon/{self.pokemon}",
            name="/api/pokemon/[name]"
        )

    @task(2)
    def get_stats(self):
        """Test endpoint /api/stats/"""
        self.client.get(
            f"/api/stats/{self.pokemon}",
            name="/api/stats/[name]"
        )

    @task(1)
    def get_images(self):
        """Test endpoint /api/images/"""
        self.client.get(
            f"/api/images/{self.pokemon}",
            name="/api/images/[name]"
        )