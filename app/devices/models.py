from datetime import datetime
from app import db

# Creacion de la tabla de dispositivo
class Device(db.Model):
    __tablename__ = "devices"

    #atributos de la tabla
    dev_id: int = db.Column(db.Integer, primary_key=True)
    id_zona = db.Column(db.Integer)
    dev_clave: str = db.Column(db.String(100))
    dev_descr: str = db.Column(db.String(2000))
    dev_tipo: str = db.Column(db.String(20))
    dev_estatus : str = db.Column(db.String(1))
    created_date: datetime = db.Column(db.DateTime, default=datetime.now)

    # funcion para crear un dispositivo
    @classmethod
    def create_device(cls, id_zona: int, dev_clave: str, dev_descr: str, dev_tipo: str, dev_estatus: str):

        device: Device = cls(
            id_zona=id_zona,
            dev_clave=dev_clave,
            dev_descr=dev_descr,
            dev_tipo=dev_tipo,
            dev_estatus=dev_estatus
        )

        db.session.add(device)
        db.session.commit()
        return device
    
    # funcion para actualizar dispositivo
    @classmethod
    def update_device_by_id(cls, dev_id: int, id_zona: int, dev_clave: str, dev_descr: str, dev_tipo: str, dev_estatus: str):

        device: Device = cls.query.get(dev_id)

        if not device:
            return None
        
        # actualizamos los datos del dispositivos
        device.id_zona = id_zona
        device.dev_clave = dev_clave
        device.dev_descr = dev_descr
        device.dev_tipo = dev_tipo
        device.dev_estatus = dev_estatus

        db.session.commit()
        return device
    
    # funcion para la eliminacion de un dispositivo
    @classmethod
    def delete_device_by_id(cls, dev_id: int):
        device = cls.query.get(dev_id)

        if device:
            db.session.delete(device)
            db.session.commit()
            return True
        else:
            return False
        
    
    # funcion para obtener device por id
    @classmethod
    def get_device_by_id(cls, dev_id: int):
        return cls.query.get(dev_id)
    
    # funcion para listar todos los dispositivos
    @classmethod
    def get_all_devices(cls):
        return cls.query.all()



    