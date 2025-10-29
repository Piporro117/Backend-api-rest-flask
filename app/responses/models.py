from datetime import datetime
from app import db

# Creacion de la tabla de respuestas
class ResponseWater(db.Model):
    __tablename__ = "responses_water"

    # atributos de la tabla
    resp_id: int = db.Column(db.Integer, primary_key=True)
    dev_eui: str = db.Column(db.String(100),nullable=False)
    resp_valv_estatus: str = db.Column(db.String(4))
    resp_fecha: datetime = db.Column(db.DateTime)
    resp_fluj_act: int = db.Column(db.Integer)
    resp_temp_agua : int = db.Column(db.Integer)
    resp_volt_bate : int = db.Column(db.Integer)
    resp_codigo : str = db.Column(db.String(100))
    created_date: datetime = db.Column(db.DateTime, default=datetime.now)


    # fucion para la creacion de una respuesta
    @classmethod
    def create_response(cls, dev_eui: str, resp_valv_estatus: str, resp_fecha: datetime,
                        resp_fluj_act: int, resp_temp_agua: int, resp_volt_bate: int, resp_codigo: str):
        
        response : ResponseWater = cls(
            dev_eui=dev_eui,
            resp_valv_estatus=resp_valv_estatus,
            resp_fecha=resp_fecha,
            resp_fluj_act=resp_fluj_act,
            resp_temp_agua=resp_temp_agua,
            resp_volt_bate=resp_volt_bate,
            resp_codigo=resp_codigo
        )

        db.session.add(response)
        db.session.commit()
        return response
    
    # funcion para actualizar respuesta 
    @classmethod
    def update_response_by_id(cls, resp_id: int, dev_eui: str, resp_valv_estatus: str, resp_fecha: datetime,
                        resp_fluj_act: int, resp_temp_agua: int, resp_volt_bate: int, resp_codigo: str):
        
        response: ResponseWater = cls.query.get(resp_id)

        if not response:
            return None
        
        response.dev_eui = dev_eui
        response.resp_valv_estatus = resp_valv_estatus
        response.resp_fecha = resp_fecha
        response.resp_fluj_act = resp_fluj_act
        response.resp_temp_agua = resp_temp_agua
        response.resp_volt_bate = resp_volt_bate
        response.resp_codigo = resp_codigo

        db.session.commit()
        return response
    
    # funcion para eliminar la respuetsa
    @classmethod
    def delete_response_by_id(cls, resp_id: int):

        response: ResponseWater = cls.query.get(resp_id)

        if response:
            db.session.delete(response)
            db.session.commit()
            return True
        return False
    
    # funcion para obtener la respuesta por id
    @classmethod
    def get_response_by_id(cls, resp_id: int):
        return cls.query.get(resp_id)
    
    # funcion para listar todas las respuestas
    @classmethod
    def get_all_response(cls):
        return cls.query.all()
    
    # funcion para listar respuestas por un dev_eui
    @classmethod
    def get_responses_by_dev_eui(cls, dev_eui: str):
        return cls.query.filter_by(dev_eui=dev_eui).order_by(cls.resp_fecha.desc()).all()
    
    # funcion para obtener la respuesta mas reciente de un dev_eui
    @classmethod
    def get_latest_response_by_dev_eui(cls, dev_eui: str):
        return cls.query.filter_by(dev_eui=dev_eui).order_by(cls.resp_fecha.desc()).first()



