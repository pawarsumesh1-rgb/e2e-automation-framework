import configparser
import os
import pathlib as pl
Path = pl.Path
path = Path(__file__)
ROOT_DIR = path.parent.parent.absolute()

def config_reader(module: str = ""):
    """
    :return: config reader object for config.ini
    """
    if module != "":
        config_path = os.path.join(ROOT_DIR, f"configurations/{module}_config.ini")
    else:
        config_path = os.path.join(ROOT_DIR, f"configurations/config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def config_reader_CR(section, key) -> str:
    """
    :param section: str : section in config.properties
    :param key: str : key of key=value pair in config.properties
    :param module: str : module to refer for config
    :return: str : value of key=value pair in config.properties
    """
    config = config_reader()
    value = config.get(section, key)
    return value


def get_path(path_key, page="nan") -> str:
    """
    :param path_key: str : key of key=value pair in config.properties
    :param page: str : page name / page title / json file name
    :return: str : path of file or folder
    """
    if page == "nan":
        value = config_reader_CR(section="PATHS", key=path_key)
        path = str(ROOT_DIR) + value
    else:
        value = config_reader_CR(section="PATHS", key=path_key).replace("page", page)
        path = str(ROOT_DIR) + value
    return path


def config_path(section, key) -> str:
    """
    :param section: str : section in config.properties
    :param key: str : key of key=value pair in config.properties
    :return: str : value of key=value pair in config.properties
    """
    config = config_reader()
    value = config.get(section, key)
    path = str(ROOT_DIR) + value
    return path


def get_config(section, key,module) -> str:
    """
    :param section: str : section in config.properties
    :param key: str : key of key=value pair in config.properties
    :return: str : value of key=value pair in config.properties
    """
    config = config_reader(module)
    value = config.get(section, key)
    return value


def get_config_value(section, key) -> str:
    """
    :param section: str : section in config.properties
    :param key: str : key of key=value pair in config.properties
    :return: str : value of key=value pair in config.properties
    """
    config = config_reader()
    value = config.get(section, key)
    return value