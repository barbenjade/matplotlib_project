from utils import data_helpers

from utils import database_helpers

def get_provider_network_code(carrier, provider_full_name, date_time):
    provider_names = re.sub(',', '', provider_full_name).split(" ")
    providers_json_array = check_all_shards(f"select response_body from api_logs where api_name = 'plansource_find_a_provider' and request_body like 'carrier_code={carrier.lower()}%' and response_body like '%{provider_names[1]}%' and response_body like '%{provider_names[0]}%' and created_at > '{date_time}' order by created_at DESC")
    result = providers_json_array.split("},")
    data = list(result)
    record_array = [s for s in data if provider_names[0] in s and provider_names[1] in s]
    network_code = record_array[0].split("\"networkCode\":")[1].split(",\n")[0].strip()
    network_code = re.sub("\"", "", network_code)
    return network_code