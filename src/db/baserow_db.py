import requests
import json
import pandas as pd
import replicate
from IPython.display import Image
import os
# load env
from dotenv import load_dotenv

load_dotenv()

# load env

class BaserowTable:
    def __init__(self, table_id : int):
        self.table_id = table_id

    # list rows
    def get_list_rows(self, page : int = None, size : int = None, search : str = None):
        pass
    def get_row(self, row_id : int):
        pass

    # create row
    def create_row(self, data : dict):
        pass

    def update_row(self, row_id : int, data : dict):
        pass



#
class DechetsTable(BaserowTable):
    def __init__(self):
        super().__init__(table_id = 12345)

    def get_list_dechets(self, filter_by_class : str = None):
        pass





