from flask import Blueprint, request, jsonify
from models.journal import Journal, db

bp = Blueprint('journal', __name__)

@bp.route('/journals', methods=['GET', 'POST'])
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
