from datetime import datetime
from app import db ,bcrypt

#Creacion de la tabla de usuarios
class User(db.Model):
    __tablename__ = "usuarios"

    # atributos de la tabla
    id : int = db.Column(db.Integer, primary_key=True)
    user_name: str = db.Column(db.String(20))
    user_email: str = db.Column(db.String(60), unique=True, index=True)
    user_password: str = db.Column(db.String(80))
    created_date: datetime = db.Column(db.DateTime, default=datetime.now)

    # funcion para verificar la contraseña
    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.user_password, password)

    # funcion para crear un usuario
    @classmethod
    def create_user(cls, user: str , email: str , password: str):
        usuario: User = cls(user_name=user,
                      user_email=email,
                      user_password=bcrypt.generate_password_hash(password).decode("utf-8")
                    )
        
        db.session.add(usuario)
        db.session.commit()
        return usuario
    
