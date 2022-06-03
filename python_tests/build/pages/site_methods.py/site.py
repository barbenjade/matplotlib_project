from selenium.webdriver.common.by import By
from pages.enrollment.enrollment_page import EnrollmentPage


class EnrollmentAccountDetailsPage(EnrollmentPage):
    # locators region
    SUBSCRIBER_ACCOUNT_INFO_EDIT_LINK = By.XPATH, "//button[normalize-space()='Edit Info']"
    SUBSCRIBER_ACCOUNT_INFO_SAVE_BUTTON = By.XPATH, "//span[text()='Save']/parent::button[@type = 'submit']"

    MFA_ADD_PHONE_TEXT = By.XPATH, "//a[text()='Add Phone']"
    PHONE_NUMBER_TEXT_FIELD = By.ID, "mobile_number"
    PHONE_NUMBER_CONFIRM_BUTTON = By.XPATH, "//span[text()='Confirm']/parent::button"

    MFA_BACKUP_CODES_SETUP_TEXT = By.XPATH, "//span[text()='Backup Codes']/parent::div//a"
    GET_NEW_CODES_LINK = By.XPATH, "//button[text()='Get New Codes']"
    BACKUP_CODES_POPUP_CLOSE_BUTTON = By.XPATH, "//button[text()='Close']"

    FORGET_DEVICES_EL = By.XPATH, "//a[normalize-space()='Forget Devices']"
    FORGET_DEVICES_YES_BUTTON = By.XPATH, "//button[normalize-space() = 'Yes']"

    CHANGE_PASSWORD_BUTTON = By.XPATH, "//button[@class='btn btn-link btn-lg fa-pencil has-fa-left']"
    CURRENT_PASSWORD_TEXT_FIELD = By.ID, "current_password"
    NEW_PASSWORD_TEXT_FIELD = By.ID, "new_password"
    CONFIRM_NEW_PASSWORD_TEXT_FIELD = By.ID, "confirm_new_password"

    ALERT_MESSAGE = By.XPATH, "//div[@role='alert']"

    # end region Locators

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{self.config['base_urls']['benefits']}/subscriber/account"

    def goto(self):
        self.goto_page(self.url)

    # region Edit Info Methods
    def click_edit_info_link(self):
        self.click_element(self.SUBSCRIBER_ACCOUNT_INFO_EDIT_LINK)

    def click_save_button(self):
        self.click_element(self.SUBSCRIBER_ACCOUNT_INFO_SAVE_BUTTON)

    # end region Edit Info Methods

    # region Add Phone(Text) Methods
    def add_mfa_phone_number(self, phone_number):
        self.click_add_mfa_phone()
        self.enter_mobile_phone_number(phone_number)
        self.click_confirm_mobile_phone_number()