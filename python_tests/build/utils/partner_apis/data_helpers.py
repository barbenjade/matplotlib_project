import time
import re
from string import ascii_letters, digits
import secrets
import random
from random import randint, seed, sample
from database_connections import db_base


def unique_number(max_value):
    value = randint(1, max_value)
    return value

def random_with_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def unique_string(string_length=5):
    alphabet = ascii_letters + digits
    string = "".join(secrets.choice(alphabet) for i in range(string_length))
    return string

# this will check if "my_time" is within a starting and ending time range
def time_in_time_range(start_time, end_time, my_time):
    return str(start_time) <= str(my_time) <= str(end_time)

def get_most_recent_message_by_to_number(to_number):
    #We need to build out the twilio api connection before we write this method.
    return False