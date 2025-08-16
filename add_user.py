from app import app, db, User

with app.app_context():
    u = User(username="testuser", password="testpass")
    db.session.add(u)
    db.session.commit()
    print("✅ User created successfully")

