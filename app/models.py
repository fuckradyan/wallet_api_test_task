from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Wallet(db.Model):
    __tablename__ = 'wallet'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def __init__(self, uuid, balance):
        self.uuid = uuid
        self.balance = balance


    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'balance': self.balance
        }
    
    
    def __repr__(self):
        return f'<Wallet {self.uuid}, balance: {self.balance}>'