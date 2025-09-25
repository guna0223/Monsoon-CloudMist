from flask import Blueprint, request, jsonify
from models.article import Article, db

bp = Blueprint('article', __name__)

@bp.route('/articles', methods=['GET', 'POST'])
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
