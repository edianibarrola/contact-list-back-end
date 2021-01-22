from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=True)
    phone = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<Contact %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email

            # do not serialize the password, its a security breach
        }