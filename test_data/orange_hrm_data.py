from utils.config_reader import get_config

URL = get_config("ORANGE_HRM","URL","orange_hrm")
USERNAME = get_config("ORANGE_HRM","USERNAME","orange_hrm")
PASSWORD = get_config("ORANGE_HRM","PASSWORD","orange_hrm")

test_001 = {
    "URL":URL,"USERNAME":USERNAME,"PASSWORD":PASSWORD
}