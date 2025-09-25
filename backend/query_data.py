from app import app, db
from app import User, Journal, Article, CommunityPost  # Assuming models are in app.py

with app.app_context():
    db.create_all()  # Create tables if they don't exist

    print("=== USERS ===")
    users = User.query.all()
    if users:
        for u in users:
            print(f"ID: {u.id}, Username: {u.username}, Email: {u.email}")
    else:
        print("No users found.")

    print("\n=== JOURNALS ===")
    journals = Journal.query.all()
    if journals:
        for j in journals:
            print(f"ID: {j.id}, User ID: {j.user_id}, Title: {j.title}, Content: {j.content[:50]}..., Image: {j.image_url}")
    else:
        print("No journals found.")

    print("\n=== ARTICLES ===")
    articles = Article.query.all()
    if articles:
        for a in articles:
            print(f"ID: {a.id}, Title: {a.title}, Body: {a.body[:50]}...")
    else:
        print("No articles found.")

    print("\n=== COMMUNITY POSTS ===")
    posts = CommunityPost.query.all()
    if posts:
        for p in posts:
            print(f"ID: {p.id}, User ID: {p.user_id}, Content: {p.content[:50]}...")
    else:
        print("No community posts found.")
