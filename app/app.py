from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

import random
import uuid


from app.models import Wallet 

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def hello():
    try:
        wallets = db.session.query(Wallet).all()
        return jsonify([wallet.to_dict() for wallet in wallets])
    except Exception as e:
        return jsonify({'error' : f"{e}"})

@app.route('/addwallet')
def addwallet():
    try:
        new_wallet = Wallet(uuid.uuid4().__str__(),random.randint(1,10000))
        db.session.add(new_wallet)
        db.session.commit()
        return (new_wallet.uuid)
    except SQLAlchemyError as e:
        db.session.rollback()
        return None


def get_wallet_balance(wallet_uuid):
    try:
        wallet = db.session.query(Wallet).filter(Wallet.uuid == wallet_uuid).first()
        return wallet.balance
    except:
        return None
    

@app.route('/api/v1/wallets/<wallet_uuid>', methods=['GET'])
def get_balance(wallet_uuid):
    try:
        balance = get_wallet_balance(wallet_uuid)
        if not balance:
            return jsonify({'error': 'Wallet not found'}), 404
        return jsonify({'balance': balance}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Database error'}), 500


def process_wallet_operation(wallet_uuid, operation_type, amount):

    # try:
    if operation_type not in ('DEPOSIT', 'WITHDRAW'):
        raise ValueError("Invalid operation type")
    if type(int()) != type(amount) or amount <= 0:
        raise ValueError("Amount must be int and greater than 0")
    
    wallet = db.session.query(Wallet).filter_by(uuid=wallet_uuid).with_for_update().first()
        
    if not wallet:
        return ValueError("Wallet not found")
    if operation_type == 'WITHDRAW' and wallet.balance < amount:
        raise ValueError("Insufficient balance")
    
    new_balance = wallet.balance + amount if operation_type == 'DEPOSIT' else wallet.balance - amount
    wallet.balance = new_balance
    db.session.commit() 
    
    return {'balance': new_balance}

    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     return {'Database error' : f'{e}'}, 500
    # except Exception as e:
    #     return {'error' : f'{e}'}, 400


@app.route('/api/v1/wallets/<wallet_uuid>/operation', methods=['POST'])
def wallet_operation(wallet_uuid):
    try:
        data = request.get_json()
        operation_type = data.get('operation_type')
        amount = data.get('amount')
        
        if not operation_type or amount is None:
            return jsonify({'error': 'Missing required fields'}), 400
            
        new_balance = process_wallet_operation(
            wallet_uuid,
            operation_type,
            amount
        )
        return jsonify(new_balance), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError:
        return jsonify({'error': 'Database error'}), 500


if __name__ == '__main__':
    app.run()