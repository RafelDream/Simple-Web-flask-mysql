from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nim = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    jurusan = db.Column(db.String(100), nullable=False)

    matakuliah = db.relationship('Matakuliah', backref='user', lazy=True)

class Matakuliah(db.Model):  
    __tablename__ = 'matakuliah'
    id = db.Column(db.Integer, primary_key=True)   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    kode_matkul = db.Column(db.String(20), nullable=False)
    matkul = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    nilai = db.Column(db.Float, nullable=False)

 
