import os # add the current directory to the path
import sys ## for local and module imports
sys.path.append(os.getcwd())
from .accounts.account import Account

class Event:
    def __init__(self, credit_list=[], debit_list=[], **kwargs):
        """ create a financial event """
        stop_cond = kwargs.get('stop_cond', lambda: False)
        if (not credit_list) and (not debit_list):
            raise ValueError('must pass a non-empty credit_list or debit_list')
        self.credit_list = credit_list
        self.debit_list = debit_list
        self.stop_cond = stop_cond
        self.stop = False

    def __call__(self):
        """ perform the event actions if the stop condition has not been met """
        if self.stop: return
        for action in self.credit_list:
            action()
        for action in self.debit_list:
            action()
        if self.stop_cond():
            self.stop = True
