'''
statis methods not pass first object as instance or class automatically


it doesnot depends on any specifi instance or class varible
'''

"""
its an alternative constructor
"""


# through instance

class Employee:
    amount = 12

    def get_amount(self):
        return self.amount


e = Employee()
print(e.get_amount())


# theough class as an argument instead of instance

class Employee:
    raise_amount = 12

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f"{first}.{last}@email.com"

    @classmethod
    def get_amount(cls):
        return cls.raise_amount

    @classmethod
    def form_str(cls, _str):
        first, last, pay = _str.spilt("-")
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True


print(Employee.get_amount())

import datetime

_date = datetime.date(2018, 9, 3)

print(Employee.is_workday(_date))

'''
Example
'''
