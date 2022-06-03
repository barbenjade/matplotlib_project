from database_connections import db_base
import time
import re


def check_all_shards(sql_query, attempts=10, return_list=False):
    """If you want to return all values that match your query, set return_list to True"""
    result = None
    count = 0
    shards = range(0, 4)
    while (not result or result == '') and count < attempts:
        for i in shards:
            my_db = db_base.establish_connection(shard=i)
            cursor = my_db.cursor()
            cursor.execute(sql_query)
            if return_list:
                var = cursor.fetchall()
                while var:
                    result = list(map(lambda x: x[0], var))
                    if result:
                        break
                if result:
                    break
            else:
                var = cursor.fetchone()
                while var:
                    result = var[0]
                    if result:
                        break
                if result:
                    break
            i += 1
        count += 1
    return result

def get_job_id(job_request_type_id, entity_id, test_start_time):
    count = 0
    job_request_id = check_shard_zero(f'''SELECT id FROM job_requests WHERE job_request_type_id = "{job_request_type_id}"
            AND entity_id = "{entity_id}"
            AND created_at > "{test_start_time}"''')
    while not job_request_id and count <= 600:
        time.sleep(5); count+=1
        job_request_id = check_shard_zero(f'''SELECT id FROM job_requests WHERE job_request_type_id = "{job_request_type_id}"
                    AND entity_id = "{entity_id}"
                    AND created_at > "{test_start_time}"''')
        job_request_id = check_shard_zero(f'''SELECT id FROM job_request_histories WHERE job_request_type_id = "{job_request_type_id}" 
                    AND entity_id = "{entity_id}"
                    AND created_at > "{test_start_time}"''')
        if job_request_id is not None:
            break
    return job_request_id


def wait_for_job_to_finish(job_id):
    count = 0
    percent = check_shard_zero(f"SELECT percent_done FROM job_request_histories WHERE id = {job_id}")
    while not percent and count <= 100:
        time.sleep(1); count+=1
        percent = check_shard_zero(f"SELECT percent_done FROM job_request_histories WHERE id = {job_id}")
        if percent is not None:
            break
    return percent


def get_job_id_by_org_id(org_id, test_start_time, job_request_type_id = None):
    """Passing in the job request type id is not necessary but will result in a faster query"""
    count = 0
    job_id = check_shard_zero(f"SELECT id FROM job_requests WHERE entity_id = '{org_id}' "
                              f" AND created_at > '{test_start_time}' LIMIT 1")
    while (job_id == "" or job_id is None) and count < 100:
        time.sleep(1)
        count += 1
        job_id = check_shard_zero(f"SELECT id FROM job_requests WHERE entity_id = '{org_id}' "
                                  f"AND created_at > '{test_start_time}' LIMIT 1")
        if job_request_type_id:
            job_finished_id = check_shard_zero(f"SELECT id FROM job_request_histories WHERE entity_id = '{org_id}' "
                                               f"AND job_request_type_id = '{job_request_type_id}' "
                                               f"AND created_at > '{test_start_time}' LIMIT 1")
        else:
            job_finished_id = check_shard_zero(f"SELECT id FROM job_request_histories WHERE entity_id = '{org_id}' "
                                               f"AND created_at > '{test_start_time}' LIMIT 1")
        if job_finished_id:
            job_id = job_finished_id
            break
    return job_id


def wait_for_job_to_fail(job_id):
    count = 0
    ps_error = check_shard_zero(f"SELECT ps_error_id from job_requests WHERE id = '{job_id}'")
    while not ps_error and count <= 100:
        time.sleep(1); count+=1
        ps_error = check_shard_zero(f"SELECT ps_error_id from job_requests WHERE id = '{job_id}'")
        if ps_error is not None:
            break
    return ps_error


# region Export helpers

def wait_for_export_status(job_id):
    done_status = 3
    count = 0
    current_status = check_all_shards(f"SELECT export_status FROM export_transactions WHERE job_request_id = '{job_id}'")
    if current_status is None:
        completed_date = check_all_shards(f"SELECT completed_at FROM job_request_histories WHERE id = '{job_id}'")
        if completed_date:
            return True
    else:
        while (int(current_status) != done_status) and count <= 10:
            time.sleep(3); count+=1
            current_status = check_all_shards(f"SELECT export_status FROM export_transactions WHERE job_request_id = '{job_id}'")
        return int(current_status) == done_status

# endregion Export helpers

def check_shard_zero(sql_query):

    """this is a support method for grabbing job request IDs, which are always on Shard 0"""
    my_db = db_base.establish_connection(shard=0)
    sql = sql_query
    cursor = my_db.cursor(buffered=True)
    cursor.execute(sql_query)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return result