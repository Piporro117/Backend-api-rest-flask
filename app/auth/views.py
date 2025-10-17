from flask import request, jsonify, make_response
from app.auth import authentication
from app.auth.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies
from datetime import timedelta
from app import db


@authentication.route("/register", methods=["POST"])
#@jwt_required()
def registrar_usuario():
    
    # obtenemos la data del post
    data = request.get_json()

    required_fields: list[str] = [ 
        "user_name", "user_ape_pat", "user_ape_mat",
        "user_email", "user_telef", "user_rol",
        "user_estatus", "password", "user_clave"
    ]

    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Faltan datos"}), 400

    # verificar si ya existe
    if User.query.filter_by(user_clave=data["user_clave"]).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    try:
        user = User.create_user(
            user_clave=data["user_clave"],
            user_name=data["user_name"],
            user_ape_pat=data["user_ape_pat"],
            user_ape_mat=data["user_ape_mat"],
            user_email=data["user_email"],
            user_telef=data["user_telef"],
            user_rol=data["user_rol"],
            user_estatus=data["user_estatus"],
            password=data["password"]
        )

        return jsonify({
            "message": "Usuario creado con éxito",
            "user_id": user.user_id
        }), 200
    except Exception as e:
        return jsonify({"error": "Error al registrar usuario", "details": str(e)}), 500
    

# Login pero con token como respuesta , sin ecriptacion
@authentication.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(user_clave=data.get("user_clave")).first()

    if user and user.check_password(data.get("password")):
        token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(hours=2))
        return jsonify({"message": "Login exitoso", "token": token}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401


# login que guarda el token como cookie y no puede accesar el front
@authentication.route("/loginCookie", methods=["POST"])
def loginConCookie():
    data = request.get_json()
    user: User = User.query.filter_by(user_clave=data.get("user_clave")).first()

    if user and user.check_password(data.get("password")):
        token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(hours=2))
        
        resp = make_response(jsonify({
        "user_id": user.user_id,
        "user_clave": user.user_clave,
        "user_name": user.user_name,
        "user_email": user.user_email,
        "created_date": user.created_date
    }), 200)
        set_access_cookies(resp, token, max_age=60*60*2)
        return resp

    return jsonify({"error": "Credenciales inválidas"}), 401


# Eliminacion de cookie
@authentication.route("/logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"message": "Logout exitoso"}), 200)
    unset_jwt_cookies(resp)  # borra tanto access como refresh token
    return resp


# Obtener usuario por ID
@authentication.route("/obtenerUsuario/<int:user_id>", methods=["GET"])
@jwt_required()
def profile(user_id):
    # obtenemos el usuario
    user: User = User.get_user_by_id(user_id)

    if not user:
        return jsonify({'error': 'usuario no encontrado'}), 404

    return jsonify({
        "user_id": user.user_id,
        "user_clave": user.user_clave,
        "user_name": user.user_name,
        "user_ape_pat": user.user_ape_pat,
        "user_ape_mat": user.user_ape_mat,
        "user_email": user.user_email,
        "user_telef": user.user_telef,
        "user_rol": user.user_rol,
        "user_estatus": user.user_estatus,
        "created_date": user.created_date
    }), 200


# obtener todos los usuarios
@authentication.route("/consultarUsuarios", methods=["GET"])
@jwt_required()
def obtener_usuarios():
    
    usuarios: list[User] = User.get_all_users()

    usuariosLista = [{
        "user_id": user.user_id,
        "user_clave": user.user_clave,
        "user_name": user.user_name,
        "user_ape_pat": user.user_ape_pat,
        "user_ape_mat": user.user_ape_mat,
        "user_email": user.user_email,
        "user_telef": user.user_telef,
        "user_rol": user.user_rol,
        "user_estatus": user.user_estatus,
        "created_date": user.created_date
        }
        for user in usuarios
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
#@jwt_required()
def editar_usuario(user_id):
    # obtenemos el json
    data = request.get_json() 

    try:
        user: User = User.update_user_by_id(
            user_id=user_id,
            user_name=data.get("user_name"),
            user_ape_pat=data.get("user_ape_pat"),
            user_ape_mat=data.get("user_ape_mat"),
            user_email=data.get("user_email"),
            user_telef=data.get("user_telef"),
            user_rol=data.get("user_rol"),
            user_estatus=data.get("user_estatus")
        )
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"message": "Usuario actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": "Error al actualizar usuario", "details": str(e)}), 500


# metodo de elimianr
@authentication.route("/eliminarUsuario/<int:user_id>", methods=["DELETE"])
#@jwt_required()  # si quieres protegerlo con token
def eliminar_usuario(user_id):
    try:
        if not User.delete_user(user_id):
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"message": "Usuario eliminado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": "Error al eliminar usuario", "details": str(e)}), 500
