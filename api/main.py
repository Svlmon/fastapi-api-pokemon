from databases import Database
from fastapi import FastAPI, HTTPException


app = FastAPI()

database = Database("sqlite:///./db/pokemon.sqlite")


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Récupère la liste de tous les pokémons
@app.get("/pokemons")
async def get_pokemons():
    query = "SELECT * FROM Pokemon"
    pokemons = await database.fetch_all(query)
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Pokémons found")
    return pokemons
