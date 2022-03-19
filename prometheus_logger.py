from prometheus_client import start_http_server, Gauge
import logging 
from gpiozero import CPUTemperature

prometheus_map = {
    'battery_percentage': Gauge('solarshed_battery_percentage', 'Battery %'),
    'battery_voltage': Gauge('solarshed_battery_volts', 'Battery Voltage'),
    'battery_current': Gauge('solarshed_battery_current', 'Battery Current'),
    'controller_temperature': Gauge('solarshed_controller_temperature_celsius', 'Controller Temperature'),
    'battery_temperature': Gauge('solarshed_battery_temperature_celsius', 'Battery Temperature'),
    'load_voltage': Gauge('solarshed_load_volts', 'Load Voltage'),
    'load_current': Gauge('solarshed_load_amperes', 'Load Current'),
    'load_power': Gauge('solarshed_load_power_watts', 'Load Power'),
    'pv_voltage': Gauge('solarshed_solar_volts', 'Solar Voltage'),
    'pv_current': Gauge('solarshed_solar_amperes', 'Solar Current'),
    'pv_power': Gauge('solarshed_solar_watts', 'Solar Power'),
    'max_charging_power_today': Gauge('solarshed_max_charging_power_today', 'Solar Power'),
    'max_discharging_power_today': Gauge('solarshed_max_discharging_power_today', 'Solar Power'),
    'charging_amp_hours_today': Gauge('solarshed_charging_amp_hours_today', 'Solar Power'),
    'discharging_amp_hours_today': Gauge('solarshed_discharging_amp_hours_today', 'Solar Power'),
    'power_generation_today': Gauge('solarshed_power_generation_today', 'Solar Power'),
    'power_generation_total': Gauge('solarshed_power_generation_total', 'Solar Power'),
    'charging_status': Gauge('solarshed_controller_charging_state', 'Controller Charging State'),
    'pi_temp': Gauge('pi_temperature_celcius', 'Pi Temperature')
}

class prometheus_logger:
    def __init__(self):
        logging.info("Starting Prometheus Server")
        start_http_server(5000)

    def data_received_callback(self, data):
        for key in data:
            value = data[key]
            logging.info("{}: {}".format(key, value))
            gauge = prometheus_map[key]
            gauge.set(value)

            gauge = prometheus_map['pi_temp']
            pi_temp = CPUTemperature()
            gauge.set(pi_temp.temperature)
