# Projet Pokémon API

Fait par Titouan FORAS

## Description du projet 

Le projet consiste à créer une API en python permettant la manipulation des données réparties en plusieurs éléments comme les types, les compétences et les pokémons

## Mise en place

### Prérequis

- Python 3
- FastAPI (Last Version)

### Installation

1. Clonez le repository :

```bash
git clone https://github.com/Svlmon/fastapi-api-pokemon.git
cd api
```

2. Activer l'environnement virtuel Python

Si l'environnement virtuel n'est pas installé 
```bash
python -m venv app-venv
```

Si l'environnement virtuel est installé 
```bash
.\venv\Scripts\activate
```

3. Installer les dépendances
   
```bash
pip install -r requirements.txt
```

4. Lancer l'API

```bash
uvicorn main:app --reload
```

API accessible à l'adresse http://localhost:8000

## Base de données 

### Création des tables

1. SQLite

Utilisation de SQLite pour simplifier le processus de connexion entre la base et le code python car la base se trouve dans un fichier donc il suffit d'importer le fichier dans notre environnement de travail pour pouvoir la manipuler.

J'ai utilisé DataGrip pour la création de ma base car le logiciel propose une création détaillé des modèles de bases et me permet de faire des modifications rapides et simples sur ma base de données.

   
2. Table Pokemon
   
```
CREATE TABLE "Pokemon" (
	"id_pokedex"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"size"	REAL,
	"weight"	REAL,
	"stats"	INTEGER,
	"image"	TEXT UNIQUE,
	"types"	INT ,
	"skills"	INT ,
	FOREIGN KEY("types") REFERENCES "Type"("id"),
	FOREIGN KEY("skills") REFERENCES "Skill"("id"),
	PRIMARY KEY("id_pokedex" AUTOINCREMENT)
)
```

2. Table Skill

```
CREATE TABLE "Skill" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL UNIQUE,
    "description"    TEXT,
    "power"    INTEGER,
    "accuracy"    INTEGER,
    "pp_max"    INTEGER,
    "type_name"    TEXT,
    FOREIGN KEY("type_name") REFERENCES "Type"("name"),
    PRIMARY KEY("id" AUTOINCREMENT)
)
```
3. Table Type
```
CREATE TABLE "Type" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
)
```

### Diagramme du schéma de données

![image](https://github.com/Svlmon/fastapi-api-pokemon/blob/main/api/asset/Model_BDD.png)

## Tests et fonctionnalités

### Postman

Utilisation de Postman car je suis plus familier avec le logiciel. Ce logiciel permet de tester des requêtes API.

Pour la démonstration, voici le lien Postman où on retrouve les 10 requêtes API : 

https://www.postman.com/titouanf/workspace/fastapi-pokemon






