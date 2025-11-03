from datetime import datetime
from app import db

# Creacion de la tabla de dispositivo
class Device(db.Model):
    __tablename__ = "devices"

    #atributos de la tabla
    dev_id: int = db.Column(db.Integer, primary_key=True)
    dev_nombre: str = db.Column(db.String(16), unique=True, nullable=False)
    dev_eui: str = db.Column(db.String(100), unique=True, nullable=False)
    dev_num_ser: str = db.Column(db.String(200))
    id_gateway: int = db.Column(db.Integer, nullable=True)
    id_zona: int = db.Column(db.Integer, nullable=True)
    dev_descr: str = db.Column(db.String(2000))
    dev_tipo: str = db.Column(db.String(20))
    dev_estatus : str = db.Column(db.String(1))
    created_date: datetime = db.Column(db.DateTime, default=datetime.now)

    # funcion para crear un dispositivo
    @classmethod
    def create_device(cls, dev_nombre: str, dev_eui: str, dev_num_ser: str,id_gateway: int ,id_zona: int,
                      dev_descr: str, dev_tipo: str, dev_estatus: str):

        device = cls(
            dev_nombre=dev_nombre,
            dev_eui=dev_eui,
            dev_num_ser=dev_num_ser,
            id_gateway=id_gateway,
            id_zona=id_zona,
            dev_descr=dev_descr,
            dev_tipo=dev_tipo,
            dev_estatus=dev_estatus
        )

        db.session.add(device)
        db.session.commit()
        return device

    # funcion para actualizar dispositivo
    @classmethod
    def update_device_by_id(cls, dev_id: int, dev_nombre: str, dev_eui: str, dev_num_ser: str,
                            id_gateway:int, id_zona: int, dev_descr: str, dev_tipo: str, dev_estatus: str):
        
        device: Device = cls.query.get(dev_id)
        if not device:
            return None

        device.dev_nombre = dev_nombre
        device.dev_eui = dev_eui
        device.dev_num_ser = dev_num_ser
        device.id_gateway = id_gateway
        device.id_zona = id_zona
        device.dev_descr = dev_descr
        device.dev_tipo = dev_tipo
        device.dev_estatus = dev_estatus

        db.session.commit()
        return device

    # funcion para eliminar dispositivo
    @classmethod
    def delete_device_by_id(cls, dev_id: int):
        device = cls.query.get(dev_id)
        if device:
            db.session.delete(device)
            db.session.commit()
            return True
        return False

    #  funcion para obtener dispositivo por id
    @classmethod
    def get_device_by_id(cls, dev_id: int):
        return cls.query.get(dev_id)

    # funcionn para listar todos los dispositivos
    @classmethod
    def get_all_devices(cls):
        return cls.query.all()
    

    # funcion para obtener el dispositivio por numero de serie
    @classmethod
    def get_device_by_num_ser(cls, dev_num_ser: str):
        return cls.query.filter_by(dev_num_ser=dev_num_ser).first()
        
