from pages.orange_hrm.login_page import LoginPage


class BaseUtils:

    def __init__(self,page):
        self.page = page
        self.login_page_obj = LoginPage(self.page)