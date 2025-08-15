from app.db import db
from app.models import Wallet

def process_wallet_operation(wallet_uuid, operation_type, amount):
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

def get_wallet_balance(wallet_uuid):
    try:
        wallet = db.session.query(Wallet).filter(Wallet.uuid == wallet_uuid).first()
        return wallet.balance
    except:
        return None
    