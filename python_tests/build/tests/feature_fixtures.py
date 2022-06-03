import pytest

# Enrollment Imports
from pages.enrollment.enrollment_401k_page import Enrollment401kPage
from pages.enrollment.enrollment_home_page import EnrollmentHomePage
from pages.enrollment.enrollment_integration_dashboard_page import EnrollmentIntegrationDashboardPage
from pages.enrollment.enrollment_page import EnrollmentPage
from pages.enrollment.enrollment_hsa_page import EnrollmentHSAPage
from pages.enrollment.enrollment_account_details_page import EnrollmentAccountDetailsPage
from pages.enrollment.enrollment_add_family_member_page import EnrollmentAddFamilyMemberPage
from pages.enrollment.enrollment_agreement_page import EnrollmentAgreementPage
from pages.enrollment.enrollment_basic_ltd_page import EnrollmentBasicLTDPage
from pages.enrollment.enrollment_basic_life_page import EnrollmentBasicLifePage
from pages.enrollment.enrollment_beneficiaries_page import EnrollmentBeneficiariesPage
from pages.enrollment.enrollment_choose_primary_care_provider_page import EnrollmentChoosePrimaryCareProviderPage
from pages.enrollment.enrollment_communication_preferences_page import EnrollmentCommunicationPreferencesPage
from pages.enrollment.enrollment_confirmation_page import EnrollmentConfirmationPage
from pages.enrollment.enrollment_contact_page import EnrollmentContactPage
from pages.enrollment.enrollment_decision_iq_survey_page import EnrollmentDecisionIqSurveyPage
from pages.enrollment.enrollment_dental_page import EnrollmentDentalPage
from pages.enrollment.enrollment_dental_plan_page import EnrollmentDentalPlanPage
from pages.enrollment.enrollment_detailed_single_pcp_view_page import EnrollmentDetailedSinglePcpViewPage
from pages.enrollment.enrollment_documents_page import EnrollmentDocumentsPage
from pages.enrollment.enrollment_document_upload_drawer_page import EnrollmentDocumentUploadDrawerPage
from pages.enrollment.enrollment_fsa_page import EnrollmentFSAPage
from pages.enrollment.enrollment_help_me_decide_page import EnrollmentHelpMeDecidePage
from pages.enrollment.enrollment_life_event_page import EnrollmentLifeEventPage
from pages.enrollment.enrollment_medical_page import EnrollmentMedicalPage
from pages.enrollment.enrollment_medical_plan_page import EnrollmentMedicalPlanPage
from pages.enrollment.enrollment_my_family_page import EnrollmentMyFamilyPage
from pages.enrollment.enrollment_my_profile_page import EnrollmentMyProfilePage
from pages.enrollment.enrollment_my_device_page import EnrollmentMyDevicePage
from pages.enrollment.enrollment_my_benefits_page import EnrollmentMyBenefitsPage
from pages.enrollment.enrollment_plan_comparison_page import EnrollmentPlanComparisonPage
from pages.enrollment.enrollment_primary_care_provider_page import EnrollmentPrimaryCareProviderPage
from pages.enrollment.enrollment_review_and_checkout_page import EnrollmentReviewAndCheckoutPage
from pages.enrollment.enrollment_survey_page import EnrollmentSurveyPage
from pages.enrollment.enrollment_tasks_with_dependent_iq import EnrollmentTasksWithDependentIQ
from pages.enrollment.enrollment_vision_page import EnrollmentVisionPage
from pages.enrollment.enrollment_vision_plan_page import EnrollmentVisionPlanPage
from pages.enrollment.enrollment_voluntary_life_page import EnrollmentVoluntaryLifePage

# Guided Renewal Imports
from pages.organization.dashboards.client_config_renewal.renewal_setup_dashboard_page import RenewalSetupDashboardPage
from pages.organization.dashboards.client_config_renewal.renewal_settings_dashboard_page import RenewalSettingsDashboardPage
from pages.organization.dashboards.client_config_renewal.guided_renewal_plan_year_page import GuidedRenewalPlanYearPage
from pages.organization.dashboards.client_config_renewal.carriers_dashboard_page import CarriersDashboardPage
from pages.organization.dashboards.client_config_renewal.benefits_dashboard_page import BenefitsDashboardPage
from pages.organization.dashboards.client_config_renewal.plans_dashboard_page import PlansDashboardPage
from pages.organization.dashboards.client_config_renewal.costs_dashboard_page import CostsDashboardPage
from pages.organization.dashboards.client_config_renewal.validate_changes_dashboard_page import ValidateChangesDashboardPage
from pages.organization.dashboards.client_config_renewal.guided_renewal_test_employee_dashboard_page import GuidedRenewalTestEmployeeDashboardPage
from pages.organization.dashboards.client_config_renewal.review_and_submit_dashboard_page import ReviewAndSubmitDashboardPage
from pages.organization.dashboards.client_config_renewal.ssr_completion_dashboard_page import SSRCompletionDashboardPage
from pages.organization.dashboards.client_config_renewal.integrations_dashboard_page import IntegrationsDashboardPage


@pytest.fixture()
def enrollment(feature_fixtures):
    """
    This will initialize all enrollment classes which can be used as a fixture.
    Ex. def test_enrollment_admin_life_event_plan7253(self, enrollment):
            enrollment.life_event_page.select_life_event('Birth')
    """
    class EnrollmentInit:
        enroll_401k_page = Enrollment401kPage(feature_fixtures)
        account_details_page = EnrollmentAccountDetailsPage(feature_fixtures)
        add_family_member_page = EnrollmentAddFamilyMemberPage(feature_fixtures)
        agreement_page = EnrollmentAgreementPage(feature_fixtures)
        basic_life_page = EnrollmentBasicLifePage(feature_fixtures)
        basic_ltd_page = EnrollmentBasicLTDPage(feature_fixtures)
        beneficiaries_page = EnrollmentBeneficiariesPage(feature_fixtures)
        choose_primary_care_provider_page = EnrollmentChoosePrimaryCareProviderPage(feature_fixtures)
        communication_preferences_page = EnrollmentCommunicationPreferencesPage(feature_fixtures)
        confirmation_page = EnrollmentConfirmationPage(feature_fixtures)
        contact_page = EnrollmentContactPage(feature_fixtures)
        decision_iq_survey_page = EnrollmentDecisionIqSurveyPage(feature_fixtures)
        dental_page = EnrollmentDentalPage(feature_fixtures)
        dental_plan_page = EnrollmentDentalPlanPage(feature_fixtures)
        detailed_single_pcp_view_page = EnrollmentDetailedSinglePcpViewPage(feature_fixtures)
        document_upload_drawer_page = EnrollmentDocumentUploadDrawerPage(feature_fixtures)
        documents_page = EnrollmentDocumentsPage(feature_fixtures)
        fsa_page = EnrollmentFSAPage(feature_fixtures)
        help_me_decide_page = EnrollmentHelpMeDecidePage(feature_fixtures)
        home_page = EnrollmentHomePage(feature_fixtures)
        hsa_page = EnrollmentHSAPage(feature_fixtures)
        life_event_page = EnrollmentLifeEventPage(feature_fixtures)
        enrollment_page = EnrollmentPage(feature_fixtures)
        medical_page = EnrollmentMedicalPage(feature_fixtures)
        medical_plan_page = EnrollmentMedicalPlanPage(feature_fixtures)
        my_benefits_page = EnrollmentMyBenefitsPage(feature_fixtures)
        my_device_page = EnrollmentMyDevicePage(feature_fixtures)
        my_family_page = EnrollmentMyFamilyPage(feature_fixtures)
        my_profile_page = EnrollmentMyProfilePage(feature_fixtures)
        page = EnrollmentPage(feature_fixtures)
        primary_care_provider_page = EnrollmentPrimaryCareProviderPage(feature_fixtures)
        review_and_checkout_page = EnrollmentReviewAndCheckoutPage(feature_fixtures)
        survey_page = EnrollmentSurveyPage(feature_fixtures)
        vision_page = EnrollmentVisionPage(feature_fixtures)
        vision_plan_page = EnrollmentVisionPlanPage(feature_fixtures)
        voluntary_life_page = EnrollmentVoluntaryLifePage(feature_fixtures)
        tasks_with_dependent_iq_page = EnrollmentTasksWithDependentIQ(feature_fixtures)
        plan_comparison_page = EnrollmentPlanComparisonPage(feature_fixtures)
        integration_dashboard_page = EnrollmentIntegrationDashboardPage(feature_fixtures)

    return EnrollmentInit()


@pytest.fixture()
def guided_renewal(feature_fixtures):

    class GuidedRenewalInit:
        renewal_setup_dashboard_page = RenewalSetupDashboardPage(feature_fixtures)
        renewal_settings_dashboard_page = RenewalSettingsDashboardPage(feature_fixtures)
        guided_renewal_plan_year_page = GuidedRenewalPlanYearPage(feature_fixtures)
        carriers_dashboard_page = CarriersDashboardPage(feature_fixtures)
        benefits_dashboard_page = BenefitsDashboardPage(feature_fixtures)
        plans_dashboard_page = PlansDashboardPage(feature_fixtures)
        costs_dashboard_page = CostsDashboardPage(feature_fixtures)
        validate_changes_dashboard_page = ValidateChangesDashboardPage(feature_fixtures)
        test_employees_dashboard_page = GuidedRenewalTestEmployeeDashboardPage(feature_fixtures)
        review_and_submit_dashboard_page = ReviewAndSubmitDashboardPage(feature_fixtures)
        ssr_completion_dashboard_page = SSRCompletionDashboardPage(feature_fixtures)
        integrations_page = IntegrationsDashboardPage(feature_fixtures)
    return GuidedRenewalInit()