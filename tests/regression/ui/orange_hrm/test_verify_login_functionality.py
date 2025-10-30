from test_data.orange_hrm_data import test_001 as idict
def test_verify_login_functionality(orange_hrm_utils):
    odict = idict
    page = orange_hrm_utils

    page.user_login(odict)
