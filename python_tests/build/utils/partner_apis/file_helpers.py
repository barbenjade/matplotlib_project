import errno
import os
import os.path
import locale
import pathlib
import re
import stat
import time
import random
import string
import fitz
from utils import config_setup

import pandas
from pandas import DataFrame
import zipfile
import csv
from os import scandir
from io import BytesIO
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import C14NWriterTarget, XMLParser
import pysftp
import shutil


# region Read Write and Delete Files

def read_file(file):
    with open(file, "r") as f:
        return f.read()


def read_file_lines(file):
    with open(file, "r") as f:
        return f.readlines()


def write_file(file_path, file):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(file_path)
            os.chmod(file_path, stat.S_IRWXU)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    if isinstance(file, bytes):
        with open(file_path, "wb+") as f:
            f.write(file)
    elif isinstance(file, str):
        with open(f"{file_path}/{file}", "w+") as f:
            random_data = f"{''.join(random.choices(string.ascii_lowercase, k=50))}"
            f.write(random_data)
            return random_data


# endregion Read Write and Delete Files

# region Get File Data

def get_file(download_path, wait=0, file_name=None):
    time.sleep(wait)
    ensure_downloads_not_empty(download_path)
    browser = config_setup.master_config()['browser']
    if 'chrome' in browser:
        files = list(scandir(download_path))
        file = max(files, key=os.path.getctime)
        this_file = file.name
        count = 0
        while '.crdownload' in this_file and count <= 30:
            time.sleep(0.5)
            files = list(scandir(download_path))
            file = max(files, key=os.path.getctime)
            this_file = file.name
            count += 1
    if file_name:
        file = find_specific_file(file_name, download_path)
        return file
    files = list(scandir(f"{download_path}"))
    file = max(files, key=os.path.getctime)
    return file


def find_specific_file(file_name, download_path):
    """file name does not need to be the full name, just a partial string is fine"""
    my_file = ""
    ensure_downloads_not_empty(download_path)
    files = list(scandir(download_path))
    for x in files:
        if file_name in x.name:
            my_file = x
            break
    return my_file


def get_file_from_import_testing_folder(file_name):
    file = repo_directory_join(f"test_data/import_testing/{file_name}")
    return file

def get_file_from_enrollment_testing_folder(file_name):
    file = repo_directory_join(f"test_data/enrollment_testing/{file_name}")
    return file

def get_file_from_organizations_folder(org_name):
    file = os.path.abspath(f"../test_data/organizations/{org_name}.json")
    return file

def is_file_type_present(download_path, file_type):
    """pass in '.xls', '.csv', etc. for 'file_type'
       this will grab the most recend downloaded file and assert that it is that type"""
    file = get_file(download_path)
    return file_type in file.name

def unzip_file(file_path, path_to_unzip_to):
    with zipfile.ZipFile(file_path, "r") as zip:
        zip.extractall(path_to_unzip_to)


def get_csv_data(file_path):
    result = pandas.read_csv(f"{file_path}.csv")
    return result


def get_csv_cell(csv_file, column, column_value, cell_to_retrieve):
    """Use this function to return a single cell"""
    df = pandas.DataFrame(data=csv_file)
    my_row = df.index[df[column] == int(column_value)][0]
    return df[cell_to_retrieve].iloc[my_row]


def get_all_matching_csv_cells(csv_file, column, value_to_search, cell_to_retrieve):
    """Use this function if there is the possibility of returning multiple values"""
    df = pandas.DataFrame(data=csv_file)
    data = df[[column, cell_to_retrieve]]
    compare_results = data.isin(
        value_to_search if type(value_to_search) is list else [value_to_search])
    index_value = compare_results.index[compare_results[column] == True]

    if df[cell_to_retrieve].iloc[index_value].empty:
        raise ValueError(f"Could not find the search value in the CSV: {value_to_search}")

    return df[cell_to_retrieve].iloc[index_value].tolist()

def is_value_in_file(file, value, wait=0):
    """value can be a string or a list"""
    time.sleep(wait)
    parsed_file = read_file(file)
    if isinstance(value, str):
        return value in parsed_file
    elif isinstance(value, list):
        is_value_present = []
        for x in value:
            if x not in parsed_file:
                is_value_present.append("False")
        return not is_value_present


# endregion Get File Data

def remove_file(path_to_file):
    try:
        if os.path.exists(path_to_file):
            os.remove(path_to_file)
    except OSError as err:
        print(err)
        pass


def ensure_downloads_not_empty(download_path):
    count = 0
    global download_dir
    download_dir = download_path
    files = list(scandir(download_dir))
    while not files and count <= 60:
        time.sleep(1)
        count += 1
        files = list(scandir(download_dir))


def repo_directory_join(path_to_join):
    root_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root_dir, path_to_join)


# region XML Helpers

# pass in the name space as a hash.  For examle {"ss" : "urn:schemas-microsoft-com:office:spreadsheet"}.  These will be listed at the top of your xml doc.
def edit_xml_text_node(file_name, name_spaces, path, string):
    __adjust_namespaces(file_name, name_spaces)
    et = ET.parse(file_name)
    var = et.find(path, name_spaces)
    var.text = string
    et.write(file_name, xml_declaration=True)


def get_xml_text_from_node(file_name, path, name_spaces):
    __adjust_namespaces(file_name, name_spaces)
    et = ET.parse(file_name)
    return et.find(path, name_spaces).text


# this will register all the namespaces in the xml file and reformat the file to work with Elementtree.
# this should only be used privately in this helper file
def __adjust_namespaces(file_name, name_spaces):
    __register_all_namespaces(file_name)
    et = ET.parse(file_name)
    list = et.findall("//ss:*", name_spaces)
    for elem in list:
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}")[1]

    et.write(file_name, xml_declaration=True)


def __register_all_namespaces(filename):
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])


# endregion XML Helpers

# region SFTP Helpers

def place_file_on_sftp_site(host_name, username, password, file_name, path_to_upload_from, path_to_download_to):
    """This will place a file on the sftp site and then download that file to a local path"""

    count = 0
    with pysftp.Connection(host=host_name, username=username, password=password) as sftp:
        sftp.put(path_to_upload_from, f"/ee/{file_name}")
        array = sftp.listdir("/ee/")
        while file_name not in array and count >= 100:
            time.sleep(1);
            count += 1
            array = sftp.listdir("/ee/")
        sftp.get(f"/ee/{file_name}", path_to_download_to)


def copy_file_from_sftp_site(host_name, username, password, file_name, path_to_download_to):
    """This will download an existing file on the sftp site and copy it to a local path"""

    count = 0
    with pysftp.Connection(host=host_name, username=username, password=password) as sftp:
        array = sftp.listdir("/ee/")
        while file_name not in array and count <= 100:
            time.sleep(1);
            count += 1
            array = sftp.listdir("/ee/")
        sftp.get(f"/ee/{file_name}", path_to_download_to)


def remove_file_from_sftp_site(host_name, username, password, file_name, directory_file_is_in=None):
    """By default this will just check the default '/ee/' directory, if you need to look in a sub directory (payroll, incoming, result)
        then set the 'directory_file_is_in to that value"""
    with pysftp.Connection(host=host_name, username=username, password=password) as sftp:
        if directory_file_is_in is not None:
            array = sftp.listdir(f"/ee/{directory_file_is_in}/")
            if file_name in array:
                sftp.remove(f"/ee/{directory_file_is_in}/{file_name}")
            else:
                print("File is not present in the SFTP directory")
        else:
            array = sftp.listdir("/ee/")
            if file_name in array:
                sftp.remove(f"/ee/{file_name}")
            else:
                print("File is not present in the SFTP directory")


# endregion SFTP Helpers

# region Content Checkers

def check_file_for_substring(string, file):
    with fitz.open(file.path) as doc:
        text = ""
        for page in doc:
            text += page.getText()
    return string in text