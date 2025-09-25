from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)

# Import models to register them with SQLAlchemy
from models.user import User
from models.journal import Journal
from models.article import Article
from models.community_post import CommunityPost

# Register blueprints
from routes.auth import bp as auth_bp
from routes.journal import bp as journal_bp
from routes.article import bp as article_bp
from routes.community import bp as community_bp

app.register_blueprint(auth_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(article_bp)
app.register_blueprint(community_bp)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
