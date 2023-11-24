import json
from databases import Database
from fastapi import FastAPI, HTTPException

from models import PokemonCreate, SkillCreate, TypeCreate


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
    pokemon = await database.fetch_one(query, values)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pas de pokemons ayant cet ID")
    return pokemon

@app.get("/api/types/{type_id}")
async def get_types_by_id(type_id : int):
    query = "SELECT * FROM Type WHERE id = :type_id"
    values = {"type_id" : type_id}
    type = await database.fetch_one(query, values)
    if not type:
        raise HTTPException(status_code=404, detail=f"Pas de type ayant cet ID : {type_id}")
    return type

@app.get("/api/abilities")
async def get_abilities():
    query = "SELECT * FROM Skill"
    skills = await database.fetch_all(query)
    if not skills:
        raise HTTPException(status_code=404, detail="Pas de capacités trouvées")
    return skills

@app.post("/api/pokemons")
async def add_pokemon(pokemon: PokemonCreate):
    check_query = "SELECT * FROM Pokemon WHERE id_pokedex = :pokedex_id"
    check_values = {"pokedex_id": pokemon.id_pokedex}
    check_pokemon = await database.fetch_one(check_query, check_values)
    if check_pokemon:
        raise HTTPException(status_code=400, detail="Le pokémon existe déjà")

    for skill_id in pokemon.skills:
        check_query = "SELECT * FROM Skill WHERE id = :skill_id"
        check_values = {"skill_id": skill_id}
        check_ability = await database.fetch_one(check_query, check_values)
        if not check_ability:
            raise HTTPException(status_code=400, detail=f"La compétence suivante : {skill_id} n'existe pas")
        
    for type_id in pokemon.types:
        check_query = "SELECT * FROM Type WHERE id = :type_id"
        check_values = {"type_id": type_id}
        check_ability = await database.fetch_one(check_query, check_values)
        if not check_ability:
            raise HTTPException(status_code=400, detail=f"Le type suivant : {type_id} n'existe pas")
            
    query = ("INSERT INTO Pokemon (name, size, weight, stats, image, types, skills) VALUES ("
             " :name, :size, :weight, :stats, :image, :types, :skills)")
    values = {
        "name": pokemon.name,
        "size": pokemon.size,
        "weight": pokemon.weight,
        "stats": pokemon.stats,
        "image": pokemon.image,
        "types": json.dumps(pokemon.types), 
        "skills": json.dumps(pokemon.skills), 
    }

    pokemon = await database.execute(query, values)
    if pokemon:
        return {"message": "Le pokémon a été ajouté"}
    raise HTTPException(status_code=404, detail="Le pokémon existe déjà")

@app.post("/api/types")
async def add_type(type: TypeCreate):
    check_query = "SELECT * FROM Type WHERE name = :name"
    check_values = {"name": type.name}
    check_type = await database.fetch_one(check_query, check_values)
    if check_type:
        raise HTTPException(status_code=400, detail="Le type existe déjà")

    query = "INSERT INTO Type (name) VALUES (:name)"
    values = {"name": type.name}

    type = await database.execute(query, values)
    if type:
        return {"message": "Le type a été ajouté"}
    raise HTTPException(status_code=404, detail="Le type existe déjà")


@app.put("/api/pokemons/{pokemon_id}")
async def update_pokemon(pokemon_id: int, pokemon: PokemonCreate):
    existing_query = "SELECT * FROM Pokemon WHERE id_pokedex = :pokemon_id"
    existing_values = {"pokemon_id": pokemon_id}
    existing_pokemon = await database.fetch_one(existing_query, existing_values)
    if not existing_pokemon:
        raise HTTPException(status_code=404, detail="Le pokémon n'existe pas")

    for skill_id in pokemon.skills:
        check_query = "SELECT * FROM Skill WHERE id = :skill_id"
        check_values = {"skill_id": skill_id}
        check_ability = await database.fetch_one(check_query, check_values)
        if not check_ability:
            raise HTTPException(status_code=400, detail=f"La compétence suivante : {skill_id} n'existe pas")

    for type_id in pokemon.types:
        check_query = "SELECT * FROM Type WHERE id = :type_id"
        check_values = {"type_id": type_id}
        check_type = await database.fetch_one(check_query, check_values)
        if not check_type:
            raise HTTPException(status_code=400, detail=f"Le type suivant : {type_id} n'existe pas")

    query = ("UPDATE Pokemon SET id_pokedex = :pokedex_id, name = :name, size = :size, weight = :weight, stats = "
             ":stats, image = :image, types = :types, skills = :skills WHERE id_pokedex = :pokemon_id")
    values = {
        "pokemon_id": pokemon_id,
        "pokedex_id": pokemon.id_pokedex,
        "name": pokemon.name,
        "size": pokemon.size,
        "weight": pokemon.weight,
        "stats": pokemon.stats,
        "image": pokemon.image,
        "types": json.dumps(pokemon.types),
        "skills": json.dumps(pokemon.skills),
    }

    pokemon = await database.execute(query, values)
    if pokemon:
        return {"message": "Le pokemon a été mise à jour"}
    raise HTTPException(status_code=404, detail="Le pokémon n'existe pas")

@app.put("/api/abilities/{ability_id}")
async def update_ability(ability_id: int, ability: SkillCreate):
    query = ("UPDATE Skill SET id = :id, name = :name, description = :description,"
             "power = :power, accuracy = :accuracy, pp_max = :pp_max, type_name = :type_name WHERE id = "
             ":ability_id")
    values = {
        "ability_id": ability.id,
        "id": ability.id,
        "name": ability.name,
        "description": ability.description,
        "power": ability.power,
        "accuracy": ability.accuracy,
        "pp_max": ability.pp_max,
        "type_name": ability.type_name,
    }

    ability = await database.execute(query, values)
    if ability:
        return {"message": "La compétence a été mise à jour"}
    raise HTTPException(status_code=404, detail="La compétence n'existe pas ")

@app.put("/api/type/{type_id}")
async def update_type(type_id: int, type: TypeCreate):
    query = "UPDATE Type SET id = :id, name = :name WHERE id = :type_id"
    values = {"type_id": type_id, "id": type.id, "name": type.name}

    type = await database.execute(query, values)
    if type:
        return {"message": "Le type a été mise à jour"}
    raise HTTPException(status_code=404, detail="Le type n'existe pas")


# Suppression du pokémon précisé par :id
@app.delete("/api/pokemon/{pokemon_id}")
async def delete_pokemon(pokemon_id: int):
    name_query = "SELECT name FROM Pokemon WHERE id_pokedex = :pokemon_id"
    name_values = {"pokemon_id": pokemon_id}
    pokemon_name = await database.fetch_val(name_query, name_values)

    if pokemon_name is None:
        raise HTTPException(status_code=404, detail="le pokémon n'existe pas")

    delete_query = "DELETE FROM Pokemon WHERE id_pokedex = :pokedex_id"
    delete_values = {"pokedex_id": pokemon_id}
    await database.execute(delete_query, delete_values)

    return {"message": f"Le pokémon suivant : {pokemon_name} a été supprimé"}
