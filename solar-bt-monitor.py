#!/usr/bin/env python3
from BTOneApp import BTOneApp
import logging 
import duallog
import configparser

# Read configuration file
config = configparser.ConfigParser()
config.read('solar-bt-monitor.ini')

# Set logging level
log_level = config.get('monitor', 'log_level', fallback='INFO')
if (log_level is None or log_level == "INFO"):
    level = logging.INFO
elif (log_level == "DEBUG"):
    level = logging.DEBUG
elif (log_level == "WARN"):
    level = logging.WARN
elif (log_level == "ERROR"):
    level = logging.ERROR

duallog.setup('solar-bt-monitor', minLevel=level, fileLevel=level, rotation='daily', keep=30)

mac_addr = config.get('monitor', 'mac_addr', fallback=None)
logging.debug("[CONFIG] mac_addr: {}".format(mac_addr))

alias = config.get('monitor', 'device_alias', fallback=None)
logging.debug("[CONFIG] alias: {}".format(alias))

adapter = config.get('monitor', 'adapter', fallback=None)
logging.debug("[CONFIG] adapter: {}".format(adapter))

reconnect = config.getboolean('monitor', 'reconnect', fallback=False)
logging.debug("[CONFIG] reconnect: {}".format(reconnect))

continuous = config.getboolean('monitor', 'continuous_monitor', fallback=False)
logging.debug("[CONFIG] continuous_monitor: {}".format(continuous))

interval = -1
if (continuous):
    interval = config.getint('monitor', 'data_read_interval', fallback=-1)
    logging.debug("[CONFIG] data_read_interval: {}".format(interval))

logger_type = config.get('monitor', 'data_logger', fallback='prometheus')
logging.debug("[CONFIG] logger_type: {}".format(logger_type))

if (mac_addr is None):
    logging.error("No configuration item for mac_addr. This configuration item is required.")
elif (alias is None):
    logging.error("No configuration item for device_alias.  This configuration item is required.")
elif (adapter is None):
    logging.error("No configuration item for adapter.  This configuration item is required.")
else:
    data_logger = None
    if (logger_type == 'prometheus'):
        from prometheus_logger import prometheus_logger
        data_logger = prometheus_logger()
    
    if (data_logger is not None):
        bt1 = BTOneApp("hci0", mac_addr, alias, data_logger.data_received_callback, auto_reconnect=reconnect, continuous=continuous, interval=interval)
        bt1.connect()

