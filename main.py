from app import create_app, db
from app.auth.models import User

app = create_app("dev")

with app.app_context():
    db.create_all()

    if not User.query.filter_by(user_rol="admin").first():
        User.create_user(
            user_name="admin",
            user_ape_mat="admin",
            user_ape_pat="admin",
            user_rol="admin",
            user_email="admin@correo.com",
            user_estatus="1",
            user_telef="8712124203",
            password="admin"
        )
    

app.run(host="localhost", port=5000)

