import os # add the current directory to the path
import sys ## for local and module imports
sys.path.append(os.getcwd())
from .accounts.account import Account

class Event:
    def __init__(self, credit_dict={}, debit_dict={}, **kwargs):
        """ create a financial event """
        stop_cond = kwargs.get('stop_cond', lambda: False)
        if (not credit_dict) and (not debit_dict):
            raise ValueError('must pass a non-empty credit_dict or debit_dict')
        self.credit_dict = credit_dict
        self.debit_dict = debit_dict
        self.stop_cond = stop_cond
        self.stop = False

    def __call__(self):
        """ perform the event actions if the stop condition has not been met """
        if self.stop: return
        for account, amount in self.credit_dict.items():
            account.credit(amount)
        for account, amount in self.debit_dict.items():
            account.debit(amount)
        if self.stop_cond():
            self.stop = True
