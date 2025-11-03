from app import create_app, db
from app.auth.models import User
from app.responses.models import SensorReading
from app.devices.models import Device
#from app.responses.models import ResponseWater

app = create_app("dev")

with app.app_context():
    try:
        connection = db.engine.connect()
        print("✅ Conexión a la base de datos exitosa:", connection.engine.url)
        db.create_all()

        if not User.query.filter_by(user_rol="admin").first():
            User.create_user(
             user_clave="admin",
             user_name="admin",
             user_ape_mat="admin",
             user_ape_pat="admin",
             user_rol="admin",
             user_email="admin@correo.com",
             user_estatus="1",
             user_telef="87121",
             password="admin"
            )
    except Exception as e:
        print("❌ Error al conectar con la base de datos:")
        print(e)
    
    

app.run(host="localhost", port=5000)

