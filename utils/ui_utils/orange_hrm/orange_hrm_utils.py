from utils.ui_utils.orange_hrm.login_utils import LoginUtils


class OrangeHRMUtils(LoginUtils):

    def logout(self):
        self.login_page_obj.user_dropdown_click()
        self.login_page_obj.logout_click()