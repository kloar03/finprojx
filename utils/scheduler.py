from collections import defaultdict
import datetime
from dateutil import rrule

ISO_map = {
    'monday':       1,
    'tuesday':      2,
    'wednesday':    3,
    'thursday':     4,
    'friday':       5,
    'saturday':     6,
    'sunday':       7
}

UNITS = [
    'days',
    'weeks',
    'months',
    'years'
]

class Scheduler:
    """ a class to schedule calendar events """
    def __init__(self, final_year: int=2100):
        self.events = defaultdict(list)
        self.func_map = dict()
        self.final_year = final_year
    
    def __getitem__(self, key):
        return [self.func_map[name] for name in self.events[key]]

    def __contains__(self, item):
        return item in self.events

    def add_event(self, key: str, func, date: datetime.date, rule: str) -> None:
        """ schedules an event for an account """
        if not ( bool(date) or bool(rule) ):
            raise ValueError('must pass at least one of date and rule')
        # the account function to be scheduled
        self.func_map[key] = func
        if not date:
            date = datetime.date(2020,1,1) 
        if not rule:
            rule = 'every month'
        # parse the rule
        freq, units = self.parse_rule(rule)
        # get the last day
        last_day = datetime.date(self.final_year, 12, 31)
        # build the schedule
        sched = self.build_schedule(date, freq, units, until=last_day)
        for event_date in sched:
            e_date = datetime.date(event_date.year,
                                    event_date.month,
                                    event_date.day)
            self.events[e_date].append(key)
    
    def remove_event(self, key: str, before: datetime.date=None, after: datetime.date=None) -> None:
        """ removes a scheduled event """
        valid_dates = [d for d in self.events if key in self.events[d]]
        if before:
            valid_dates = [d for d in valid_dates if d < before]
        if after:
            valid_dates = [d for d in valid_dates if d > after]
        # now we have only events with our key and valid dates
        for d in valid_dates:
            self.events[d].remove(key)
    
    def generate_days(self, year):
        """ yield all of the days with events in the current year """
        today = datetime.date.today()
        first_day = today if today.year == year else datetime.date(year, 1, 1)
        last_day = datetime.date(year, 12, 31)
        days = sorted([day for day in self.events.keys() if day.year == year])
        days.insert(0, first_day)
        days.insert(-1, last_day)
        for idx in range(1, len(days)): # yield the fence, not the posts
            yield days[idx-1], days[idx]

    @staticmethod
    def build_schedule(date, freq, units, until=None):
        """ build the event schedule """
        if freq == 'once':
            freq_val = 1000*365 # an enormous value to ensure we don't increment
        elif freq == 'every':
            freq_val = 1
        elif freq == 'second':
            freq_val = 2
        elif freq == 'third':
            freq_val = 3
        elif freq == 'fourth':
            freq_val = 4
        else:
            raise ValueError(f'invalid freq passed: {freq}')

        if freq == 'once':
            freq_units = rrule.DAILY # value doesn't matter here
        elif units == 'days':
            freq_units = rrule.DAILY
        elif units == 'weeks':
            freq_units = rrule.WEEKLY
        elif units == 'months':
            freq_units = rrule.MONTHLY
        elif units == 'years':
            freq_units = rrule.YEARLY
        else:
            raise ValueError('invalid units passed')
        
        return rrule.rrule(freq=freq_units, interval=freq_val,
                            dtstart=date, until=until)

    @classmethod
    def parse_rule(self, rule) -> tuple:
        """ a helper function to parse rules and return their function """
        freq = self.clean_frequency(rule)
        rule_tokens = rule.split(' ')
        cleaned_tokens = list(map(self.clean_units, rule_tokens))
        units = None
        for token in cleaned_tokens:
            if token in UNITS: units = token
        return freq, units

    @classmethod
    def clean_units(self, string):
        """ format the units for the rule """
        if string in ['d','day','days']:
            return 'days'
        elif string in ['w', 'week', 'weeks']:
            return 'weeks'
        elif string in ['m', 'month', 'months']:
            return 'months'
        elif string in ['y', 'year', 'years']:
            return 'years'
        else: # no units identified
            return string

    @classmethod
    def clean_frequency(self, string):
        """ format the frequency of the rule """
        if 'once' in string:
            return 'once'
        elif 'every other' in string:
            return 'second'
        elif 'every second' in string:
            return 'second'
        elif 'every two' in string:
            return 'second'
        elif 'every third' in string:
            return 'third'
        elif 'every three' in string:
            return 'third'
        elif 'every fourth' in string:
            return 'fourth'
        elif 'every four' in string:
            return 'fourth'
        elif 'every' in string:
            return 'every'
        else:
            return None

