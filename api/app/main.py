from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from requests import Session
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import List

# Database configuration
DATABASE_URL = "sqlite:///identifier.sqlite"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database models
class Type(Base):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Pokemon(Base):
    __tablename__ = "pokemons"
    id_pokedex = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    size = Column(Float)
    weight = Column(Float)
    stats = Column(String)
    image = Column(String)
    type_id = Column(Integer, ForeignKey("types.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    # Relationship with Type and Skill
    type = relationship("Type", back_populates="pokemons")
    skill = relationship("Skill", back_populates="pokemons")

# Linking relationships
Type.pokemons = relationship("Pokemon", back_populates="type")
Skill.pokemons = relationship("Pokemon", back_populates="skill")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic models
class TypeBase(BaseModel):
    name: str

class TypeCreate(TypeBase):
    pass

class TypeResponse(TypeBase):
    id: int

class SkillBase(BaseModel):
    name: str

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int

class PokemonBase(BaseModel):
    name: str
    size: float
    weight: float
    stats: str
    image: str
    type_id: int
    skill_id: int

class PokemonCreate(PokemonBase):
    pass

class PokemonResponse(PokemonBase):
    id_pokedex: int

# Custom response model
class CustomResponse(BaseModel):
    item_id: int
    q: str

# Define a generic function to retrieve all items from a table
def get_all_items(db_session: Session, model):
    try:
        items = db_session.query(model).all()
        return [item.__dict__ for item in items]
    except Exception as e:
        print(f"Error retrieving items from {model.__name__} table: {e}")
        return None

# Define a generic function to retrieve an item from a table by ID
def get_item_by_id(db_session: Session, model, item_id: int):
    try:
        item = db_session.query(model).filter(model.id == item_id).first()
        return item.__dict__ if item else None
    except Exception as e:
        print(f"Error retrieving item from {model.__name__} table with ID {item_id}: {e}")
        return None

# Define a generic function to create an item in a table
def create_item(db_session: Session, model, item_data):
    try:
        db_item = model(**item_data.dict())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)
        return db_item.__dict__
    except Exception as e:
        print(f"Error creating item in {model.__name__} table: {e}")
        return None

# Define a generic function to update an item in a table by ID
def update_item(db_session: Session, model, item_id: int, updated_data):
    try:
        db_item = db_session.query(model).filter(model.id == item_id).first()
        if db_item:
            for key, value in updated_data.dict().items():
                setattr(db_item, key, value)
            db_session.commit()
            return db_item.__dict__
    except Exception as e:
        print(f"Error updating item in {model.__name__} table: {e}")
    return None

# Define a generic function to delete an item in a table by ID
def delete_item(db_session: Session, model, item_id: int):
    try:
        db_item = db_session.query(model).filter(model.id == item_id).first()
        if db_item:
            db_session.delete(db_item)
            db_session.commit()
            return {"message": "Item deleted successfully"}
    except Exception as e:
        print(f"Error deleting item in {model.__name__} table: {e}")
    return {"message": "Item not found"}

@app.get("/")
def read_root():
    return {"Hello": "World"}


# Example route to get all Pokemon
@app.get("/pokemon/", response_model=List[CustomResponse])
def get_all_pokemon(db: Session = Depends(get_db)):
    pokemons = get_all_items(db, Pokemon)
    
    # Modify this part to return the custom response
    return [CustomResponse(item_id=pokemon.id_pokedex, q=pokemon.name) for pokemon in pokemons]

# Example route to get a specific Pokemon by ID
@app.get("/pokemon/{pokemon_id}", response_model=CustomResponse)
def get_pokemon_by_id(pokemon_id: int, db: Session = Depends(get_db)):
    pokemon = get_item_by_id(db, Pokemon, pokemon_id)
    
    # Modify this part to return the custom response
    return CustomResponse(item_id=pokemon.id_pokedex, q=pokemon.name)

# Example route to create a new Pokemon
@app.post("/pokemon/", response_model=CustomResponse)
def create_pokemon(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    db_pokemon = create_item(db, Pokemon, pokemon)
    
    # Modify this part to return the custom response
    return CustomResponse(item_id=db_pokemon.id_pokedex, q=db_pokemon.name)

# Example route to update a Pokemon by ID
@app.put("/pokemon/{pokemon_id}", response_model=CustomResponse)
def update_pokemon(pokemon_id: int, updated_pokemon: PokemonCreate, db: Session = Depends(get_db)):
    db_pokemon = update_item(db, Pokemon, pokemon_id, updated_pokemon)
    
    # Modify this part to return the custom response
    return CustomResponse(item_id=db_pokemon.id_pokedex, q=db_pokemon.name)

# Example route to delete a Pokemon by ID
@app.delete("/pokemon/{pokemon_id}", response_model=dict)
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    delete_item(db, Pokemon, pokemon_id)
    
    # Modify this part to return the custom response
    return {"message": "Pokemon deleted successfully"}

# Example route to get all types
@app.get("/types/", response_model=List[TypeResponse])
def get_all_types(db: Session = Depends(get_db)):
    types = get_all_items(db, Type)
    return types

# Example route to get a specific type by ID
@app.get("/types/{type_id}", response_model=TypeResponse)
def get_type_by_id(type_id: int, db: Session = Depends(get_db)):
    type_entity = get_item_by_id(db, Type, type_id)
    if type_entity:
        return type_entity
    raise HTTPException(status_code=404, detail="Type not found")

