import pytest
from database_connections import db_base
from utils import config_setup
from utils.simple_config import ConfigParse


@pytest.mark.usefixtures("init_driver")
class BaseTest:
    pass

    @staticmethod
    def org_info(config_entry):
        org_data = ConfigParse.org_info(config_entry)
        return org_data

    @staticmethod
    def config():
        file = config_setup.config()
        return file

    @staticmethod
    def master_config():
        file = config_setup.master_config()
        return file

    @staticmethod
    def establish_db_connection(my_shard=None):
        my_db = db_base.establish_connection(shard=my_shard)
        return my_db