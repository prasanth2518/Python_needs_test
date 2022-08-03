class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.email = f'{first}.{last}@email.com'

    def full_name(self):
        return f'{self.first}{self.last}'


emp_1 = Employee("prasanth", "utti")

print(emp_1.first)
print(emp_1.last)
print(emp_1.email)
print(emp_1.full_name())


# changing attr name as setattr

class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last

    def full_name(self):
        return f'{self.first}{self.last}'

    def email(self):
        return f'{self.first}.{self.last}@email.com'


emp_1 = Employee("prasanth", "utti")
emp_1.first = "Sreekanth"
print(emp_1.first)
print(emp_1.last)
print(emp_1.email())
print(emp_1.full_name())


class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last

    def full_name(self):
        return f'{self.first}{self.last}'

    @property
    def email(self):
        return f'{self.first}.{self.last}@email.com'


emp_1 = Employee("prasanth", "utti")
emp_1.first = "Sreekanth"
print(emp_1.first)
print(emp_1.last)
print(emp_1.email)
print(emp_1.full_name())
