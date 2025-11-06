from datetime import datetime
from app import db ,bcrypt

#Creacion de la tabla de usuarios
class User(db.Model):
    __tablename__ = "usuarios"

    # atributos de la tabla
    user_id : int = db.Column(db.Integer, primary_key=True)
    user_clave: str = db.Column(db.String(20), index=True)
    user_nombre: str = db.Column(db.String(20))
    user_email: str = db.Column(db.String(60), unique=True)
    user_telef: int = db.Column(db.Integer)
    user_rfc: str = db.Column(db.String(15), unique=True)
    user_rol: str = db.Column(db.String(20))
    user_calle: str = db.Column(db.String(100))
    user_col: str = db.Column(db.String(100))
    user_ciudad: str = db.Column(db.String(100))
    user_estado:  str = db.Column(db.String(100))
    user_num_ext: str = db.Column(db.String(10))
    user_estatus: str = db.Column(db.String(1))
    user_password: str = db.Column(db.String(80))
    created_date: datetime = db.Column(db.DateTime, default=datetime.now)

    # funcion para verificar la contraseña
    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.user_password, password)

    # funcion para crear un usuario
    @classmethod
    def create_user(cls,
                user_clave: str,
                user_nombre: str,
                user_email: str,
                user_telef: int,
                user_rol: str,
                user_rfc: str,
                user_calle: str,
                user_col: str,
                user_num_ext: str,
                user_ciudad: str,
                user_estado: str,
                user_estatus: str,
                password: str):
        
        usuario: User = cls(
        user_clave=user_clave,
        user_nombre=user_nombre,
        user_rfc=user_rfc,
        user_calle=user_calle,
        user_num_ext = user_num_ext,
        user_col=user_col,
        user_ciudad=user_ciudad,
        user_estado=user_estado,
        user_email=user_email,
        user_telef=user_telef,
        user_rol=user_rol,
        user_estatus=user_estatus,
        user_password=bcrypt.generate_password_hash(password).decode("utf-8")
        )
        
        db.session.add(usuario)
        db.session.commit()
        return usuario
    
    # metodo para actualziar usuario
    @classmethod
    def update_user_by_id(cls, user_id: int, user_nombre: str,
                user_email: str,
                user_telef: int,
                user_rol: str,
                user_rfc: str,
                user_calle: str,
                user_num_ext: str,
                user_col: str,
                user_ciudad: str,
                user_estado: str,
                user_estatus: str):
        
        usuario: User = cls.query.get(user_id)

        if not usuario:
            return None
        
        # actualizar campos de usaurio
        usuario.user_nombre = user_nombre
        usuario.user_email = user_email
        usuario.user_telef = user_telef
        usuario.user_rfc = user_rfc
        usuario.user_calle = user_calle
        usuario.user_num_ext = user_num_ext
        usuario.user_col = user_col,
        usuario.user_ciudad = user_ciudad
        usuario.user_estado = user_estado
        usuario.user_rol = user_rol
        usuario.user_estatus = user_estatus

        db.session.commit()
        return usuario
    
    # metodo para la actualizacion de la contraseña
    @classmethod
    def update_password_by_id(cls, user_id: int , current_password: str , new_password: str):
        usuario = cls.query.get(user_id)

        if not usuario:
            return None
        
        # verificacion de la contraseña
        if not bcrypt.check_password_hash(usuario.user_password, current_password):
            raise ValueError("la contraseña no coinciden")
        
        # actualizamos la contraseña
        usuario.user_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        db.session.commit()

        return True

    
    # metodo para eliminar usaurio
    @classmethod
    def delete_user(cls, user_id: int):
        usuario = cls.query.get(user_id)

        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        else:
            return False
        
    #metodo para obtener usuario por id
    @classmethod
    def get_user_by_id(cls, user_id: int):
        return cls.query.get(user_id)

    # metodo para obtener todos los usaurios  
    @classmethod
    def get_all_users(cls):
        return cls.query.all()
    
