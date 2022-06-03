from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class UltiProLoginPage(BasePage):
    LOGIN_USERNAME = By.ID, "ctl00_Content_Login1_UserName"
    LOGIN_PASSWORD = (By.ID, "ctl00_Content_Login1_Password")
    LOGIN_BUTTON = (By.ID, "ctl00_Content_Login1_LoginButton")

    def __init__(self, driver):
        super().__init__(driver)

    def goto(self):
        url = f"{self.config['base_urls']['ulti_pro_login']}"
        self.goto_page(url)

    def goto_prod_demo_ulti(self):
        url = f"{self.config['base_urls']['ulti_pro_prod_demo_login']}"
        self.goto_page(url)