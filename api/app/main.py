from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/api-pokemon'
db = SQLAlchemy(app)


#BDD
class Type(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    id = db.Column(db.Integer, nullable=False, unique=True, autoincrement=True)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, default=None)
    power = db.Column(db.Integer, default=None)
    accuracy = db.Column(db.Integer, default=None)
    max_life_point = db.Column(db.Integer, default=None)
    type_name = db.Column(db.String(20), db.ForeignKey('type.name'))
    
    type = db.relationship('Type', backref=db.backref('skills'))

class Pokemon(db.Model):
    id_pokedex = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    size = db.Column(db.Float, default=None)
    weight = db.Column(db.Float, default=None)
    stats = db.Column(db.Integer, default=None)
    image = db.Column(db.Text, default=None)
    types = db.Column(db.Integer, db.ForeignKey('type.id'))
    skills = db.Column(db.Integer, db.ForeignKey('skill.id'))
    
    type = db.relationship('Type', foreign_keys=[types], backref=db.backref('pokemons'))
    skill = db.relationship('Skill', foreign_keys=[skills], backref=db.backref('pokemons'))

# Routes
@app.route('/types', methods=['GET'])
def get_types():
    return jsonify({"message": "GET types"})

@app.route('/types', methods=['POST'])
def create_type():
    return jsonify({"message": "POST type"})

@app.route('/types/<type_name>', methods=['GET'])
def get_type(type_name):
    return jsonify({"message": f"GET type {type_name}"})

@app.route('/types/<type_name>', methods=['PUT'])
def update_type(type_name):
    return jsonify({"message": f"PUT type {type_name}"})

@app.route('/types/<type_name>', methods=['DELETE'])
def delete_type(type_name):
    return jsonify({"message": f"DELETE type {type_name}"})


if __name__ == '__main__':
    app.run(debug=True)
