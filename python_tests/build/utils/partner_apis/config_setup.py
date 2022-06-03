import json
import os
import toml
from typing import List

from pydantic import BaseModel


def master_config():
    current_path = os.path.join(os.path.dirname(__file__), "../config/master_config.json")
    with open(current_path) as mc_config:
        data = json.load(mc_config)
        return data


def config():
    """the master config environment needs to be 'dev', 'uat', 'rc', 'prod', or 'partner_dev'"""
    current_path = os.path.join(os.path.dirname(__file__), "../config/")
    env = master_config()['environment']
    with open(f"{current_path}{env}/{env}_config.toml") as config_file:
        data = toml.load(config_file)
    return data


class MasterConfig(BaseModel):
    browser: str
    environment: str
    options: List[str] = []
    version: str
    driver_exe_path: str = "manager"