from app import create_app, db

app = create_app("dev")

with app.app_context():
    db.create_all()
    

app.run(host="localhost", port=5000)