# ------------------------------------------------------
# Original Author: Scott Nichol
# https://github.com/snichol67/solar-bt-monitor
#
# This small module sets up several prometheus gauges
# and starts the prometheus server on port 5000.  The
# prometheus_logger class provides a method that is 
# used as a callback for when data is received by the
# bluetooth modules.
#
# When data is received, we set a value on each of the 
# mapped gauges, pushing them into the prometheus store.
#
# Feel free to reuse this code for any purpose
# ------------------------------------------------------
from prometheus_client import start_http_server, Gauge
import logging 
from gpiozero import CPUTemperature

prometheus_map = {
    'battery_percentage': Gauge('solarmon_battery_percentage', 'Battery %'),
    'battery_voltage': Gauge('solarmon_battery_volts', 'Battery Voltage'),
    'battery_current': Gauge('solarmon_battery_current', 'Battery Current'),
    'controller_temperature': Gauge('solarmon_controller_temperature_celsius', 'Controller Temperature'),
    'battery_temperature': Gauge('solarmon_battery_temperature_celsius', 'Battery Temperature'),
    'load_voltage': Gauge('solarmon_load_volts', 'Load Voltage'),
    'load_current': Gauge('solarmon_load_amperes', 'Load Current'),
    'load_power': Gauge('solarmon_load_power_watts', 'Load Power'),
    'pv_voltage': Gauge('solarmon_solar_volts', 'Solar Voltage'),
    'pv_current': Gauge('solarmon_solar_amperes', 'Solar Current'),
    'pv_power': Gauge('solarmon_solar_watts', 'Solar Power'),
    'max_charging_power_today': Gauge('solarmon_max_charging_power_today', 'Solar Power'),
    'max_discharging_power_today': Gauge('solarmon_max_discharging_power_today', 'Solar Power'),
    'charging_amp_hours_today': Gauge('solarmon_charging_amp_hours_today', 'Solar Power'),
    'discharging_amp_hours_today': Gauge('solarmon_discharging_amp_hours_today', 'Solar Power'),
    'power_generation_today': Gauge('solarmon_power_generation_today', 'Solar Power'),
    'power_generation_total': Gauge('solarmon_power_generation_total', 'Solar Power'),
    'charging_status': Gauge('solarmon_controller_charging_state', 'Controller Charging State'),
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
