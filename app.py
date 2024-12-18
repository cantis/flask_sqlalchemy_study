from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the database instance
db = SQLAlchemy()

def create_app():
    """Application Factory"""
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register routes
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Flask App!"})

    @app.route('/users', methods=['POST'])
    def create_user():
        from models import User, Wallet
        data = request.json
        user = User(name=data['name'], email=data['email'])
        wallet = Wallet(balance=0.0, user=user)
        db.session.add(user)
        db.session.add(wallet)
        db.session.commit()
        return jsonify(user.to_dict()), 201

    @app.route('/transactions', methods=['POST'])
    def create_transaction():
        from models import Wallet, Transaction
        data = request.json
        wallet = Wallet.query.get(data['wallet_id'])
        if not wallet:
            return jsonify({"error": "Wallet not found"}), 404

        transaction = Transaction(amount=data['amount'], wallet=wallet)
        wallet.balance += data['amount']
        db.session.add(transaction)
        db.session.commit()
        return jsonify(transaction.to_dict()), 201

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        from models import User
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict())

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        from models import db
        db.create_all()
    app.run(debug=True)