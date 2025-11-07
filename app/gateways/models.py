from datetime import datetime
from app import db

# Creacion de tabla de gateways
class Gateway(db.Model):

    __tablename__ = "gateways"

    # atributos de tabla
    gate_id: int = db.Column(db.Integer, primary_key=True)
    gate_nombre: str = db.Column(db.String(100), unique=True, nullable=False)
    gate_clave: str = db.Column(db.String(100), unique=True, nullable=False, index=True)
    gate_calle: str = db.Column(db.String(100))
    gate_col: str = db.Column(db.String(100))
    gate_ciudad: str = db.Column(db.String(100))
    gate_estado:  str = db.Column(db.String(100))
    gate_num_ext: str = db.Column(db.String(10))
    gate_long: float = db.Column(db.Float)
    gate_lat:float = db.Column(db.Float)
    gate_estatus: str = db.Column(db.String(10))
    user_id: int = db.Column(db.Integer)
    created_date: datetime = db.Column(db.DateTime, default=datetime.now)


    # - funcion de crear un gateway
    @classmethod
    def create_gateway(cls, gate_nombre: str, gate_clave: str, gate_calle: str ,gate_col: str, gate_ciudad: str, 
                       gate_estado: str, gate_num_ext: str, gate_long: float, gate_lat: float, 
                       gate_estatus: str, user_id: int):

        gateway: Gateway = cls(
            gate_nombre=gate_nombre,
            gate_clave=gate_clave,
            gate_calle=gate_calle,
            gate_col=gate_col,
            gate_ciudad=gate_ciudad,
            gate_estado=gate_estado,
            gate_num_ext=gate_num_ext,
            gate_long=gate_long,
            gate_lat=gate_lat,
            gate_estatus=gate_estatus,
            user_id=user_id
        )

        db.session.add(gateway)
        db.session.commit()
        return gateway
    
    # funcion de actualizacion de gateway
    @classmethod
    def update_gateway_by_id(cls, gate_id: int ,gate_nombre: str, gate_clave: str, gate_calle: str ,gate_col: str, gate_ciudad: str, 
                       gate_estado: str, gate_num_ext: str, gate_long: float, gate_lat: float, 
                       gate_estatus: str, user_id: int):
        
        gateway: Gateway = cls.query.get(gate_id)

        if not gateway:
            return None
        
        # actualizacion del gateway
        gateway.gate_nombre = gate_nombre
        gateway.gate_clave = gate_clave
        gateway.gate_col = gate_col
        gateway.gate_calle = gate_calle
        gateway.gate_ciudad = gate_ciudad
        gateway.gate_estado = gate_estado
        gateway.gate_num_ext = gate_num_ext
        gateway.gate_long = gate_long
        gateway.gate_lat = gate_lat
        gateway.gate_estatus = gate_estatus
        gateway.user_id = user_id

        db.session.commit()
        return gateway
    
    # funcion de eliminar gateway
    @classmethod
    def delete_by_id(cls, gate_id: int):
        gateway = cls.query.get(gate_id)
        if gateway:
            db.session.delete(gateway)
            db.session.commit()
            return True
        return False
    
    # funcion para obtener un gateway por id
    @classmethod
    def get_gateway_by_id(cls, gate_id: int):
        return cls.query.get(gate_id)
    
    # funcion para obtener todos los gateway
    @classmethod
    def get_all_gateways(cls):
        return cls.query.all()
    
    # funcion para obtener gateway por gate_clave
    @classmethod
    def get_gateway_by_clave(cls, gate_clave: str):
        return cls.query.filter_by(gate_clave=gate_clave).first()
    
    # funcion para regresar gateways que tenga un usuario
    @classmethod
    def get_gateways_by_user_id(cls, user_id: int):
        return cls.query.filter_by(user_id=user_id)