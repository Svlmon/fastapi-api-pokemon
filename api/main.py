from databases import Database
from fastapi import FastAPI, HTTPException


app = FastAPI()

database = Database("sqlite:///./db/pokemon.sqlite")


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Récupère la liste de tous les pokémons
@app.get("/api/pokemons")
async def get_pokemons():
    query = "SELECT * FROM Pokemon"
    pokemons = await database.fetch_all(query)
    if not pokemons:
        raise HTTPException(status_code=404, detail="Pas de pokemons trouvés")
    return pokemons

@app.get("/api/pokemons/{pokemon_id}")
async def get_pokemons_by_id(pokemon_id : int):
    query = "SELECT * FROM Pokemon WHERE id_pokedex = :pokemon_id"
    values = {"pokemon_id" : pokemon_id}
    pokemons = await database.fetch_one(query, values)
    if not pokemons:
        raise HTTPException(status_code=404, detail="Pas de pokemons ayant cet ID")
    return pokemons

