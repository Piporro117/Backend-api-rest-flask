from flask import request, jsonify
from app.responses import response
from app.responses.models import ResponseWater, SensorReading
from app.devices.models import Device
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
        return jsonify(None), 200 

    # if not response:
    #     return jsonify({'error': 'Respuesta no encontrada'}), 404
    
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
    



#----------------------- RUTAS DE NUEVA RESPUETSA DE LORAWAN-----------------------------

# guardar lectura
@response.route("/guardarLectura", methods=['POST'])
#@jwt_required()
def guardar_lectura():
    
    data: SensorReading = request.get_json()

    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    # guardamos la lectura
    try:
        lectura: SensorReading = SensorReading.create_reading(
            gateway_id=data.get("gateway_id"),
            raw_payload=data.get("raw_payload"),
            device_eui=data.get("device_eui"),
            function_code=data.get("function_code"),
            reporting_type=data.get("reporting_type"),
            device_has_valve=data.get("device_has_valve"),
            device_is_prepaid=data.get("device_is_prepaid"),
            device_power_source=data.get("device_power_source"),
            device_is_rechargeable=data.get("device_is_rechargeable"),
            device_class=data.get("device_class"),
            cumulative_flow_unit=data.get("cumulative_flow_unit"),
            instantaneous_flow_unit=data.get("instantaneous_flow_unit"),
            temperature_unit=data.get("temperature_unit"),
            cumulative_water_volume=data.get("cumulative_water_volume"),
            yesterday_cumulative_water_volume=data.get("yesterday_cumulative_water_volume"),
            instantaneous_flow=data.get("instantaneous_flow"),
            water_temperature=data.get("water_temperature"),
            big_alarm_min_flow_rate=data.get("big_alarm_min_flow_rate"),
            small_alarm_max_flow_rate=data.get("small_alarm_max_flow_rate"),
            alarm_reverse_flow=data.get("alarm_reverse_flow"),
            alarm_empty_pipe=data.get("alarm_empty_pipe"),
            alarm_low_power_warning=data.get("alarm_low_power_warning"),
            alarm_low_power=data.get("alarm_low_power"),
            alarm_flow_limit=data.get("alarm_flow_limit"),
            alarm_low_flow=data.get("alarm_low_flow"),
            alarm_high_water_temp=data.get("alarm_high_water_temp"),
            alarm_low_water_temp=data.get("alarm_low_water_temp"),
            alarm_low_water_level=data.get("alarm_low_water_level"),
            alarm_water_overdraft=data.get("alarm_water_overdraft"),
            alarm_water_overdraft_end=data.get("alarm_water_overdraft_end"),
            alarm_high_current=data.get("alarm_high_current"),
            alarm_small_flow=data.get("alarm_small_flow"),
            alarm_zero_balance=data.get("alarm_zero_balance"),
            valve_is_open=data.get("valve_is_open"),
            valve_is_closed=data.get("valve_is_closed"),
            valve_failure=data.get("valve_failure"),
            last_valve_command=data.get("last_valve_command"),
            total_uploads=data.get("total_uploads"),
            last_valve_actuation_time_sec=data.get("last_valve_actuation_time_sec"),
            valve_closing_count=data.get("valve_closing_count"),
            valve_opening_count=data.get("valve_opening_count"),
            rust_removal_count=data.get("rust_removal_count"),
            rust_removal_state=data.get("rust_removal_state"),
            flow_alarm_serial_number=data.get("flow_alarm_serial_number"),
        )

        return jsonify({
            "message": "Lectura creada con éxito",
            "id": lectura.id
        }), 200
    
    except Exception as e:
        return jsonify({"error": "Error al registrar lectura", "details": str(e)}), 500


# actualizar lectura
@response.route("/editarLectura/<int:reading_id>", methods=['PUT'])
#@jwt_required()
def actualizar_lectura(reading_id: int):

    data = request.get_json()

    try:
        lectura: SensorReading = SensorReading.update_reading_by_id(reading_id, **data)

        if not lectura:
            return jsonify({"error": "Lectura no encontrada"}), 404
        
        return jsonify({"message": "Lectura actualizada correctamente"}), 200
    except Exception as ex:
        return jsonify({"error": "Error al actualizar lectura", "details": str(ex)}), 500
    

# obtener lectura por lectura id
@response.route("/consultarLecturaPorId/<int:reading_id>", methods=['GET'])
@jwt_required()
def obtener_lectura_por_id(reading_id: int):

    lectura: SensorReading = SensorReading.get_reading_by_id(reading_id)

    if not lectura:
        return jsonify({"error": "Lectura no encontrada"}), 404
    
    return jsonify({c.name: getattr(lectura, c.name) for c in lectura.__table__.columns}), 200

# obtener todas las lecturas
@response.route("/consultarTodasLecturas", methods=['GET'])
@jwt_required()
def obtener_todas_lecturas():

    lecturas: list[SensorReading] = SensorReading.get_all_readings()
    lecturas_list = []

    for lectura in lecturas:
        lectura_dict = {c.name: getattr(lectura, c.name) for c in lectura.__table__.columns}

        dispositivo: Device = Device.get_device_by_num_ser(lectura.device_eui)

        # ✅ solo incluir si el dispositivo existe y tiene nombre
        if dispositivo and dispositivo.dev_nombre:
            lectura_dict["dev_nombre"] = dispositivo.dev_nombre
            lecturas_list.append(lectura_dict)

    return jsonify(lecturas_list), 200

    # lecturas: list[SensorReading] = SensorReading.get_all_readings()

    # # lecturas_list = [
    # #     {c.name: getattr(l, c.name) for c in l.__table__.columns}
    # #     for l in lecturas
    # # ]

    # lecturas_list = []

    # for lectura in lecturas:
    #     lectura_dict = {c.name: getattr(lectura, c.name) for c in lectura.__table__.columns}

    #     dispositivo: Device = Device.get_device_by_num_ser(lectura.device_eui)
    #     lectura_dict["dev_nombre"] = dispositivo.dev_nombre if dispositivo else None

    #     lecturas_list.append(lectura_dict)


    # return jsonify(lecturas_list), 200

# obtener lectura mas reciente por dev_eui
@response.route("/consultarLecturaRecientePorDevice/<string:device_eui>", methods=['GET'])
@jwt_required()
def obtener_lectura_reciente_por_dev_eui(device_eui: str):

    lectura: SensorReading = SensorReading.get_latest_reading_by_device_eui(device_eui)

    if not lectura:
        return jsonify(None), 200
    
    return jsonify({c.name: getattr(lectura, c.name) for c in lectura.__table__.columns}), 200


# obtener lecturas de un device _eui 
@response.route("/obtenerLecturasPorEUI/<string:device_eui>", methods=["GET"])
@jwt_required()
def obtener_lecturas_por_eui(device_eui: str):
    lecturas: list[SensorReading] = SensorReading.get_readings_by_device_eui(device_eui)

    lecturas_list = [
        {c.name: getattr(l, c.name) for c in l.__table__.columns}
        for l in lecturas
    ]

    return jsonify(lecturas_list), 200


# eliminar lectura por id
@response.route("/eliminarLecturaPorId/<int:reading_id>", methods=['GET'])
#@jwt_required()
def eliminar_lectura(reading_id: int):
    try:
        if not SensorReading.delete_reading_by_id(reading_id):
            return jsonify({"error": "Lectura no encontrada"}), 404

        return jsonify({"message": "Lectura eliminada con éxito"}), 200

    except Exception as e:
        return jsonify({"error": "Error al eliminar lectura", "details": str(e)}), 500
    
# obtener lecturas por gateway id
@response.route("/obtenerLecturasPorGateway/<string:gate_clave>", methods=["GET"])
@jwt_required()
def obtener_lecturas_por_gateway(gate_clave: str):
    lecturas: list[SensorReading] = SensorReading.get_reading_by_gateway_clave(gate_clave)

    lecturas_list = [
        {c.name: getattr(l, c.name) for c in l.__table__.columns}
        for l in lecturas
    ]

    return jsonify(lecturas_list), 200