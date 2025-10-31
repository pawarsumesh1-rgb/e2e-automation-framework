from utils.ui_utils.orange_hrm.base_utils import BaseUtils


class LoginUtils(BaseUtils):
    def user_login(self,odict):
        try:
            self.page.goto(odict["URL"])
            self.login_page_obj.enter_username(odict["USERNAME"])
            self.login_page_obj.enter_password(odict["PASSWORD"])
            self.login_page_obj.login_click()
            self.login_page_obj.login_status()
        except AssertionError:
            raise
        except Exception as e:
            assert False, f"Login failed: {e}"