from datetime import datetime
from app import db
from typing import Optional

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



############################ RESPUESTA DE BD DE EMPRESA LORAWAN
class SensorReading(db.Model):
    __tablename__ = "sensor_readings"

    id = db.Column(db.Integer, primary_key=True)
    received_at = db.Column(db.DateTime, default=datetime.now)
    gateway_id = db.Column(db.String)
    raw_payload = db.Column(db.String)
    device_eui = db.Column(db.String)
    function_code = db.Column(db.String)
    reporting_type = db.Column(db.String)
    device_has_valve = db.Column(db.Boolean)
    device_is_prepaid = db.Column(db.Boolean)
    device_power_source = db.Column(db.String)
    device_is_rechargeable = db.Column(db.Boolean)
    device_class = db.Column(db.String)
    cumulative_flow_unit = db.Column(db.String)
    instantaneous_flow_unit = db.Column(db.String)
    temperature_unit = db.Column(db.String)
    cumulative_water_volume = db.Column(db.Float)
    yesterday_cumulative_water_volume = db.Column(db.Float)
    instantaneous_flow = db.Column(db.Float)
    water_temperature = db.Column(db.Float)
    big_alarm_min_flow_rate = db.Column(db.Float)
    small_alarm_max_flow_rate = db.Column(db.Float)
    alarm_reverse_flow = db.Column(db.Boolean)
    alarm_empty_pipe = db.Column(db.Boolean)
    alarm_low_power_warning = db.Column(db.Boolean)
    alarm_low_power = db.Column(db.Boolean)
    alarm_flow_limit = db.Column(db.Boolean)
    alarm_low_flow = db.Column(db.Boolean)
    alarm_high_water_temp = db.Column(db.Boolean)
    alarm_low_water_temp = db.Column(db.Boolean)
    alarm_low_water_level = db.Column(db.Boolean)
    alarm_water_overdraft = db.Column(db.Boolean)
    alarm_water_overdraft_end = db.Column(db.Boolean)
    alarm_high_current = db.Column(db.Boolean)
    alarm_small_flow = db.Column(db.Boolean)
    alarm_zero_balance = db.Column(db.Boolean)
    valve_is_open = db.Column(db.Boolean)
    valve_is_closed = db.Column(db.Boolean)
    valve_failure = db.Column(db.Boolean)
    last_valve_command = db.Column(db.String)
    total_uploads = db.Column(db.Integer)
    last_valve_actuation_time_sec = db.Column(db.Integer)
    valve_closing_count = db.Column(db.Integer)
    valve_opening_count = db.Column(db.Integer)
    rust_removal_count = db.Column(db.Integer)
    rust_removal_state = db.Column(db.String)
    flow_alarm_serial_number = db.Column(db.Integer)


    @classmethod
    def create_reading(
        cls,
        gateway_id: Optional[str] = None,
        raw_payload: Optional[str] = None,
        device_eui: Optional[str] = None,
        function_code: Optional[str] = None,
        reporting_type: Optional[str] = None,
        device_has_valve: Optional[bool] = None,
        device_is_prepaid: Optional[bool] = None,
        device_power_source: Optional[str] = None,
        device_is_rechargeable: Optional[bool] = None,
        device_class: Optional[str] = None,
        cumulative_flow_unit: Optional[str] = None,
        instantaneous_flow_unit: Optional[str] = None,
        temperature_unit: Optional[str] = None,
        cumulative_water_volume: Optional[float] = None,
        yesterday_cumulative_water_volume: Optional[float] = None,
        instantaneous_flow: Optional[float] = None,
        water_temperature: Optional[float] = None,
        big_alarm_min_flow_rate: Optional[float] = None,
        small_alarm_max_flow_rate: Optional[float] = None,
        alarm_reverse_flow: Optional[bool] = None,
        alarm_empty_pipe: Optional[bool] = None,
        alarm_low_power_warning: Optional[bool] = None,
        alarm_low_power: Optional[bool] = None,
        alarm_flow_limit: Optional[bool] = None,
        alarm_low_flow: Optional[bool] = None,
        alarm_high_water_temp: Optional[bool] = None,
        alarm_low_water_temp: Optional[bool] = None,
        alarm_low_water_level: Optional[bool] = None,
        alarm_water_overdraft: Optional[bool] = None,
        alarm_water_overdraft_end: Optional[bool] = None,
        alarm_high_current: Optional[bool] = None,
        alarm_small_flow: Optional[bool] = None,
        alarm_zero_balance: Optional[bool] = None,
        valve_is_open: Optional[bool] = None,
        valve_is_closed: Optional[bool] = None,
        valve_failure: Optional[bool] = None,
        last_valve_command: Optional[str] = None,
        total_uploads: Optional[int] = None,
        last_valve_actuation_time_sec: Optional[int] = None,
        valve_closing_count: Optional[int] = None,
        valve_opening_count: Optional[int] = None,
        rust_removal_count: Optional[int] = None,
        rust_removal_state: Optional[str] = None,
        flow_alarm_serial_number: Optional[int] = None,
        received_at: Optional[datetime] = None,
    ) -> "SensorReading":
        reading = cls(
            gateway_id=gateway_id,
            raw_payload=raw_payload,
            device_eui=device_eui,
            function_code=function_code,
            reporting_type=reporting_type,
            device_has_valve=device_has_valve,
            device_is_prepaid=device_is_prepaid,
            device_power_source=device_power_source,
            device_is_rechargeable=device_is_rechargeable,
            device_class=device_class,
            cumulative_flow_unit=cumulative_flow_unit,
            instantaneous_flow_unit=instantaneous_flow_unit,
            temperature_unit=temperature_unit,
            cumulative_water_volume=cumulative_water_volume,
            yesterday_cumulative_water_volume=yesterday_cumulative_water_volume,
            instantaneous_flow=instantaneous_flow,
            water_temperature=water_temperature,
            big_alarm_min_flow_rate=big_alarm_min_flow_rate,
            small_alarm_max_flow_rate=small_alarm_max_flow_rate,
            alarm_reverse_flow=alarm_reverse_flow,
            alarm_empty_pipe=alarm_empty_pipe,
            alarm_low_power_warning=alarm_low_power_warning,
            alarm_low_power=alarm_low_power,
            alarm_flow_limit=alarm_flow_limit,
            alarm_low_flow=alarm_low_flow,
            alarm_high_water_temp=alarm_high_water_temp,
            alarm_low_water_temp=alarm_low_water_temp,
            alarm_low_water_level=alarm_low_water_level,
            alarm_water_overdraft=alarm_water_overdraft,
            alarm_water_overdraft_end=alarm_water_overdraft_end,
            alarm_high_current=alarm_high_current,
            alarm_small_flow=alarm_small_flow,
            alarm_zero_balance=alarm_zero_balance,
            valve_is_open=valve_is_open,
            valve_is_closed=valve_is_closed,
            valve_failure=valve_failure,
            last_valve_command=last_valve_command,
            total_uploads=total_uploads,
            last_valve_actuation_time_sec=last_valve_actuation_time_sec,
            valve_closing_count=valve_closing_count,
            valve_opening_count=valve_opening_count,
            rust_removal_count=rust_removal_count,
            rust_removal_state=rust_removal_state,
            flow_alarm_serial_number=flow_alarm_serial_number,
            received_at=received_at or datetime.utcnow(),
        )
        db.session.add(reading)
        db.session.commit()
        return reading

    @classmethod
    def update_reading_by_id(
        cls,
        reading_id: int,
        gateway_id: Optional[str] = None,
        raw_payload: Optional[str] = None,
        device_eui: Optional[str] = None,
        function_code: Optional[str] = None,
        reporting_type: Optional[str] = None,
        device_has_valve: Optional[bool] = None,
        device_is_prepaid: Optional[bool] = None,
        device_power_source: Optional[str] = None,
        device_is_rechargeable: Optional[bool] = None,
        device_class: Optional[str] = None,
        cumulative_flow_unit: Optional[str] = None,
        instantaneous_flow_unit: Optional[str] = None,
        temperature_unit: Optional[str] = None,
        cumulative_water_volume: Optional[float] = None,
        yesterday_cumulative_water_volume: Optional[float] = None,
        instantaneous_flow: Optional[float] = None,
        water_temperature: Optional[float] = None,
        big_alarm_min_flow_rate: Optional[float] = None,
        small_alarm_max_flow_rate: Optional[float] = None,
        alarm_reverse_flow: Optional[bool] = None,
        alarm_empty_pipe: Optional[bool] = None,
        alarm_low_power_warning: Optional[bool] = None,
        alarm_low_power: Optional[bool] = None,
        alarm_flow_limit: Optional[bool] = None,
        alarm_low_flow: Optional[bool] = None,
        alarm_high_water_temp: Optional[bool] = None,
        alarm_low_water_temp: Optional[bool] = None,
        alarm_low_water_level: Optional[bool] = None,
        alarm_water_overdraft: Optional[bool] = None,
        alarm_water_overdraft_end: Optional[bool] = None,
        alarm_high_current: Optional[bool] = None,
        alarm_small_flow: Optional[bool] = None,
        alarm_zero_balance: Optional[bool] = None,
        valve_is_open: Optional[bool] = None,
        valve_is_closed: Optional[bool] = None,
        valve_failure: Optional[bool] = None,
        last_valve_command: Optional[str] = None,
        total_uploads: Optional[int] = None,
        last_valve_actuation_time_sec: Optional[int] = None,
        valve_closing_count: Optional[int] = None,
        valve_opening_count: Optional[int] = None,
        rust_removal_count: Optional[int] = None,
        rust_removal_state: Optional[str] = None,
        flow_alarm_serial_number: Optional[int] = None,
        received_at: Optional[datetime] = None,
    ) -> Optional["SensorReading"]:
        reading = cls.query.get(reading_id)
        if not reading:
            return None

        # solo actualizamos los campos que no sean None
        if gateway_id is not None:
            reading.gateway_id = gateway_id
        if raw_payload is not None:
            reading.raw_payload = raw_payload
        if device_eui is not None:
            reading.device_eui = device_eui
        if function_code is not None:
            reading.function_code = function_code
        if reporting_type is not None:
            reading.reporting_type = reporting_type
        if device_has_valve is not None:
            reading.device_has_valve = device_has_valve
        if device_is_prepaid is not None:
            reading.device_is_prepaid = device_is_prepaid
        if device_power_source is not None:
            reading.device_power_source = device_power_source
        if device_is_rechargeable is not None:
            reading.device_is_rechargeable = device_is_rechargeable
        if device_class is not None:
            reading.device_class = device_class
        if cumulative_flow_unit is not None:
            reading.cumulative_flow_unit = cumulative_flow_unit
        if instantaneous_flow_unit is not None:
            reading.instantaneous_flow_unit = instantaneous_flow_unit
        if temperature_unit is not None:
            reading.temperature_unit = temperature_unit
        if cumulative_water_volume is not None:
            reading.cumulative_water_volume = cumulative_water_volume
        if yesterday_cumulative_water_volume is not None:
            reading.yesterday_cumulative_water_volume = yesterday_cumulative_water_volume
        if instantaneous_flow is not None:
            reading.instantaneous_flow = instantaneous_flow
        if water_temperature is not None:
            reading.water_temperature = water_temperature
        if big_alarm_min_flow_rate is not None:
            reading.big_alarm_min_flow_rate = big_alarm_min_flow_rate
        if small_alarm_max_flow_rate is not None:
            reading.small_alarm_max_flow_rate = small_alarm_max_flow_rate
        if alarm_reverse_flow is not None:
            reading.alarm_reverse_flow = alarm_reverse_flow
        if alarm_empty_pipe is not None:
            reading.alarm_empty_pipe = alarm_empty_pipe
        if alarm_low_power_warning is not None:
            reading.alarm_low_power_warning = alarm_low_power_warning
        if alarm_low_power is not None:
            reading.alarm_low_power = alarm_low_power
        if alarm_flow_limit is not None:
            reading.alarm_flow_limit = alarm_flow_limit
        if alarm_low_flow is not None:
            reading.alarm_low_flow = alarm_low_flow
        if alarm_high_water_temp is not None:
            reading.alarm_high_water_temp = alarm_high_water_temp
        if alarm_low_water_temp is not None:
            reading.alarm_low_water_temp = alarm_low_water_temp
        if alarm_low_water_level is not None:
            reading.alarm_low_water_level = alarm_low_water_level
        if alarm_water_overdraft is not None:
            reading.alarm_water_overdraft = alarm_water_overdraft
        if alarm_water_overdraft_end is not None:
            reading.alarm_water_overdraft_end = alarm_water_overdraft_end
        if alarm_high_current is not None:
            reading.alarm_high_current = alarm_high_current
        if alarm_small_flow is not None:
            reading.alarm_small_flow = alarm_small_flow
        if alarm_zero_balance is not None:
            reading.alarm_zero_balance = alarm_zero_balance
        if valve_is_open is not None:
            reading.valve_is_open = valve_is_open
        if valve_is_closed is not None:
            reading.valve_is_closed = valve_is_closed
        if valve_failure is not None:
            reading.valve_failure = valve_failure
        if last_valve_command is not None:
            reading.last_valve_command = last_valve_command
        if total_uploads is not None:
            reading.total_uploads = total_uploads
        if last_valve_actuation_time_sec is not None:
            reading.last_valve_actuation_time_sec = last_valve_actuation_time_sec
        if valve_closing_count is not None:
            reading.valve_closing_count = valve_closing_count
        if valve_opening_count is not None:
            reading.valve_opening_count = valve_opening_count
        if rust_removal_count is not None:
            reading.rust_removal_count = rust_removal_count
        if rust_removal_state is not None:
            reading.rust_removal_state = rust_removal_state
        if flow_alarm_serial_number is not None:
            reading.flow_alarm_serial_number = flow_alarm_serial_number
        if received_at is not None:
            reading.received_at = received_at

        db.session.commit()
        return reading

    @classmethod
    def delete_reading_by_id(cls, reading_id: int) -> bool:
        reading = cls.query.get(reading_id)
        if reading:
            db.session.delete(reading)
            db.session.commit()
            return True
        return False

    @classmethod
    def get_reading_by_id(cls, reading_id: int) -> Optional["SensorReading"]:
        return cls.query.get(reading_id)

    @classmethod
    def get_all_readings(cls):
        return cls.query.order_by(cls.received_at.desc()).all()

    @classmethod
    def get_readings_by_device_eui(cls, device_eui: str):
        return cls.query.filter_by(device_eui=device_eui).order_by(cls.received_at.desc()).all()

    @classmethod
    def get_latest_reading_by_device_eui(cls, device_eui: str):
        return cls.query.filter_by(device_eui=device_eui).order_by(cls.received_at.desc()).first()