from utils.ui_utils.orange_hrm.base_utils import BaseUtils


class LoginUtils(BaseUtils):

    def __init__(self,page):
        super().__init__(page)
        self.page = page

    def user_login(self,odict):
        self.page.goto(odict["URL"])
        self.login_page_obj.enter_username(odict["USERNAME"])
        self.login_page_obj.enter_password(odict["PASSWORD"])
        self.login_page_obj.login_click()