from app import create_app, db
from app.auth.models import User
from app.responses.models import SensorReading
from app.devices.models import Device
from app.gateways.models import Gateway
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
                user_nombre="admin",
                user_rol="admin",
                user_email="admin@correo.com",
                user_telef="0000000000",
                user_rfc="XXX000000XXX",
                user_calle="S/N",
                user_col="Centro",
                user_num_ext="0",
                user_ciudad="Sin ciudad",
                user_estado="Sin estado",
                user_estatus="1",
                password="admin"
            )


        if not Gateway.query.filter_by(gate_clave="parque-centenario-01").first():
            Gateway.create_gateway(
                gate_nombre="Parque centenario 01",
                gate_clave="parque-centenario-01",
                gate_calle="Carretera a Mieleras",
                gate_ciudad="Matamoros",
                gate_estado="Coahuila",
                gate_num_ext="S/N",
                gate_col=None,
                gate_long=25.455341,
                gate_lat=-103.318396,
                gate_estatus="1",
                user_id=2
            )

        if not User.query.filter_by(user_clave="pcentenario01").first():
            User.create_user(
                user_clave="pcentenario01",
                user_nombre="Parque centenario 01",
                user_rol="estan",
                user_email="contacto@4ti.io",
                user_telef="0000010000",
                user_rfc="XXX00000XXXX",
                user_calle="S/N",
                user_col="Centro",
                user_num_ext="0",
                user_ciudad="Sin ciudad",
                user_estado="Sin estado",
                user_estatus="1",
                password="pcentenario01.!"
            )

        if not Device.query.filter_by(dev_eui="0095690600058B42").first():
            Device.create_device(
                dev_nombre="VOSS Automotive",
                dev_num_ser="70666100019109",
                dev_eui="0095690600058B42",
                dev_descr="VOSS Automotive México",
                dev_estatus="1",
                dev_long=25.454925,
                dev_lat=-103.318244,
                dev_tipo="agu",
                id_gateway=1,
                id_zona=None
            )
        
    except Exception as e:
        print("❌ Error al conectar con la base de datos:")
        print(e)
    
    

app.run(host="localhost", port=5000)

