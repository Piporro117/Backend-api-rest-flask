from flask import request, jsonify
from app.gateways import gateway
from app.gateways.models import Gateway
from app import db
from flask_jwt_extended import jwt_required


@gateway.route("/register", methods=["POST"])
#jwt_required()
def registrar_gateway():

    # obtenemos el json
    data: Gateway = request.get_json()

    required_fields: list[str] = ["gate_nombre", "gate_clave", "gate_calle", "gate_col",
                                  "gate_ciudad", "gate_estado", "gate_num_ext", "gate_long"
                                  ,"gate_lat", "gate_estatus", "user_id"]
    
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Faltan datos"}), 400
    
    if Gateway.query.filter_by(gate_clave=data["gate_clave"]).first():
        return jsonify({"error": "la clave del gateway ya existe"}), 400
    
    try:
        gateway: Gateway = Gateway.create_gateway(
            gate_nombre=data["gate_nombre"],
            gate_clave=data["gate_clave"],
            gate_calle=data["gate_calle"],
            gate_col=data["gate_col"],
            gate_ciudad=data["gate_ciudad"],
            gate_estado=data["gate_estado"],
            gate_num_ext=data["gate_num_ext"],
            gate_estatus=data["gate_estatus"],
            gate_lat=data["gate_lat"],
            gate_long=data["gate_long"],
            user_id=data["user_id"]
        )

        return jsonify({
            "message": "Gateway creado con éxito",
            "dev_id": gateway.gate_id 
        }), 200

    except Exception as e: 
        return jsonify({"error": "Error al registrar el gateway", "details": str(e)}), 500
    

@gateway.route("/obtenerGateway/<int:dev_id>", methods=["GET"])
@jwt_required()
def obtener_gateway_por_id(gate_id: int):

    # obtenemos el gateway
    gateway: Gateway = Gateway.get_gateway_by_id(gate_id)

    if not gateway:
        return jsonify({'error': 'gateway no encontrado'}), 404
    
    return jsonify({
        "gate_id": gateway.gate_id,
        "gate_nombre": gateway.gate_nombre,
        "gate_clave": gateway.gate_clave,
        "gate_calle": gateway.gate_calle,
        "gate_col": gateway.gate_col,
        "gate_ciudad": gateway.gate_ciudad,
        "gate_estado": gateway.gate_estado,
        "gate_num_ext": gateway.gate_num_ext,
        "gate_long": gateway.gate_long,
        "gate_lat": gateway.gate_lat,
        "gate_estatus": gateway.gate_estatus,
        "user_id": gateway.user_id,
        "created_date": gateway.created_date
    }), 200


@gateway.route("/obtenerGatewayClave/<string:gate_clave>", methods=["GET"])
@jwt_required()
def obtener_gateway_por_clave(gate_clave: str):
    # obtenemos el gateway
    gateway: Gateway = Gateway.get_gateway_by_clave(gate_clave)

    if not gateway:
        return jsonify({'error': 'gateway no encontrado'}), 404
    
    return jsonify({
        "gate_id": gateway.gate_id,
        "gate_nombre": gateway.gate_nombre,
        "gate_clave": gateway.gate_clave,
        "gate_calle": gateway.gate_calle,
        "gate_col": gateway.gate_col,
        "gate_ciudad": gateway.gate_ciudad,
        "gate_estado": gateway.gate_estado,
        "gate_num_ext": gateway.gate_num_ext,
        "gate_long": gateway.gate_long,
        "gate_lat": gateway.gate_lat,
        "gate_estatus": gateway.gate_estatus,
        "user_id": gateway.user_id,
        "created_date": gateway.created_date
    }), 200

@gateway.route("/consultarTodos", methods=["GET"])
@jwt_required()
def consultar_todos():

    gateways: list[Gateway] = Gateway.get_all_gateways()

    gatewaysLista = [{
        "gate_id": gateway.gate_id,
        "gate_nombre": gateway.gate_nombre,
        "gate_clave": gateway.gate_clave,
        "gate_calle": gateway.gate_calle,
        "gate_col": gateway.gate_col,
        "gate_ciudad": gateway.gate_ciudad,
        "gate_estado": gateway.gate_estado,
        "gate_num_ext": gateway.gate_num_ext,
        "gate_long": gateway.gate_long,
        "gate_lat": gateway.gate_lat,
        "gate_estatus": gateway.gate_estatus,
        "user_id": gateway.user_id,
        "created_date": gateway.created_date}
        for gateway in gateways
    ]

    return jsonify(gatewaysLista), 200

@gateway.route("/consultarTodoPorUsu/<int:user_id>", methods=["GET"])
@jwt_required()
def consultar_todos_por_user_id(user_id: int):

    gateways: list[Gateway] = Gateway.get_gateways_by_user_id(user_id)

    gatewaysLista = [{
        "gate_id": gateway.gate_id,
        "gate_nombre": gateway.gate_nombre,
        "gate_clave": gateway.gate_clave,
        "gate_calle": gateway.gate_calle,
        "gate_col": gateway.gate_col,
        "gate_ciudad": gateway.gate_ciudad,
        "gate_estado": gateway.gate_estado,
        "gate_num_ext": gateway.gate_num_ext,
        "gate_long": gateway.gate_long,
        "gate_lat": gateway.gate_lat,
        "gate_estatus": gateway.gate_estatus,
        "user_id": gateway.user_id,
        "created_date": gateway.created_date}
        for gateway in gateways
    ]

    return jsonify(gatewaysLista), 200


# modificar gateway
@gateway.route("/editarGateway/<int:gate_id>", methods=["PUT"])
#@jwt_required()
def editar_gateway_by_id(gate_id: int):

    # obtenemos json
    data: Gateway = request.get_json()

    try:

        gateway: Gateway = Gateway.update_gateway_by_id(
            gate_id=gate_id,
            gate_nombre=data["gate_nombre"],
            gate_clave=data["gate_clave"],
            gate_calle=data["gate_calle"],
            gate_col=data["gate_col"],
            gate_ciudad=data["gate_ciudad"],
            gate_estado=data["gate_estado"],
            gate_num_ext=data["gate_num_ext"],
            gate_estatus=data["gate_estatus"],
            gate_lat=data["gate_lat"],
            gate_long=data["gate_long"],
            user_id=data["user_id"]
        )

        if not gateway:
            return jsonify({"error": "Gateway no encontrado"}), 404
        
        return jsonify({"message": "Gateway actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": "Error al actualizar gateway", "details": str(e)}), 500
    
@gateway.route("/eliminarGateway/<int:gate_id>", methods=["DELETE"])
#@jwt_required()
def eliminar_gateway(gate_id: int):
    try:
        if not Gateway.delete_by_id(gate_id):
            return jsonify({"error": "Gateway no encontrado"}), 404

        return jsonify({"message": "Gateway eliminado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": "Error al eliminar Gateway", "details": str(e)}), 500
