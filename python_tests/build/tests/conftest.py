import logging
import pathlib
import shutil
import stat
import sys
import time
import pytest
import pytz
import os
import re
import requests
import json

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from typing import List

from tests.for_the_memes import for_the_memes
from utils import config_setup
from selenium import webdriver
from pages.login_page import LoginPage as login
from datetime import datetime
from pytest_reportportal import RPLogger, RPLogHandler
from tests.webdriver_setup import build_browser
from utils.config_setup import MasterConfig, master_config
from utils import data_helpers

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='session')
def init_driver(request, project_root, main_config, test_run, rp_logger, download_file, tmp_path_factory):

    rand_int = data_helpers.random_with_n_digits(6)
    temp_driver_path = f"{tmp_path_factory.mktemp('data')}/{rand_int}"
    os.environ['WDM_LOG_LEVEL'] = '0'
    global web_driver
    # Builds the Browser options for browser setup
    browser_options = main_config.options
    experimental_options = [{"download.default_directory": f"{temp_download_dir}"}]

    if main_config.browser == "chrome":
        if main_config.driver_exe_path == "manager":
            web_driver = build_browser("chrome", experimental_options=experimental_options, browser_options=browser_options,
                                       version=main_config.version, driver_manager=True, path=temp_driver_path)
        else:
            web_driver = build_browser("chrome", experimental_options=experimental_options, browser_options=browser_options,
                                       version=main_config.version, driver_manager=False)
    elif main_config.browser == "firefox":
        if main_config.driver_exe_path == "manager":
            web_driver = build_browser("firefox", experimental_options=experimental_options, browser_options=browser_options,
                                       version=main_config.version, driver_manager=True)
        else:
            web_driver = build_browser("firefox", experimental_options=experimental_options, browser_options=browser_options,
                                       version=main_config.version, driver_manager=False)
    #todo finish setting up edge when we actually care
    elif main_config.browser == "edge":
        web_driver = build_browser("edge", browser_options, main_config.version, driver_manager=True)

    #request.cls.driver = web_driver
    session_obj = request.node
    for item in session_obj.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", web_driver)

    test_start_time = datetime.now()
    test_start_time = test_start_time.astimezone(pytz.utc)
    if "mobile" in browser_options:
        web_driver.set_window_size(360, 640)
    elif "headless" in browser_options:
        web_driver.set_window_size(1920, 1080)
    else:
        web_driver.maximize_window()
    web_driver.implicitly_wait(5)
    web_driver.set_page_load_timeout(300)
    yield web_driver
    try:
        if request.session.testsfailed > 0:
            # If a test run fails, a screenshot will be added to test results, and logged to report portal
            # TODO this needs to be reworked to attach screenshots to the correct test run in report portal
            filelist = []
            test_path = f'{project_root}/test_data/test_results'

            for root, dirs, files in os.walk(test_path):
                for file in files:
                    if file.endswith(".png"):
                        filelist.append(os.path.join(root, file))

            for screenshot in filelist:
                with open(screenshot, "rb") as fh:
                    image_file = fh.read()
                    rp_logger.info("Test Failed - Attaching Screenshot",
                                   attachment={
                                       "name": "test_failed.png",
                                       "data": image_file,
                                       "mime": "image/png"
                                   })
    except AttributeError:
        rp_logger.error('Unable to send screenshot to report portal.')
    except TypeError:
        rp_logger.info('Report Portal not connected to this run')
    web_driver.quit()
    try:
        shutil.rmtree(str(temp_driver_path))
    except Exception:
        pass
    login.org_admin_ps_error(test_start_time)


@pytest.fixture(scope='session', autouse=True)
def project_root() -> str:
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='session', autouse=False)
def test_run(project_root, request) -> str:
    """
    Creates the `/test_results` directory to store the results of the Test Run.
    Creates the `/test_data/downloads` directory to store downloaded files
    Returns:
        The `/test_results` directory as a filepath (str).
    """
    session = request.node
    temp_file = data_helpers.random_with_n_digits(6)
    test_data_path = re.sub("/tests", "", os.path.dirname(__file__))
    test_results_dir = os.path.join(test_data_path, "test_data/test_results")
    global temp_download_dir
    temp_download_dir = os.path.join(test_data_path, f"test_data/downloads/{temp_file}")
    download_dir = os.path.join(test_data_path, "test_data/downloads")

    for directories, dirs, files in os.walk(test_results_dir, topdown=False):
        if dirs:
            for x in dirs:
                if os.path.exists(f'{test_results_dir}/{x}'):
                    try:
                        os.rmdir(f'{test_results_dir}/{x}')
                    except:
                        pass

    if not os.path.exists(test_results_dir):
        # create /test_results for this Test Run
        os.makedirs(test_results_dir, exist_ok=True)
    if os.path.exists(download_dir):
        # cleans up the downloads directory from the previous run
        try:
            shutil.rmtree(download_dir, ignore_errors=True)
        except:
            pass
    if not os.path.exists(temp_download_dir):
        # create /test_data/downloads folder if it doesn't already exist
        try:
            os.makedirs(temp_download_dir, exist_ok=True)
        except:
            pass

    for test in session.items:
        # make the test_result directory for each test
        if not os.path.exists(f'{str(test_results_dir)}/{test.name}'):
            try:
                os.makedirs(f'{str(test_results_dir)}/{test.name}', exist_ok=True)
            except:
                pass

    return test_results_dir


@pytest.fixture(scope="session")
def rp_logger(request):
    """ Report Portal Logger """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Create handler for Report Portal if the service has been
    # configured and started.
    if hasattr(request.node.config, 'py_test_service'):
        # Import Report Portal logger and handler to the test module.
        logging.setLoggerClass(RPLogger)
        rp_handler = RPLogHandler(request.node.config.py_test_service)
        # Add additional handlers if it is necessary
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
    else:
        rp_handler = logging.StreamHandler(sys.stdout)
    # Set INFO level for Report Portal handler.
    rp_handler.setLevel(logging.INFO)
    return logger


def pytest_sessionstart(session):
    session.results = dict()


def remove_downloads():
    path = re.sub("/tests", "", os.path.dirname(__file__))
    download_dir = os.path.join(path, "test_data/downloads")
    path = os.scandir(download_dir)
    try:
        for i in path:
            os.remove(i)
    except PermissionError:
        for i in path:
            os.chmod(i, stat.S_IRWXU)
            os.remove(i)


@pytest.fixture(scope="function")
def feature_fixtures(init_driver):
    """Passes the driver in for feature_fixtures.py"""
    return web_driver


@pytest.fixture(scope="function")
def api():
    """Simple requests fixture to make HTTP API calls"""
    return requests

cli_ring_central = None

@pytest.fixture(scope="session")
def main_config(request):
    _json = config_setup.master_config()
    config = MasterConfig(**_json)

    cli_browser = request.config.getoption('--browser')
    if cli_browser:
        config.browser = cli_browser

    cli_browser_options = request.config.getoption('--options')
    if cli_browser_options:
        config.options = [option.strip() for option in cli_browser_options.split(',')]

    cli_version = request.config.getoption('--driver_version')
    if cli_version:
        config.version = cli_version

    cli_driver_exe_path = request.config.getoption('--driver_exe_path')
    if cli_driver_exe_path:
        config.driver_exe_path = cli_driver_exe_path

    global cli_ring_central
    cli_ring_central = request.config.getoption('--ringC')

    return config

@pytest.fixture(scope='session')
def download_file():
    return temp_download_dir


def pytest_addoption(parser):
    parser.addoption(
        '--browser', action='store', default='', help='The lowercase browser name: chrome | firefox'
    )
    parser.addoption(
        '--options', action='store',
        default='', help='Comma-separated list of Browser Options. Ex. "headless, incognito"'
    )
    parser.addoption(
        '--driver_version', action='store', default='', help='Webdriver manager version to run'
    )
    parser.addoption(
        '--driver_exe_path', action='store',
        default='', help='Specify driver path or use "manager" string to use Webdriver Manager'
    )
    parser.addoption(
        '--ringC', action='store',
        default='N', help='Use this to send failed reports to Ring Central. Use Y for yes and N for no'
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    session = requests.session()
    report = yield
    result = report.get_result()
    if result.when == 'call' or result.when == 'setup':
        if result.failed:
            try:
                test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
                # web_driver.save_screenshot(
                    # f'{ROOT_PATH}/test_results/{test_name}/{datetime.today().strftime("%m-%d_%H:%M")}_screenshot.png')
                if "smoke" in item.own_markers[0].name and cli_ring_central == "Y":
                    urls = webhook_urls()
                    current_env_version = version_urls()[master_config()['environment']]
                    body = {
                        "activity": "QA Smoke Failures",
                        "iconUri": "https://tenor.com/view/creepy-guy-behind-plant-hide-gif-11543382.gif",
                        "attachments": [
                            {
                                "type": "Card",
                                "fallback": "Something happened",
                                "color": "#FF0000",
                                "intro": "               WHAT DID YOU DO?",
                                "author": {
                                    "name": current_env_version,
                                    "iconUri": for_the_memes()
                                },
                                "fields": [
                                    {
                                        "title": "Where",
                                        "title_link": current_env_version,
                                        "value": f"{master_config()['environment'].upper()}",
                                        "style": "Short"
                                    },
                                    {
                                        "title": "Test Failure",
                                        "value": item.name,
                                        "style": "long"
                                    },
                                    {
                                        "title": "Failure Message",
                                        "value": result.longrepr.reprcrash.message
                                    }
                                ]
                            }
                        ]
                    }
                    temp = json.dumps(body, indent=2)
                    json_body = re.sub("\n ", "", temp)

                    headers = {"Content-Type": "application/json"}
                    session.headers.update(headers)

                    for team, url in urls.items():
                        if team == "cicd" and master_config()['environment'] == "dev":
                            requests.post(url, data=json_body, headers=session.headers)
                        elif team == "qa_patch":
                            requests.post(url, data=json_body, headers=session.headers)

            except Exception:
                pass

        item.session.results[item] = result


def version_urls():
    environments = {"dev": "https://benefits.plansourcedev.com/ver.txt",
                    "uat": "https://benefits.plansourcetest.com/ver.txt",
                    "partner_dev": "https://partner-dev-benefits.plansource.com/ver.txt",
                    "prod": "https://benefits.plansource.com/ver.txt"}
    return environments


def webhook_urls():
    url_hash = {"cicd": "https://hooks.ringcentral.com/webhook/v2/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvdCI6InUiLCJvaSI6IjE0MTI4MDY3NTQzMDciLCJpZCI6IjE2MDg3NjEzNzEifQ.VIVm3oyRIqa1PJpUEc952VNzuYz4XUL_24D0u8Fk9rQ",
                "qa_patch": "https://hooks.ringcentral.com/webhook/v2/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvdCI6InUiLCJvaSI6IjEzOTEzNjg4MzkxNzEiLCJpZCI6IjE0ODc1NjA3MzEifQ.I91Dhz7_GqFnDsi0cNtiWbLwOAOswDISy7l-RtP-xuU"}
    return url_hash