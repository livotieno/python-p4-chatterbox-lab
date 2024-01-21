from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = []
    
    if request.method == "GET":
        for message in Message.query.all():
            messages.append(message.to_dict())
        
        response = make_response(jsonify(messages), 200)
        return(response)
    
    elif request.method == "POST": 
        data = request.get_json()               
        new_message = Message(body=data.get('body'), username=data.get('username'))
        # new_message = Message(body = request.form.get('body'), username = request.form.get('username'))
        
        db.session.add(new_message)
        db.session.commit()
        
        response = make_response(jsonify(new_message.to_dict()), 201)
        return(response)

@app.route('/messages/<int:id>', methods = ["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()
    if request.method == "GET":
        response = make_response(jsonify(message.to_dict()), 200)
        return(response)
    
    elif request.method == "PATCH":
        message = Message.query.filter_by(id = id).first()
        data = request.get_json()
        
        for attr in data:
            setattr(message, attr, data.get(attr))
            
        db.session.add(message) 
        db.session.commit() 
            
        response = make_response(jsonify(message.to_dict()))
        
        return(response)
    
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        
        response = make_response(
            jsonify({'deleted': True}),
            200,
        )
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
