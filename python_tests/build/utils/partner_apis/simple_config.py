from dataclasses import dataclass
from utils import config_setup


@dataclass
class ConfigParse:

    admin_username: "ConfigParse" = None
    admin_password: "ConfigParse" = None
    username: "ConfigParse" = None
    password: "ConfigParse" = None
    name: "ConfigParse" = None
    client_id: "ConfigParse" = None
    broker: "ConfigParse" = None
    org_code: "ConfigParse" = None

    @staticmethod
    def org_info(entry_name):

        if entry_name:
            """THIS IS CURRENTLY FOR ORG ENTRIES ONLY,
            pass in the entry for the org.  example: 'organizations.employee_le_eoi'"""
            data = config_setup.config()
            parent = entry_name.split(".")[0]
            child = entry_name.split(".")[1]
            p_data = data[parent]
            value = p_data[child]

            try:
                admin_username = value['admin_username']
            except KeyError:
                admin_username = None
            try:
                admin_password = value['admin_password']
            except KeyError:
                admin_password = None
            try:
                username = value['username']
            except KeyError:
                username = None
            try:
                password = value['password']
            except KeyError:
                password = None
            try:
                name = value['name']
            except KeyError:
                name = None
            try:
                client_id = value['client_id']
            except KeyError:
                client_id = None
            try:
                broker = value['broker']
            except KeyError:
                broker = None
            try:
                org_code = value['org_code']
            except KeyError:
                org_code = None

            org = ConfigParse(admin_username=admin_username, admin_password=admin_password,
                              username=username, password=password, name=name,
                              client_id=client_id, broker=broker, org_code=org_code)
            return org