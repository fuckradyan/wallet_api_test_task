from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

import random
import uuid

from app.db import db
from app.services import process_wallet_operation, get_wallet_balance
from app.models import Wallet 

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
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
        return jsonify(new_wallet.to_dict())
    except SQLAlchemyError as e:
        db.session.rollback()
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
    
    except SQLAlchemyError:
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run()