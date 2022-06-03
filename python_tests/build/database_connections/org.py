from utils import database_helpers

def get_carrier_id_by_lookup_code(lookup_code):
    carrier_id = database_helpers.check_all_shards(f"SELECT id FROM carriers WHERE lookup_code = '{lookup_code}'")
    return carrier_id