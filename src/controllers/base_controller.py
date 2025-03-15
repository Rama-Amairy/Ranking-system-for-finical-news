from config.app_config import load_config
from config.env_config import get_settings


class BaseController:

    def __init__(self):
        self.env_config = get_settings()
        self.app_config = load_config()
