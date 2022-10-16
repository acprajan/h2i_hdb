import json
import logging

def get_config_data(env='dev'):
    with open('config.json', 'r') as cfg_data : config_data = json.load(cfg_data)
    return config_data[env]

def get_config_params_info():
    with open('config.json', 'r') as cfg_data : config_data = json.load(cfg_data)
    return config_data["params"]

def get_logger():
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
    return logging
    