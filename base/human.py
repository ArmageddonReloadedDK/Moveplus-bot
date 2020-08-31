from org_commands.org_status_change import Status_change
from org_commands.reg_change import Regchange
from org_commands.write_to_person import write_to_person
from org_commands.family_search import Family_search_class
from base.base_human import Base_human_class



class Human_class(Base_human_class):

    def __init__(self):
        super().__init__()
        self.status = Status_change()
        self.reg_status = Regchange()
        self.write_to_person = write_to_person()
        self.family_search=Family_search_class()



