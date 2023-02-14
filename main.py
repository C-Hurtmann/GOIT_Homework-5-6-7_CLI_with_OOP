from collections import UserDict
from datetime import datetime
import re


class AddressBook(UserDict):
    def __init__(self):
        super().__init__(self)
        self.counter = 0
    
    def __iter__(self):
        return self
       
    def __next__(self):
        page = [i for i in self.data.keys()]
        if self.counter < len(page):
            result = self.data[page[self.counter]]
            self.counter += 1
            return result
        raise StopIteration
    

    def iterator(self, page_length):
        return [j for i, j in enumerate(self) if i < page_length]

    
    def add_record(self, record):
        self.data[record.name.value] = record
    
    
class Record:
    def __init__(self, name, phones = None, birthday = None):
        self.name = name
        self.phones = phones if isinstance(phones, list) else [phones]
        self.birthday = birthday
        
    def __repr__(self):
        return f'{self.name} | {self.birthday} | {self.phones}'
    
    def days_to_birthday(self):
        try:
            birthday_date = self.birthday.value.replace(year=datetime.now().year)
            days_left = (birthday_date - datetime.now()).days
            return f'{days_left} days left untill birthday'
        except AttributeError:
            return f'{self.name} has no birthday set'

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
        
    def __repr__(self):
        return f'{self.value}'  

class Name(Field):
    pass

class Phone(Field):
    @property    
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        value = re.sub(r'[\-\(\)\+ ]', '', value) # delete all the most common signs in phone record 
        if len(value) == 12:
            value = '+' + value
        elif len(value) == 10:
            value = '+38' + value
        elif len(value) == 9:
            value = '+380' + value
        else:
            raise ValueError('Phone is not valid')
        self.__value = value

            
class Birthday(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if isinstance(value, str):
            temp_date = list(map(int, re.findall(r'\d+', value)))
            temp_date = temp_date if len(str(temp_date[0])) == 4 else list(reversed(temp_date))
            try:
                if temp_date[0] > datetime.now().year:
                    raise ValueError
                temp_date = datetime(*temp_date)
            except ValueError:
                print('Date is not valid')
                self.__value = None
            else:
                self.__value = temp_date
        elif isinstance(value, datetime):
            self.__value = value
    
    def __repr__(self):
        if self.value:
            return self.value.strftime('%d %B')
        return ''


if __name__ == '__main__':
    name = Name('Bill')
    name2 = Name('Ben')
    name3 = Name('Constantine')
    phone = Phone('+380(99) 296 - 87 - 89')
    phone2 = Phone('992968788')
    birthday = Birthday('29.03.1995')
    birthday2 = Birthday('30.09.2005')
    rec = Record(name, [phone, phone2], birthday)
    rec2 = Record(name2, phone, birthday2)
    rec3 = Record(name3, phone)
    #print(rec.days_to_birthday())
    ab = AddressBook()
    ab.add_record(rec)
    ab.add_record(rec2)
    ab.add_record(rec3)
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '+380992968789'
    assert Phone('+380(99) 296 - 87 - 89').value == '+380992968789'
    assert Phone('992968789').value == '+380992968789'
    print(ab.iterator(4))
    print(ab.iterator(2))