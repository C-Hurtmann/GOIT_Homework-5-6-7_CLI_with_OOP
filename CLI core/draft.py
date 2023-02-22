
class Record:
    __instances = {}
    phone = []
    def __new__(cls, *args):
        if args[0] not in cls.__instances:
            cls.__instances[args[0]] = super().__new__(cls)
        return cls.__instances[args[0]]
    
    def __init__(self, name, phone=None):
        self.name = name
        if phone:
            self.phone.append(phone)

x = Record('Bob', '+6568411')
y = Record("Bob")

print(x == y, x is y)
print(x.phone)