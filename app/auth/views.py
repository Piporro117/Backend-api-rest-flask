from flask import request, jsonify, make_response
from app.auth import authentication
from app.auth.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies
from datetime import timedelta
from app import db

@authentication.route("/register", methods=["POST"])
def registrar_usuario():
    
    # obtenemos la data del post
    data = request.get_json()

    print(data)

    if not data or not all(k in data for k in ("user_name", "user_email", "password")):
        return jsonify({"error": "Faltan datos"}), 400

    # verificar si ya existe
    if User.query.filter_by(user_email=data["user_email"]).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    user = User.create_user(
        user=data["user_name"],
        email=data["user_email"],
        password=data["password"]
    )
    return jsonify(), 200
    

# login que refresa el token en el front como json
@authentication.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(user_email=data.get("user_email")).first()

    if user and user.check_password(data.get("password")):
        token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(hours=2))
        return jsonify({"message": "Login exitoso", "token": token}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401

# login que guarda el token como cookie y no puede accesar el front
@authentication.route("/loginCookie", methods=["POST"])
def loginConCookie():
    data = request.get_json()
    user = User.query.filter_by(user_email=data.get("user_email")).first()

    if user and user.check_password(data.get("password")):
        token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(hours=2))
        
        resp = make_response(jsonify({
        "user_id": user.user_id,
        "user_name": user.user_name,
        "user_email": user.user_email,
        "created_date": user.created_date
    }), 200)
        set_access_cookies(resp, token, max_age=60*60*2)
        return resp

    return jsonify({"error": "Credenciales inválidas"}), 401


@authentication.route("/logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"message": "Logout exitoso"}), 200)
    unset_jwt_cookies(resp)  # borra tanto access como refresh token
    return resp


# Perfil (requiere token)
@authentication.route("/obtenerUsuario/<int:user_id>", methods=["GET"])
@jwt_required()
def profile(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'usuario no encontrado'}), 404

    return jsonify({
        "user_id": user.user_id,
        "user_name": user.user_name,
        "user_email": user.user_email,
        "created_date": user.created_date
    }), 200


# obtener todos los usuarios
@authentication.route("/consultarUsuarios", methods=["GET"])
@jwt_required()
def obtener_usuarios():
    
    usuarios = User.query.all()

    usuariosLista = [{
        "user_id": u.user_id,
        "user_name": u.user_name,
        "user_email": u.user_email,
        "created_date": u.created_date
        }
        for u in usuarios
    ]

    return jsonify(usuariosLista), 200
    

    
# funcion para checar que el token de usaurio sigue activo
@authentication.route("/me", methods=["GET"])
@jwt_required()
def verificacion_token():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    return jsonify({"user_id": user.user_id, "email": user.user_email})


# metodo para la edicion de un usaurio
@authentication.route("/editarUsuario/<int:user_id>", methods=["POST"])
def editar_usuario(user_id):
    data = request.get_json()  # Lo que mande el frontend en el body

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Actualizar solo los campos que vengan en el body
    if "user_name" in data:
        user.user_name = data["user_name"]
    if "user_email" in data:
        user.user_email = data["user_email"]

    try:
        db.session.commit()
        return jsonify({
            "message": "Usuario actualizado con éxito",
            "user": {
                "user_id": user.user_id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "created_date": user.created_date
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar usuario", "details": str(e)}), 500


# metodo de elimianr
@authentication.route("/eliminarUsuario/<int:user_id>", methods=["DELETE"])
#@jwt_required()  # si quieres protegerlo con token
def eliminar_usuario(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar usuario", "details": str(e)}), 500
