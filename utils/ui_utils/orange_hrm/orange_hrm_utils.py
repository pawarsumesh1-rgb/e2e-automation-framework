from utils.ui_utils.orange_hrm.login_utils import LoginUtils


class OrangeHRMUtils(LoginUtils):

    def __init__(self,page):
        super().__init__(page)
        self.page = page