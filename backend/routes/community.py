from flask import Blueprint, request, jsonify
from models.community_post import CommunityPost, db

bp = Blueprint('community', __name__)

@bp.route('/community', methods=['GET', 'POST'])
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
