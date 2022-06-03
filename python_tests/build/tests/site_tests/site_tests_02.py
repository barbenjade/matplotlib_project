from tests.base_test import BaseTest
from pages.broker.broker_home_page import BrokerHomePage
from pages.organization.system.plugins.plugins_page import PluginsPage
from pages.organization.system.plugins.hartford_eoi_page import HartfordEoiPage
from pages.organization.system.plugins.bamboo_hr_page import BambooHrPage
from pages.organization.system.plugins.ulti_pro_plugin_page import UltiProPluginPage
from utils import data_helpers
from pages.login_page import LoginPage
import pytest


class TestPlugins(BaseTest):

    @pytest.mark.plugins
    def test_bamboo_configure_fields_plan12452(self, teardown_plan12542):
        global bamboo_page12452

        login_page = LoginPage(self.driver)
        broker_page = BrokerHomePage(self.driver)
        plugin_page = PluginsPage(self.driver)
        bamboo_page12452 = BambooHrPage(self.driver)

        ps_attribute = 'User Defined Field10'
        mapped_attribute = 'Completed - Completed'

        assert_array = []

        login_page.login_as_root()
        broker_page.search_and_select_organization(login_page.config['organizations']['bamboo']['name'])
        plugin_page.goto()
        plugin_page.click_plugin('BambooHR Sync')
        bamboo_page12452.click_mapped_attribute_dropdown('employee_census_data')

        if not bamboo_page12452.is_ps_attribute_displayed(ps_attribute):
            assert_array.append('ps attribute was not displayed')

        if not bamboo_page12452.search_and_click_mapped_attributes(ps_attribute, mapped_attribute):
            assert_array.append('Mapped Bamboo attribute was not displayed')

        assert not assert_array, assert_array

    @pytest.mark.plugins
    def test_ukg_global_filtering_plan15061(self, teardown_plan15061):
        # region pages
        global ukg_page
        global default_cc
        global default_date
        global default_ee_ids

        login_page = LoginPage(self.driver)
        broker_page = BrokerHomePage(self.driver)
        ukg_page = UltiProPluginPage(self.driver)
        # endregion pages
        assert_array = []

        # region variables
        default_cc = 'USA,CAN'
        default_date = '2019-01-01'
        default_ee_ids = ''

        updated_cc = 'AUS'
        updated_date = '2020-01-01'
        updated_ee_ids = f'{data_helpers.unique_string(7)}'
        # endregion variables

        login_page.login(login_page.config['login']['admin_username'],
                         login_page.config['login']['admin_password'])
        broker_page.search_and_select_organization(login_page.config['organizations']['ulti_bey8_client']['name'])
        ukg_page.goto()

        ukg_page.set_country_code_to_sync(updated_cc)
        ukg_page.set_sync_terminations_loa_date(updated_date)
        ukg_page.employee_ids_to_sync(updated_ee_ids)

        ukg_page.click_save_button()
        ukg_page.goto()

        if ukg_page.get_country_code() != updated_cc:
            assert_array.append('Updated country code did not save')

        if ukg_page.get_terminations_loa_date() != updated_date:
            assert_array.append('Updated date did not save')

        if ukg_page.get_employee_ids_to_sync() != updated_ee_ids:
            assert_array.append('Updated ee ids did not save')

        assert not assert_array, assert_array

    @pytest.mark.plugins
    def test_hartford_eoi_plugin_configuration_13329(self, teardown_plan13329):
        # region pages
        global plugin_page
        global hartford_eoi

        login_page = LoginPage(self.driver)
        plugin_page = PluginsPage(self.driver)
        hartford_eoi = HartfordEoiPage(self.driver)
        # end region pages

        assert_array = []
        group_id = "340238"

        org_info = self.org_info('organizations.hartford_eoi_config')
        login_page.login(org_info.username, org_info.password)
        hartford_eoi.goto()
        hartford_eoi.toggle_hartford_enrollment_sso(True)
        hartford_eoi.hartford_fill_out_group_id(group_id)
        hartford_eoi.toggle_test_only_checkbox(True)
        hartford_eoi.click_save_button()
        plugin_page.goto()
        if not plugin_page.is_plugin_active_in_ui("The Hartford EOI"):
            assert_array.append("Hartford SSO Checkbox not saved, Hartford not active.")
        plugin_page.click_plugin("The Hartford EOI")
        if not hartford_eoi.get_hartford_sso_toggle_value():
            assert_array.append("SSO toggle value not saved.")
        if not hartford_eoi.get_hartford_group_id_value() == group_id:
            assert_array.append("Group ID value not saved correctly.")
        if not hartford_eoi.get_test_employee_toggle_value():
            assert_array.append("Test only checkbox toggle not saved.")
        hartford_eoi.click_relationship_tab()
        hartford_eoi.set_hartford_relationship_value("Student", "Child")
        hartford_eoi.click_save_button()
        hartford_eoi.click_relationship_tab()
        if not hartford_eoi.get_hartford_relationship_mapped_value("Student") == "Child":
            assert_array.append("Relationship Mapping Value not saved")
        if not hartford_eoi.is_data_mapping_tab_present():
            assert_array.append("Data Mapping Tab not present")

        assert not assert_array, assert_array

    @pytest.fixture()
    def teardown_plan15061(self):
        yield
        ukg_page.set_country_code_to_sync(default_cc)
        ukg_page.set_sync_terminations_loa_date(default_date)
        ukg_page.employee_ids_to_sync(default_ee_ids)
        ukg_page.click_save_button()

    @pytest.fixture()
    def teardown_plan12542(self):
        yield
        if bamboo_page12452.is_discard_changes_button_present():
            bamboo_page12452.click_discard_changes_button()

    @pytest.fixture()
    def teardown_plan13329(self):
        yield
        plugin_page.goto()
        plugin_page.click_plugin("The Hartford EOI")
        hartford_eoi.toggle_hartford_enrollment_sso(False)
        hartford_eoi.hartford_fill_out_group_id("")
        hartford_eoi.test_only_checkbox(False)
        hartford_eoi.click_save_button()
        hartford_eoi.click_relationship_tab()
        hartford_eoi.set_hartford_relationship_value("Student", "")
        hartford_eoi.click_save_button()