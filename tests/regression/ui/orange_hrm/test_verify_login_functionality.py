import allure
import pytest

from test_data.orange_hrm_data import test_001 as idict
from utils.decorators import screenshot_on_failure, retry_on_failure, log_start_end
from utils.ui_client import UIClient


@allure.feature("ORANGE_HRM")
@allure.parent_suite("ORANGE_HRM")
@pytest.mark.regression
@pytest.mark.smoke
@screenshot_on_failure
@retry_on_failure()
@log_start_end
def test_verify_login_functionality(orange_hrm_utils,retry_count = None):
    odict = idict
    page = orange_hrm_utils
    odict["retries_counter"] = retry_count
    step = 1

    with allure.step(f"UI | Step {step}: Login to Orange HRM portal"):
        page.user_login(odict)
        UIClient.attach_ui_data("Login Page", odict)
        step += 1
