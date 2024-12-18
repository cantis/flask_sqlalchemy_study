from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

# Initialize the database instance
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    wallets = relationship('Wallet', back_populates='user')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "wallets": [wallet.to_dict() for wallet in self.wallets]
        }

class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='wallets')
    transactions = relationship('Transaction', back_populates='wallet')

    def to_dict(self):
        return {
            "id": self.id,
            "balance": self.balance,
            "user_id": self.user_id,
            "transactions": [transaction.to_dict() for transaction in self.transactions]
        }

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    wallet = relationship('Wallet', back_populates='transactions')

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "wallet_id": self.wallet_id
        }