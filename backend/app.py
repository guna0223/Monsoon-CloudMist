from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from otp_utils import generate_otp, send_otp_email
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
mail = Mail(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define directories relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Journal model
class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# Article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# Community Post model
class CommunityPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    data['password'] = hashed_password
    otp = generate_otp()
    print(f"Generated OTP for testing: {otp}")  # Print OTP for dev testing
    session['otp'] = otp
    session['reg_data'] = data
    # Send OTP to email (silent fail for dev)
    send_otp_email(data['email'], otp)
    return jsonify({'message': 'OTP ready (check console if email fails)'}), 200

# OTP verification endpoint
@app.route('/verify-otp', methods=['POST'])
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
        return jsonify({'message': 'User registered successfully'})
    else:
        return jsonify({'message': 'Invalid OTP'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'message': 'User not found. Please register first.'}), 401
    if check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login successful', 'access_token': access_token})
    return jsonify({'message': 'invalide username'}), 401

@app.route('/journals', methods=['GET', 'POST'])
@jwt_required()
def journals():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')
        image_url = None
        if image:
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            image_url = f'/uploads/{filename}'
        journal = Journal(user_id=user_id, title=title, content=content, image_url=image_url)
        db.session.add(journal)
        db.session.commit()
        return jsonify({'message': 'Journal created'})
    else:
        journals = Journal.query.all()
        return jsonify([{'id': j.id, 'user_id': j.user_id, 'title': j.title, 'content': j.content, 'image_url': j.image_url, 'timestamp': j.timestamp} for j in journals])

@app.route('/user-journals', methods=['GET'])
@jwt_required()
def user_journals():
    user_id = get_jwt_identity()
    journals = Journal.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': j.id, 'title': j.title, 'content': j.content, 'image_url': j.image_url, 'timestamp': j.timestamp} for j in journals])

@app.route('/user-profile', methods=['GET'])
@jwt_required()
def user_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    journal_count = Journal.query.filter_by(user_id=user_id).count()
    return jsonify({'username': user.username, 'journal_count': journal_count})

@app.route('/journals/<int:journal_id>', methods=['PUT'])
@jwt_required()
def update_journal(journal_id):
    user_id = get_jwt_identity()
    journal = Journal.query.get_or_404(journal_id)
    if journal.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    title = request.form.get('title', journal.title)
    content = request.form.get('content', journal.content)
    image = request.files.get('image')
    if image:
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        journal.image_url = f'/uploads/{filename}'
    journal.title = title
    journal.content = content
    db.session.commit()
    return jsonify({'message': 'Journal updated'})

@app.route('/articles', methods=['GET', 'POST'])
@jwt_required()
def articles():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        data = request.json
        article = Article(title=data['title'], body=data['body'])
        db.session.add(article)
        db.session.commit()
        return jsonify({'message': 'Article created'})
    else:
        articles = Article.query.all()
        return jsonify([{'id': a.id, 'title': a.title, 'body': a.body, 'timestamp': a.timestamp} for a in articles])

@app.route('/community', methods=['GET', 'POST'])
@jwt_required()
def community():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        data = request.json
        post = CommunityPost(user_id=user_id, content=data['content'])
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'Post created'})
    else:
        posts = CommunityPost.query.all()
        return jsonify([{'id': p.id, 'user_id': p.user_id, 'content': p.content, 'timestamp': p.timestamp} for p in posts])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    print(f"Frontend DIR: {FRONTEND_DIR}")
    print(f"Index path: {os.path.join(FRONTEND_DIR, 'index.html')}")
    print(f"Exists: {os.path.exists(os.path.join(FRONTEND_DIR, 'index.html'))}")
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('backend/'):
        return send_from_directory(BACKEND_DIR, path.replace('backend/', ''))
    else:
        print(f"Serving frontend file: {path}")
        print(f"Path exists: {os.path.exists(os.path.join(FRONTEND_DIR, path))}")
        return send_from_directory(FRONTEND_DIR, path)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Pre-create the specific user if not exists
        user = User.query.filter_by(username='gunasekarpeace@gmail.com').first()
        if not user:
            hashed_password = generate_password_hash('12345')
            user = User(username='gunasekarpeace@gmail.com', email='gunasekarpeace@gmail.com', password=hashed_password)
            db.session.add(user)
            db.session.commit()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
