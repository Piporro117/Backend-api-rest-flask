from flask import request, jsonify, make_response
from app.responses import response
from app.responses.models import ResponseWater
from datetime import timedelta
from app import db
from flask_jwt_extended import jwt_required

# funcion para guardar
@response.route("/register", methods=["POST"])
#jwt_required()
def registrar_respuesta():

    # obtener el json
    data: ResponseWater = request.get_json()

    required_fields: list[str] = ["dev_eui", "resp_valv_estatus", "resp_fecha", "resp_fluj_act",
                                  "resp_temp_agua", "resp_volt_bate", "resp_codigo"]
    
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Faltan datos"}), 400
    
    try:
        response: ResponseWater = ResponseWater.create_response(
            dev_eui=data["dev_eui"],
            resp_valv_estatus=data["resp_valv_estatus"],
            resp_fecha=data["resp_fecha"],
            resp_fluj_act=data["resp_fluj_act"],
            resp_temp_agua=data["resp_temp_agua"],
            resp_volt_bate=data["resp_volt_bate"],
            resp_codigo=data["resp_codigo"]
        )

        return jsonify({
            "message": "Respuesta creado con éxito",
            "resp_id": response.resp_id 
        }), 200

    except Exception as e:
        return jsonify({"error": "Error al registrar respuesta", "details": str(e)}), 500
    
@response.route("/editarRespuesta/<int:resp_id>", methods=["PUT"])
#@jwt_required()
def editar_respuesta(resp_id : int):

    data: ResponseWater = request.get_json()

    try:
        response: ResponseWater = ResponseWater.update_response_by_id(
            resp_id=resp_id,
            dev_eui=data["dev_eui"],
            resp_valv_estatus=data["resp_valv_estatus"],
            resp_fecha=data["resp_fecha"],
            resp_fluj_act=data["resp_fluj_act"],
            resp_temp_agua=data["resp_temp_agua"],
            resp_volt_bate=data["resp_volt_bate"],
            resp_codigo=data["resp_codigo"]
        )

        if not response:
            return jsonify({"error": "Respuesta no encontrado"}), 404
        
        return jsonify({"message": "Respuesta actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": "Error al actualizar respuesta", "details": str(e)}), 500


@response.route("/obtenerRespuestaPorId/<int:resp_id>", methods=["GET"])
@jwt_required()
def obtener_respuesta_por_id(resp_id: int):

    # obtenemos la respuesta
    response: ResponseWater = ResponseWater.get_response_by_id(resp_id)

    if not response:
        return jsonify({'error': 'Respuesta no encontrado'}), 404
    
    return jsonify({
        "resp_id": response.resp_id,
        "dev_eui": response.dev_eui,
        "resp_valv_estatus": response.resp_valv_estatus,
        "resp_fecha": response.resp_fecha,
        "resp_fluj_act": response.resp_fluj_act,
        "resp_temp_agua": response.resp_temp_agua,
        "resp_volt_bate": response.resp_volt_bate,
        "resp_codigo": response.resp_codigo,
        "created_date": response.created_date,
    }), 200

@response.route("/obtenerRespuestaPorEUI/<string:dev_eui>", methods=["GET"])
@jwt_required()
def obtener_respuesta_por_dev_eui(dev_eui: str):

    # obtenemos la respuesta
    response: ResponseWater = ResponseWater.get_latest_response_by_dev_eui(dev_eui)

    if not response:
        return jsonify({'error': 'Respuesta no encontrado'}), 404
    
    return jsonify({
        "resp_id": response.resp_id,
        "dev_eui": response.dev_eui,
        "resp_valv_estatus": response.resp_valv_estatus,
        "resp_fecha": response.resp_fecha,
        "resp_fluj_act": response.resp_fluj_act,
        "resp_temp_agua": response.resp_temp_agua,
        "resp_volt_bate": response.resp_volt_bate,
        "resp_codigo": response.resp_codigo,
        "created_date": response.created_date,
    }), 200

@response.route("/obtenerRespuestas", methods=["GET"])
@jwt_required()
def obtener_todas_respuestas():

    responses: list[ResponseWater] = ResponseWater.get_all_response()

    responsesList = [
        {
        "resp_id": response.resp_id,
        "dev_eui": response.dev_eui,
        "resp_valv_estatus": response.resp_valv_estatus,
        "resp_fecha": response.resp_fecha,
        "resp_fluj_act": response.resp_fluj_act,
        "resp_temp_agua": response.resp_temp_agua,
        "resp_volt_bate": response.resp_volt_bate,
        "resp_codigo": response.resp_codigo,
        "created_date": response.created_date,
    }
    for response in responses
    ]

    return jsonify(responsesList), 200

@response.route("/obtenerRespuestasPorDevEui/<string:dev_eui>", methods=["GET"])
@jwt_required()
def obtener_todas_respuestas_por_dev_eui(dev_eui: str):

    responses: list[ResponseWater] = ResponseWater.get_responses_by_dev_eui(dev_eui)

    responsesList = [
        {
        "resp_id": response.resp_id,
        "dev_eui": response.dev_eui,
        "resp_valv_estatus": response.resp_valv_estatus,
        "resp_fecha": response.resp_fecha,
        "resp_fluj_act": response.resp_fluj_act,
        "resp_temp_agua": response.resp_temp_agua,
        "resp_volt_bate": response.resp_volt_bate,
        "resp_codigo": response.resp_codigo,
        "created_date": response.created_date,
    }
    for response in responses
    ]

    return jsonify(responsesList), 200

# metodo de elimianr
@response.route("/eliminarRespuesta/<int:resp_id>", methods=["DELETE"])
#@jwt_required()  
def eliminar_respuesta(resp_id: int):
    try:
        if not ResponseWater.delete_response_by_id(resp_id):
            return jsonify({"error": "Respuesta no encontrado"}), 404

        return jsonify({"message": "Respuesta eliminada con éxito"}), 200
    except Exception as e:
        return jsonify({"error": "Error al eliminar Respuesta", "details": str(e)}), 500