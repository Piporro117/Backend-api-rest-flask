from flask import request, jsonify, make_response
from app.devices import device
from app.devices.models import Device
from datetime import timedelta
from app import db
from flask_jwt_extended import jwt_required

@device.route("/register", methods=["POST"])
#jwt_required()
def registrar_dispositivo():

    # obtenemos el json
    data: Device = request.get_json()

    required_fields: list[str] = ["dev_nombre", "dev_eui", "dev_num_ser",
        "dev_descr", "dev_tipo", "dev_estatus", "dev_lat", "dev_long"]
    
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Faltan datos"}), 400
    
    # verificar si la el nombre ya existe 
    if Device.query.filter_by(dev_nombre=data["dev_nombre"]).first():
        return jsonify({"error": "El nombre del dispositivo ya existe"}), 400
    
    # verificar si la el nombre ya existe 
    if Device.query.filter_by(dev_eui=data["dev_eui"]).first():
        return jsonify({"error": "El eui del dispositivo ya existe"}), 400
    
    try:
        device: Device = Device.create_device(
            dev_nombre=data["dev_nombre"],
            dev_eui=data["dev_eui"],
            dev_num_ser=data["dev_num_ser"],
            id_gateway=data["id_gateway"],
            id_zona=data["id_zona"],
            dev_descr=data["dev_descr"],
            dev_tipo=data["dev_tipo"],
            dev_lat=data["dev_lat"],
            dev_long=data["dev_long"],
            dev_estatus=data["dev_estatus"]            
        )

        return jsonify({
            "message": "Dispositivo creado con éxito",
            "dev_id": device.dev_id 
        }), 200

    except Exception as e:
        return jsonify({"error": "Error al registrar el dispositivo", "details": str(e)}), 500
    

# obtencion de dispositivo por id
@device.route("/obtenerDispositivo/<int:dev_id>", methods=["GET"])
@jwt_required()
def obtenerDispositivoPorId(dev_id: int):
    # obtenemos el dipsoitivo
    device: Device = Device.get_device_by_id(dev_id)

    if not device:
        return jsonify({'error': 'dispositivo no encontrado'}), 404
    
    return jsonify({
        "dev_id": device.dev_id,
        "dev_nombre": device.dev_nombre,
        "dev_eui": device.dev_eui,
        "dev_num_ser": device.dev_num_ser,
        "id_gateway": device.id_gateway,
        "id_zona": device.id_zona,
        "dev_descr": device.dev_descr,
        "dev_tipo": device.dev_tipo,
        "dev_lat": device.dev_lat,
        "dev_long": device.dev_long,
        "dev_estatus": device.dev_estatus,
        "created_date": device.created_date
    }), 200

# obtener todos los dispositivos
@device.route("/consultarDispositivos", methods=["GET"])
@jwt_required()
def obtener_dispositivos():

    dispositivos: list[Device] = Device.get_all_devices()

    dispositivosLista = [{
        "dev_id": dispositivo.dev_id,
        "dev_nombre": dispositivo.dev_nombre,
        "dev_eui": dispositivo.dev_eui,
        "dev_num_ser": dispositivo.dev_num_ser,
        "id_gateway": dispositivo.id_gateway,
        "id_zona": dispositivo.id_zona,
        "dev_descr": dispositivo.dev_descr,
        "dev_tipo": dispositivo.dev_tipo,
        "dev_lat": dispositivo.dev_lat,
        "dev_long": dispositivo.dev_long,
        "dev_estatus": dispositivo.dev_estatus,
        "created_date": dispositivo.created_date}
        for dispositivo in dispositivos    
    ]

    return jsonify(dispositivosLista), 200


# metodo para la edicion de un usaurio
@device.route("/editarDispositivo/<int:dev_id>", methods=["PUT"])
#@jwt_required()
def editar_dispositivo(dev_id: int):

    # obtenemos el json
    data = request.get_json()

    try:
        device: Device = Device.update_device_by_id(
            dev_id=dev_id,
            dev_nombre=data["dev_nombre"],
            dev_eui=data["dev_eui"],
            dev_num_ser=data["dev_num_ser"],
            id_gateway=data["id_gateway"],
            id_zona=data["id_zona"],
            dev_descr=data["dev_descr"],
            dev_tipo=data["dev_tipo"],
            dev_lat=data["dev_lat"],
            dev_long=data["dev_long"],
            dev_estatus=data["dev_estatus"]            
        )
        if not device:
            return jsonify({"error": "Dispositivo no encontrado"}), 404
        
        return jsonify({"message": "Dispositivo actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": "Error al actualizar dispositivo", "details": str(e)}), 500
    

# metodo de elimianr
@device.route("/eliminarDispositivo/<int:dev_id>", methods=["DELETE"])
#@jwt_required()  # si quieres protegerlo con token
def eliminar_dispositivo(dev_id):
    try:
        if not Device.delete_device_by_id(dev_id):
            return jsonify({"error": "Dispositivo no encontrado"}), 404

        return jsonify({"message": "Dispositivo eliminado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": "Error al eliminar Dispositivo", "details": str(e)}), 500