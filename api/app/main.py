from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/api-pokemon"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Base = declarative_base()

class Type(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, index=True)

class Skill(Base):
    __tablename__ = "skill"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(Text, nullable=True)
    power = Column(Integer, nullable=True)
    accuracy = Column(Integer, nullable=True)
    max_life_point = Column(Integer, nullable=True)
    type_name = Column(String(20), ForeignKey("type.name"))

class Pokemon(Base):
    __tablename__ = "pokemon"
    id_pokedex = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), index=True)
    size = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    stats = Column(Integer, nullable=True)
    image = Column(Text, nullable=True)
    types = Column(Integer, ForeignKey("type.id"))
    skills = Column(Integer, ForeignKey("skill.id"))

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/pokemon/")
def get_all_pokemon(db: Session = Depends(get_db)):
    pokemons = db.query(Pokemon).all()
    return pokemons

# Example route to get a specific Pokemon by ID
@app.get("/pokemon/{pokemon_id}")
def get_pokemon_by_id(pokemon_id: int, db: Session = Depends(get_db)):
    pokemon = db.query(Pokemon).filter(Pokemon.id_pokedex == pokemon_id).first()
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

# Example route to create a new Pokemon
@app.post("/pokemon/")
def create_pokemon(pokemon: Pokemon, db: Session = Depends(get_db)):
    db_pokemon = Pokemon(**pokemon.dict())
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon

# Example route to update a Pokemon by ID
@app.put("/pokemon/{pokemon_id}")
def update_pokemon(pokemon_id: int, updated_pokemon: Pokemon, db: Session = Depends(get_db)):
    db_pokemon = db.query(Pokemon).filter(Pokemon.id_pokedex == pokemon_id).first()
    if db_pokemon:
        for key, value in updated_pokemon.dict().items():
            setattr(db_pokemon, key, value)
        db.commit()
        return db_pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

# Example route to delete a Pokemon by ID
@app.delete("/pokemon/{pokemon_id}")
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = db.query(Pokemon).filter(Pokemon.id_pokedex == pokemon_id).first()
    if db_pokemon:
        db.delete(db_pokemon)
        db.commit()
        return {"message": "Pokemon deleted successfully"}
    raise HTTPException(status_code=404, detail="Pokemon not found")

# Additional routes

# Example route to get all types
@app.get("/types/")
def get_all_types(db: Session = Depends(get_db)):
    types = db.query(Type).all()
    return types

# Example route to get a specific type by ID
@app.get("/types/{type_id}")
def get_type_by_id(type_id: int, db: Session = Depends(get_db)):
    type_entity = db.query(Type).filter(Type.id == type_id).first()
    if type_entity:
        return type_entity
    raise HTTPException(status_code=404, detail="Type not found")
