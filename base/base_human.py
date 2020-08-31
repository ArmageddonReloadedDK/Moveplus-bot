from settings import config
from .base_psql import base_psql_class
from .base_vedis import base_vedis_class



class Base_human_class(base_psql_class, base_vedis_class):
    def __init__(self):
        super().__init__()
        self.bot = config.get_bot()
