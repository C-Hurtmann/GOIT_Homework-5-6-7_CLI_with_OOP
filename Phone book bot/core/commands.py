from collections import UserDict

phone_book = {}

class PhoneBook(UserDict):
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __getitem__(self, key):
        return self.data[key]
    
    def get_phone(self, name):
        if not phone_book_object.get(name):
            return 'No such name in you phone book'
        return phone_book_object.get(name).get('phone')
    
    def get_email(self, name):
        if not phone_book_object.get(name):
            return 'No such name in you phone book'
        return phone_book_object.get(name).get('email')
    
    def show_all(self):
        result_table = ['Here is your phone book:']
        for name, values in phone_book_object.items():
            for k, v in values.items():
                result_table.append(f'{name:<10}|{k:^10}|{v:^10}')
        return result_table
    
phone_book_object = PhoneBook()

class Record:
    def __init__(self, name, phone = None, email = None):
        self.name = Name(name).view()
        self.phone = Phone(phone).view()
        self.email = Email(email).view()
    
    def add(self):
        """Recive name and phone. If it's a new name in your phone book, save them"""
        name = self.name
        values = vars(self)
        del values['name']
        if not phone_book_object.get(name):
            phone_book_object[name] = values
            return f'{values.values()} has been saved for {name}'
        new_values = {}
        for dct in [phone_book_object[name], values]:
            for k, v in dct.items():
                if isinstance(v, list):
                    new_values.setdefault(k, []).extend(v)
                    continue
                new_values.setdefault(k, []).append(v)
        phone_book_object[name] = new_values
        return f'{values.values()} has been saved for {name}'
    
    def change(self):
        name = self.name
        values = vars(self)
        del values['name']
        if not phone_book_object.get(name):
            return 'No such name in you phone book'
        if len(values) == 2:
            old_values = phone_book_object[name]
            phone_book_object[name] = values
        return f'Values {old_values} have been changed to {values} for {name}'
        
    
    def get_phone(self):
        name = self.name
        if not phone_book_object.get(name):
            return 'No such name in you phone book'
        return phone_book_object.get(name).get('phone')

class Field:
    def __init__(self, value = None):
        self.value = value
    
    def view(self):
        return self.value


class Name(Field):
    def __init__(self, name):
        self.value = name

class Phone(Field):
    pass

class Email(Field):
    pass


def hello() -> str:
    """Just respond on hello"""
    return 'How can I help you?'


def add(name: str, phone: str) -> str:
    """Recive name and phone. If it's a new name in your phone book, save them """
    if not phone_book.get(name):
        phone_book[name] = phone
        return f'{name} has been saved in your phone book with number {phone}'
    return f'{name} already exists in your phone book. Number is {phone_book.get(name)}'


def change(name: str, new_phone: str) -> str:
    """Receive name and phone. If this name excists in your phone book, save new number for him """
    old_phone = phone_book.get(name)
    if old_phone:
        phone_book[name] = new_phone
        return f'''For {name} the number has been
                    changed from {old_phone} to {new_phone}'''
    return f'No such user in your phone book'


def phone(name: str) -> str:
    """eceive name. If this name ixcists in your phone book, show his number"""
    if phone_book.get(name):
        return f'Phone of {name} is {phone_book.get(name)}'
    return f'No such user in your phone book'


def show_all() -> str:
    """Show all contacts in your phone book"""
    result_table = ['Here is your phone book:']
    for k, v in phone_book.items():
        result_table.append(f'{k:<10}|{v:<10}')
    return '\n'.join(result_table)




if __name__ == '__main__':
    Record('Ben', '+308453').add()
    Record('Ben', '+3434', 'con@gmail.com').add()
    Record('Ben', '+3084554654983').add()
    Record('Alex', '+308453').add()
    Record('Alex', '+65654+84').change()
    print(phone_book_object)
    # print(phone_book_object.get_phone('Alex'))
    print(phone_book_object.show_all())