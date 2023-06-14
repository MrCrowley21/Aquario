import numpy as np
import logging

MIN_PH = 6.5
MAX_PH = 7.5
MIN_TEMP = 22.5
MAX_TEMP = 27.7
AMMONIUM = 0.0
MIN_OXYGEN = 6.0
MAX_OXYGEN = 8.0
NITRATE_MAX = 50.0
DURITY_MIN = 65.0
DURITY_MAX = 200.0
MAX_TURBIDITY = 2.0


def check_parameter(sensor, value):
    try:
        quality = 0
        if sensor == "TEMPERATURE":
            quality = _check_temperature_parameter(value)
        elif sensor == "PH":
            quality = _check_ph_parameter(value)
        elif sensor == "OXYGEN":
            quality = _check_oxygen_parameter(value)
        elif sensor == "TURBIDITY":
            quality = _check_turbidity_parameter(value)
        elif sensor == "NITRATE":
            quality = _check_nitrate_parameter(value)
        elif sensor == "DURITY":
            quality = _check_durity_parameter(value)
        elif sensor == "AMMONIUM":
            quality = _check_ammonium_parameter(value)
        return quality
    except:
        logging.info(f'Wrong sensor data')
        return -1


def _compute_sigmoid(value):
    s = 1 / (1 + np.exp(-value))
    return s * 100


def _check_temperature_parameter(value):
    if value < MIN_TEMP:
        difference = MIN_TEMP - value
    elif value > MAX_TEMP:
        difference = MIN_TEMP - value
    else:
        return 100.0
    return 100.0 - compute_sigmoid(difference)


def _check_ph_parameter(value):
    if value < MIN_PH:
        difference = MIN_PH - value
    elif value > MAX_PH:
        difference = MAX_PH - value
    else:
        return 100.0
    return 100.0 - compute_sigmoid(difference)


def _check_durity_parameter(value):
    if value < DURITY_MIN:
        difference = DURITY_MIN - value
    elif value > DURITY_MAX:
        difference = DURITY_MAX - value
    else:
        return 100.0
    return 100.0 - compute_sigmoid(difference)


def _check_oxygen_parameter(value):
    if value < MIN_OXYGEN:
        difference = MIN_OXYGEN - value
    elif value > MAX_OXYGEN:
        difference = MAX_OXYGEN - value
    else:
        return 100.0
    return 100.0 - compute_sigmoid(difference)


def _check_ammonium_parameter(value):
    if value > AMMONIUM:
        return 100.0 - compute_sigmoid(value - AMMONIUM)
    return 100.0


def _check_nitrate_parameter(value):
    if value > NITRATE_MAX:
        return 100.0 - compute_sigmoid(value - NITRATE_MAX)
    return 100.0


def _check_turbidity_parameter(value):
    if value > MAX_TURBIDITY:
        return 100.0 - compute_sigmoid(value - MAX_TURBIDITY)
    return 100.0


def get_system_state(sensor_values):
    general_state = 0
    for value in sensor_values:
        general_state += value
    general_state /= len(sensor_values)
    return "{:.3f}".format(general_state)


def get_ideal_sensor_value(sensor):
    try:
        value = 0
        if sensor == "TEMPERATURE":
            value = "{:.3f}".format((MAX_TEMP + MIN_TEMP) / 2)
        elif sensor == "PH":
            value = "{:.3f}".format((MAX_PH + MIN_PH) / 2)
        elif sensor == "OXYGEN":
            value = "{:.3f}".format((MAX_OXYGEN + MIN_OXYGEN) / 2)
        elif sensor == "TURBIDITY":
            value = 0.0
        elif sensor == "NITRATE":
            value = 0.0
        elif sensor == "DURITY":
            value = "{:.3f}".format((DURITY_MAX + DURITY_MIN) / 2)
        elif sensor == "AMMONIUM":
            value = 0.0
        return value
    except:
        logging.info(f'Wrong sensor data')
        return -1
