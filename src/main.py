"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# get all contacts
@app.route('/contacts', methods=['GET'])
def get_all():
    
    response_body = Contact.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    

    return jsonify(response_body), 200

@app.route('/contacts', methods=['POST'])
def add_contact():
    contact_info= request.get_json()
    new_contact= Contact(full_name=contact_info['full_name'], address= contact_info['address'], phone=contact_info['phone'], email=contact_info['email'], )
    db.session.add(new_contact)
    db.session.commit()
    response = Contact.query.all()
    response = list(map(lambda x: x.serialize(), response))

    return jsonify(response), 200

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact_to_delete = Contact.query.get(id)
    if contact_to_delete is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(contact_to_delete)
    db.session.commit()
    response = Contact.query.all()
    response = list(map(lambda x: x.serialize(), response))

    return jsonify(response), 200

@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact_to_update = Contact.query.get(id)
    if contact_to_update is None:
        raise APIException('User not found', status_code=404)
    body = request.get_json()
    if 'full_name' in body:
        contact_to_update.full_name = body['full_name']
    if 'address' in body:
        contact_to_update.address = body['address']
    if 'phone' in body:
        contact_to_update.phone = body['phone']
    if 'email' in body:
        contact_to_update.email = body['email']
    db.session.commit()
    response = Contact.query.all()
    response = list(map(lambda x: x.serialize(), response))
    
    return jsonify(response), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
