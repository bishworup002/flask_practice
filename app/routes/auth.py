from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.schemas import AuthSchema, UserSchema, PasswordResetRequestSchema, PasswordResetSchema
from marshmallow import ValidationError

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    schema = UserSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    user = User(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    schema = AuthSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@bp.route('/password-reset-request', methods=['POST'])
def password_reset_request():
    schema = PasswordResetRequestSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        # Generate and send reset token (implement this part)
        # For now, we'll just return a success message
        return jsonify({'message': 'Password reset instructions sent to your email'}), 200
    return jsonify({'message': 'Email not found'}), 404

@bp.route('/password-reset', methods=['POST'])
def password_reset():
    schema = PasswordResetSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Verify reset token and update password (implement this part)
    # For now, we'll just return a success message
    return jsonify({'message': 'Password reset successfully'}), 200