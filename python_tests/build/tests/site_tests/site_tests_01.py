import pytest
from datetime import date
from pages.login_page import LoginPage
from pages.organization.configure.plan_year_page import PlanYearPage
from pages.base_page import BasePage
from pages.organization.configure.define_benefit_plans_page import DefineBenefitPlansPage
from pages.organization.employees.dependent_profile_card_page import DependentProfileCardPage
from pages.organization.employees.employee_profile_page import EmployeeProfilePage
from pages.organization.tasks.ben_admin_document_request_card_page import BenAdminDocumentRequestCardPage
from pages.organization.tasks.tasks_page import TasksPage
from test_data import api_employee, api_dependent
from tests.base_test import BaseTest
from database_connections import organizations, org_plan_years
from tests.feature_fixtures import enrollment
from utils import config_setup


class TestEnrollmentAdmin3(BaseTest):

    @pytest.mark.enrollment_admin_three
    def test_enrollment_admin_contribution_type_transit_reimbursement_account_two_plan15739(self, enrollment, teardown_plan15739):
        assert_list = []
        global organization_15739
        global employee_15739

        # region Objects
        login_page = LoginPage(self.driver)
        employee_profile_page = EmployeeProfilePage(self.driver)
        # endregion Objects

        admin = login_page.config['organizations']['transit_account_reimbursement_two']['username']
        password = login_page.config['organizations']['transit_account_reimbursement_two']['password']
        organization_15739 = login_page.config['organizations']['transit_account_reimbursement_two']['name']

        login_page.login(admin, password)

        employee_15739 = api_employee.create_api_employee(organization_15739)
        employee_profile_page.goto_with_user_id(employee_15739['id'])
        employee_profile_page.click_new_hire_enrollment_link()
        enrollment.home_page.get_started_button()
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.enrollment_page.click_benefit("Transit Reimbursement Account 2")
        enrollment.enrollment_page.maximize_contribution_flex_benefit()
        if not enrollment.enrollment_page.transit_account_two_maximize_link_exists():
            assert_list.append("Maximize link is not present")
        enrollment.enrollment_page.click_update_cart()
        enrollment.enrollment_page.proceed_to_checkout()
        enrollment.review_and_checkout_page.checkout_button()
        if not login_page.do_titles_match(enrollment.confirmation_page.confirmation_title()):
            assert_list.append("Enrollment failed, did not reach confirmation page")
        assert not assert_list, assert_list

    @pytest.mark.enrollment_admin_three
    def test_enrollment_admin_validate_life_event_enrollment_population_based_oe_plan15055(self, enrollment, teardown_plan15055):

        global organization_15055
        global employee_15055

        # region Objects
        login_page = LoginPage(self.driver)
        employee_profile_page = EmployeeProfilePage(self.driver)
        # endregion Objects

        admin = login_page.config['organizations']['dual_enrollment']['username']
        password = login_page.config['organizations']['dual_enrollment']['password']
        organization_15055 = login_page.config['organizations']['dual_enrollment']['name']

        login_page.login(admin, password)

        employee_15055 = api_employee.create_api_employee(organization_15055)
        employee_profile_page.goto_with_user_id(employee_15055['id'])
        employee_profile_page.life_event_link()
        enrollment.life_event_page.select_life_event("Birth")
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.medical_page.enroll_in_medical(plan="Silver PPO")
        enrollment.enrollment_page.proceed_to_checkout()
        enrollment.review_and_checkout_page.checkout_button()
        assert login_page.do_titles_match(
            enrollment.confirmation_page.confirmation_title()), "Enrollment failed, did not reach confirmation page"

    @pytest.mark.enrollment_admin_three
    def test_enrollment_3_admin_contribution_type_parking_reimbursement_account_link_plan13968(self, enrollment, teardown_plan13968):
        assert_list = []
        global organization_13968
        global employee_13968

        # region Objects
        login_page = LoginPage(self.driver)
        employee_profile_page = EmployeeProfilePage(self.driver)
        # endregion Objects

        admin = login_page.config['organizations']['parking_account']['username']
        password = login_page.config['organizations']['parking_account']['password']
        organization_13968 = login_page.config['organizations']['parking_account']['name']

        login_page.login(admin, password)

        employee_13968 = api_employee.create_api_employee(organization_13968)
        employee_profile_page.goto_with_user_id(employee_13968['id'])
        employee_profile_page.click_new_hire_enrollment_link()
        enrollment.home_page.get_started_button()
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.enrollment_page.click_benefit("Parking Reimbursement Account")
        enrollment.enrollment_page.maximize_contribution_flex_benefit()
        if not enrollment.enrollment_page.transit_account_two_maximize_link_exists():
            assert_list.append("Maximize link is not present")
        enrollment.enrollment_page.click_update_cart()
        enrollment.enrollment_page.proceed_to_checkout()
        enrollment.review_and_checkout_page.checkout_button()
        if not login_page.do_titles_match(enrollment.confirmation_page.confirmation_title()):
            assert_list.append("Enrollment failed, did not reach confirmation page")
        assert not assert_list, assert_list

    @pytest.mark.enrollment_admin_three
    def test_enrollment_dual_admin_early_checkout_plan11983(self, enrollment):

        # object declaration
        basepage = BasePage(self.driver)
        loginpage = LoginPage(self.driver)
        employeeprofilepage = EmployeeProfilePage(self.driver)
        planyearpage = PlanYearPage(self.driver)
        # end object declaration

        organization = loginpage.config['organizations']['admin_dualenrollment_earlycheckout']['name']
        employee = api_employee.create_api_employee(organization)
        adminusername = loginpage.config['organizations']['admin_dualenrollment_earlycheckout']['username']
        adminpassword = loginpage.config['organizations']['admin_dualenrollment_earlycheckout']['password']
        orgid = organizations.name_to_id(organization)
        planyearname = f"01/01/{date.today().year + 1} to 12/31/{date.today().year + 1}"

        loginpage.login(adminusername, adminpassword)

        if not org_plan_years.admin_oe_dates_active(orgid, plan_year_name=planyearname):
            planyearpage.update_oe_dates_to_current_month(plan_year_name=planyearname)

        employeeprofilepage.goto_with_user_id(employee['id'])

        employeeprofilepage.click_new_hire_enrollment_link()

        # first, new hire enrollment
        enrollment.home_page.shop_new_hire_enrollment_button()
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.medical_page.enroll_in_medical(plan='Bronze PPO')
        enrollment.enrollment_page.proceed_to_checkout()
        enrollment.review_and_checkout_page.checkout_button()

        # second, open enrollment
        enrollment.home_page.shop_open_enrollment_button()
        enrollment.medical_page.enroll_in_medical(plan='Bronze PPO')
        enrollment.enrollment_page.proceed_to_checkout()
        enrollment.review_and_checkout_page.checkout_button()
        assert basepage.do_titles_match(
            enrollment.confirmation_page.confirmation_title()), "Enrollment failed, did not reach confirmation page"

        # Tear down
        api_employee.remove_employee_through_api(organization, employee['id'])

    @pytest.mark.enrollment_admin_three
    def test_enrollment_admin_contribution_type_dcra_account_link_plan13969(self, enrollment, teardown_plan13969):
        assert_list = []
        global organization_13969
        global employee_13969

        # region Objects
        login_page = LoginPage(self.driver)
        employee_profile_page = EmployeeProfilePage(self.driver)
        # endregion Objects

        admin = login_page.config['organizations']['dcra_account']['username']
        password = login_page.config['organizations']['dcra_account']['password']
        organization_13969 = login_page.config['organizations']['dcra_account']['name']

        login_page.login(admin, password)

        employee_13969 = api_employee.create_api_employee(organization_13969)
        employee_profile_page.goto_with_user_id(employee_13969['id'])
        employee_profile_page.click_new_hire_enrollment_link()
        enrollment.home_page.get_started_button()
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.enrollment_page.click_benefit("Dependent Care Reimbursement Account")
        enrollment.enrollment_page.maximize_contribution_flex_benefit()
        if not enrollment.enrollment_page.transit_account_two_maximize_link_exists():
            assert_list.append("Maximize link is not present")
        enrollment.enrollment_page.click_update_cart()
        enrollment.enrollment_page.proceed_to_checkout()
        enrollment.review_and_checkout_page.checkout_button()
        if not login_page.do_titles_match(enrollment.confirmation_page.confirmation_title()):
            assert_list.append("Enrollment failed, did not reach confirmation page")
        assert not assert_list, assert_list

    @pytest.mark.enrollment_admin_three
    def test_enrollment_admin_contribution_type_hcra_account_link_plan13973(self, enrollment, teardown_plan13973):
        assert_list = []
        global organization_13973
        global employee_13973

        # region Objects
        login_page = LoginPage(self.driver)
        employee_profile_page = EmployeeProfilePage(self.driver)
        # endregion Objects

        admin = login_page.config['organizations']['hcra_account']['username']
        password = login_page.config['organizations']['hcra_account']['password']
        organization_13973 = login_page.config['organizations']['hcra_account']['name']

        login_page.login(admin, password)

        employee_13973 = api_employee.create_api_employee(organization_13973)
        employee_profile_page.goto_with_user_id(employee_13973['id'])
        employee_profile_page.click_new_hire_enrollment_link()
        enrollment.home_page.get_started_button()
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.enrollment_page.click_benefit("Health Care Reimbursement Account")
        enrollment.enrollment_page.maximize_contribution_flex_benefit()
        if not enrollment.enrollment_page.transit_account_two_maximize_link_exists():
            assert_list.append("Maximize link is not present")
        enrollment.enrollment_page.click_update_cart()
        enrollment.enrollment_page.proceed_to_checkout()
        enrollment.review_and_checkout_page.checkout_button()
        if not login_page.do_titles_match(enrollment.confirmation_page.confirmation_title()):
            assert_list.append("Enrollment failed, did not reach confirmation page")
        assert not assert_list, assert_list

    @pytest.mark.enrollment_admin_three
    def test_enrollment_3_admin_dependent_coverage_hide_yourself_plan10096(self, enrollment, teardown_plan10096):
        assert_list = []
        global organization_10096
        global employee_10096

        # object declaration
        login_page = LoginPage(self.driver)
        employee_profile_page = EmployeeProfilePage(self.driver)
        # end object declaration
        organization_10096 = login_page.config['organizations']['dep_cov_hide_yourself']['name']
        admin_username = login_page.config['organizations']['dep_cov_hide_yourself']['username']
        admin_password = login_page.config['organizations']['dep_cov_hide_yourself']['password']
        employee_10096 = api_employee.create_api_employee(organization_10096)
        child_plan10096 = api_dependent.create_api_dependent(organization_10096, employee_10096['id'], "Child",
                                                             min_age=0, max_age=26)
        login_page.login(admin_username, admin_password)

        employee_profile_page.goto_with_user_id(employee_10096['id'])
        employee_profile_page.click_new_hire_enrollment_link()
        enrollment.home_page.get_started_button()
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.medical_page.enroll_in_medical()
        enrollment.enrollment_page.click_update_cart()
        enrollment.enrollment_page.click_update_cart()
        enrollment.enrollment_page.click_benefit("Medical")
        val1 = enrollment.enrollment_page.benefit_family_covered()
        if "Yourself" not in val1:
            assert_list.append("Yourself was not included")
        enrollment.enrollment_page.click_update_cart()
        enrollment.my_benefits_page.click_benefit("Voluntary Dependent Life")
        val1 = enrollment.enrollment_page.benefit_family_covered()
        if "Yourself" in val1:
            assert_list.append("Yourself was included in Dependent Only coverage")
        assert not assert_list, assert_list

    @pytest.mark.enrollment_admin_three
    def test_enrollment_3_stacked_coverages_admin_voluntary_life_plan12262(self, enrollment, teardown_plan12262):
        assert_list = []
        global organization_12262
        global employee_12262

        # object declaration
        login_page = LoginPage(self.driver)
        employee_profile_page = EmployeeProfilePage(self.driver)
        # end object declaration

        admin_username = login_page.config['organizations']['enrollment_stacked_voluntary_life']['username']
        admin_password = login_page.config['organizations']['enrollment_stacked_voluntary_life']['password']
        organization_12262 = login_page.config['organizations']['enrollment_stacked_voluntary_life']['name']
        employee_12262 = api_employee.create_api_employee(organization_12262)
        login_page.login(admin_username, admin_password)
        employee_profile_page.goto_with_user_id(employee_12262['id'])
        employee_profile_page.click_new_hire_enrollment_link()
        enrollment.home_page.get_started_button()
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.voluntary_life_page.enroll_in_voluntary_life(coverage_amount="$20,000")
        enrollment.voluntary_life_page.click_to_benefits()
        enrollment.enrollment_page.proceed_to_checkout()
        enrollment.review_and_checkout_page.checkout_button()
        enrollment.enrollment_page.admin_menu_home_page_link()

        api_employee.update_employee_through_api(organization_name=organization_12262, sub_id=employee_12262['id'])

        enrollment.enrollment_page.enroll_refresh_page()
        employee_profile_page.life_event_link()
        enrollment.life_event_page.select_life_event("Marriage")
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.home_page.click_benefit('Voluntary Employee Life')
        enrollment.voluntary_life_page.select_amount_existing_coverage('$30,000')
        enrollment.voluntary_life_page.click_update_cart()
        enrollment.enrollment_page.click_benefit("Voluntary Employee Life")
        prior_coverage = enrollment.enrollment_page.stacked_coverage_prior_amount()
        current_election = enrollment.enrollment_page.stacked_coverage_current_coverage_election()
        if not prior_coverage == "$20,000.00":
            assert_list.append("Stacked Coverage prior amount is incorrect.  Previous coverage should be $20,000.00 ")
        if not current_election == "$10,000.00":
            assert_list.append("Stacked Coverage new election is incorrect.  New election should be for $10,000.00")

        enrollment.enrollment_page.proceed_to_checkout()

        assert not assert_list, assert_list

    @pytest.mark.enrollment_admin_three
    def test_enrollment_3_admin_decline_with_waive_plan12254(self, enrollment, teardown_plan12254):
        global organization_12254
        global employee_12254

        # object declaration
        login_page = LoginPage(self.driver)
        employee_profile_page = EmployeeProfilePage(self.driver)
        # end object declaration
        admin_username = login_page.config['organizations']['decline_with_waive']['username']
        admin_password = login_page.config['organizations']['decline_with_waive']['password']
        organization_12254 = login_page.config['organizations']['decline_with_waive']['name']
        employee_12254 = api_employee.create_api_employee(organization_12254)
        login_page.login(admin_username, admin_password)
        employee_profile_page.goto_with_user_id(employee_12254['id'])
        employee_profile_page.click_new_hire_enrollment_link()
        enrollment.home_page.get_started_button()
        enrollment.my_profile_page.profile_next()
        enrollment.my_family_page.family_next()
        enrollment.medical_page.enroll_in_medical(plan="Custom Premier PPO - 1730PA")
        enrollment.dental_page.click_update_cart_button()
        enrollment.vision_page.decline_with_waive_vision()
        enrollment.my_benefits_page.review_and_checkout_button()
        enrollment.review_and_checkout_page.checkout_button()
        assert login_page.do_titles_match(
            enrollment.confirmation_page.confirmation_title()), "Enrollment failed, did not reach confirmation page"

    @pytest.fixture()
    def teardown_plan10096(self):
        yield
        api_employee.remove_employee_through_api(organization_10096, employee_10096['id'])

    @pytest.fixture()
    def teardown_plan13973(self):
        yield
        api_employee.remove_employee_through_api(organization_13973, employee_13973['id'])

    @pytest.fixture()
    def teardown_plan13968(self):
        yield
        api_employee.remove_employee_through_api(organization_13968, employee_13968['id'])

    @pytest.fixture()
    def teardown_plan15739(self):
        yield
        api_employee.remove_employee_through_api(organization_15739, employee_15739['id'])

    @pytest.fixture()
    def teardown_plan15055(self):
        yield
        api_employee.remove_employee_through_api(organization_15055, employee_15055['id'])

    @pytest.fixture()
    def teardown_plan13969(self):
        yield
        api_employee.remove_employee_through_api(organization_13969, employee_13969['id'])

    @pytest.fixture()
    def teardown_plan12262(self):
        yield
        api_employee.remove_employee_through_api(organization_12262, employee_12262['id'])

    @pytest.fixture()
    def teardown_plan12254(self):
        yield
        api_employee.remove_employee_through_api(organization_12254, employee_12254['id'])