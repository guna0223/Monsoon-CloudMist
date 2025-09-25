from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from otp_utils import generate_otp, send_otp_email

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monsoon.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key
db = SQLAlchemy(app)

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
    content = db.Column(db.Text, nullable=False)
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
    otp = generate_otp()
    session['otp'] = otp
    session['reg_data'] = data
    # Send OTP to email
    email_sent = send_otp_email(data['email'], otp)
    if email_sent:
        return jsonify({'message': 'OTP sent to email'})
    else:
        return jsonify({'message': 'Failed to send OTP'}), 500

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
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/journals', methods=['GET', 'POST'])
def journals():
    if request.method == 'POST':
        data = request.json
        journal = Journal(user_id=data['user_id'], content=data['content'])
        db.session.add(journal)
        db.session.commit()
        return jsonify({'message': 'Journal created'})
    else:
        journals = Journal.query.all()
        return jsonify([{'id': j.id, 'user_id': j.user_id, 'content': j.content, 'timestamp': j.timestamp} for j in journals])

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        data = request.json
        article = Article(title=data['title'], body=data['body'])
        db.session.add(article)
        db.session.commit()
        return jsonify({'message': 'Article created'})
    else:
        articles = Article.query.all()
        return jsonify([{'id': a.id, 'title': a.title, 'body': a.body, 'timestamp': a.timestamp} for a in articles])

@app.route('/community', methods=['GET', 'POST'])
def community():
    if request.method == 'POST':
        data = request.json
        post = CommunityPost(user_id=data['user_id'], content=data['content'])
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'Post created'})
    else:
        posts = CommunityPost.query.all()
        return jsonify([{'id': p.id, 'user_id': p.user_id, 'content': p.content, 'timestamp': p.timestamp} for p in posts])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
