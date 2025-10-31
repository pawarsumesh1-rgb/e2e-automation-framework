from pages.orange_hrm.base_page import BasePage
from utils.config_reader import get_config
from utils.logger import get_logger

logger = get_logger()


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.username_locator = get_config("LOGIN_XPATH","username_xpath","orange_hrm")
        self.password_locator = get_config("LOGIN_XPATH", "password_xpath", "orange_hrm")
        self.login_button_locator = get_config("LOGIN_XPATH", "login_button_xpath", "orange_hrm")
        self.login_status_locator = get_config("LOGIN_XPATH", "login_status_xpath", "orange_hrm")
        self.logout_locator = get_config("LOGIN_XPATH", "logout_xpath", "orange_hrm")

    def enter_username(self,username):
        self.fill_text(self.username_locator,username)

    def enter_password(self,password):
        self.fill_text(self.password_locator,password)

    def login_click(self):
        self.click(self.login_button_locator)

    def login_status(self):
        try:
            self.get_locator(self.login_status_locator)
            logger.info("login to orange hrm portal successful")
        except:
            logger.info("login to orange hrm portal failed")
            assert False

    def user_dropdown_click(self):
        self.click(self.login_status_locator)
    def logout_click(self):
        self.click(self.logout_locator)


