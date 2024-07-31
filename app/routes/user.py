from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, UserRole
from app.schemas import UserSchema, UserUpdateSchema
from marshmallow import ValidationError

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != UserRole.ADMIN:
        return jsonify({'message': 'Unauthorized'}), 403

    users = User.query.all()
    schema = UserSchema(many=True)
    return jsonify(schema.dump(users)), 200

@bp.route('/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def user_operations(user_id):
    current_user = User.query.get(get_jwt_identity())
    target_user = User.query.get(user_id)

    if not target_user:
        return jsonify({'message': 'User not found'}), 404

    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    if request.method == 'GET':
        schema = UserSchema()
        return jsonify(schema.dump(target_user)), 200

    elif request.method == 'PUT':
        schema = UserUpdateSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        for key, value in data.items():
            if key == 'password':
                target_user.set_password(value)
            else:
                setattr(target_user, key, value)

        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200

    elif request.method == 'DELETE':
        if current_user.role != UserRole.ADMIN:
            return jsonify({'message': 'Unauthorized'}), 403

        db.session.delete(target_user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200