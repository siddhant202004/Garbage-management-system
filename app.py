from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garbage_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Database Model
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    collection_date = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text, nullable=True)

# Create Home Route to Fix 404 Error
@app.route('/')
def home():
    return "Welcome to the Garbage Management System!"

# Route to Handle Form Submission
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_entry = Registration(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address'],
        category=data['category'],
        collection_date=data['collectionDate'],
        note=data.get('note', '')
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 201


# Route to Fetch All Registrations (Admin View)
@app.route('/admin/registrations', methods=['GET'])
def get_registrations():
    registrations = Registration.query.all()
    data = [{
        "id": reg.id,
        "name": reg.name,
        "email": reg.email,
        "phone": reg.phone,
        "address": reg.address,
        "category": reg.category,
        "collection_date": reg.collection_date,
        "note": reg.note
    } for reg in registrations]
    return jsonify(data), 200



# Run Flask App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created only when the app starts
    app.run(debug=True, port=5000)
    

print("Flask is running!")


#http://127.0.0.1:5000/admin/registrations for data visualization 