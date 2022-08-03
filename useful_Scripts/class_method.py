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


print(Employee.get_amount())

'''
Example
'''
