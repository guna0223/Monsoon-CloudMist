from flask import Blueprint, request, jsonify, session, current_app
from models.user import User, db
from services.auth_service import generate_jwt
from otp_utils import generate_otp, send_otp_email

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    otp = generate_otp()
    session['otp'] = otp
    session['reg_data'] = data
    email_sent = send_otp_email(data['email'], otp)
    if email_sent:
        return jsonify({'message': 'OTP sent to email'})
    else:
        return jsonify({'message': 'Failed to send OTP'}), 500

@bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    user_otp = data.get('otp')
    if user_otp == session.get('otp'):
        reg_data = session.get('reg_data')
        user = User(username=reg_data['username'], email=reg_data['email'], password=reg_data['password'])
        db.session.add(user)
        db.session.commit()
        session.pop('otp', None)
        session.pop('reg_data', None)
        token = generate_jwt(user.id)
        return jsonify({'message': 'User registered successfully', 'token': token})
    else:
        return jsonify({'message': 'Invalid OTP'}), 400

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        token = generate_jwt(user.id)
        return jsonify({'message': 'Login successful', 'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401
