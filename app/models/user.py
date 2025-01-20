from app import db

class User(db.Model):
    __tablename__ = "USER"  # Matches the table name in the database

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
