from collections import UserDict
from datetime import datetime
import pickle
import re


class AddressBook(UserDict):
    
    def __init__(self, filename=None):
        super().__init__(self)
        if filename:
            self.data = self.read_data(filename)

    def __str__(self):
        lines_qty = len(self.data.keys())
        return '\n'.join(self.iterator(lines_qty))

    def get_header(self):
        return '{:^15}|{:^15}|{:^15}\n'.format('Name', 'Birthday', 'Phones') + '=' * 50

    def iterator(self, page_length):
        yield self.get_header()
        for i, v in enumerate(self.values()):
            if i < page_length:
                name = str(v.name)
                try:
                    birthday = str(v.birthday)
                except AttributeError:
                    birthday = ''
                try:
                    phones = ', '.join(list(map(str, v.phones)))
                except AttributeError:
                    phones = ''
                yield '{:15}|{:15}|'.format(name, birthday) + f'{phones}'

    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, search):
        lines_qty = len(self.data.keys())
        table = list(self.iterator(lines_qty))
        match = [i for i in table if i.find(search) != -1]
        return '\n'.join([self.get_header()] + match)

    def save_data(self, filename):
        with open(filename, 'wb') as fh:
            pickle.dump(self.data, fh)

    def read_data(self, filename):
        with open(filename, 'rb') as fh:
            reader = pickle.load(fh)
            Record._instances = reader
            return reader


class Record:
    """
    This is a value of Address Book
    Based on singleton pattern so no need to change address book value directly.
    Can be called many times with adding some info. Previous filled info will be saved
    
    """
    _instances = {}

    def __new__(cls, **kwargs):
        try:
            name = kwargs['name'].value
        except KeyError:
            return super().__new__(cls)
        else:
            if name not in cls._instances:
                cls._instances[name] = super().__new__(cls)
            return cls._instances[name]

    def __init__(self, name, phones=[], birthday=None):
        self.name = name
        if birthday:
            self.__birthday = None
            self.birthday = birthday

        if phones:
            try:
                self.__phones = self.__phones
            except AttributeError:
                self.__phones = []

            self.phones = phones

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        if birthday:
            self.__birthday = birthday

    @property
    def phones(self):
        return self.__phones

    @phones.setter
    def phones(self, phones):
        if phones:
            self.__phones += phones

    def __repr__(self):
        try:
            return f'{self.birthday} | {self.phones}'
        except AttributeError:
            return 'None'

    def days_to_birthday(self):
        """
        Counts days to birthday for the Record if it has birthday field
        """
        try:
            birthday_date = self.birthday.value.replace(year=datetime.now().year)
        except AttributeError:
            return f'{self.name} has no birthday set'
        now = datetime.now()
        if now > birthday_date:
            now = birthday_date.replace(year=now.year + 1)
        days_left = abs((birthday_date - now).days + 1)
        return f'{days_left} days left untill birthday'

    def change_field(self, old_field: list, new_field: list):
        """
        Changes phone numbers in the Record

        Args:
            old_field (list): list of excisting phones in record, this func should remove
            new_field (list): list of phones, this func should add instead of old_field
        """
        phone_values = [i.value for i in self.phones]
        for i in old_field:

            self.phones.pop(phone_values.index(i.value))
        self.phones.extend(new_field)
        return f'Phone {old_field} have been changed to {new_field}'


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
    def value(self, value: str):
        value = re.sub(r'[\-\(\)\+ ]', '', value)  # delete all the most common signs in phone record 
        if len(value) == 12:
            value = '+' + value
        elif len(value) == 10:
            value = '+38' + value
        elif len(value) == 9:
            value = '+380' + value
        else:
            value = None
        self.__value = value


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        temp_date = list(map(int, re.findall(r'\d+', value)))
        temp_date.reverse()
        try:
            if temp_date[0] > datetime.now().year:
                raise ValueError
            temp_date = datetime(*temp_date)
        except ValueError:
            print('Date is not valid')
            self.__value = None
        else:
            self.__value = temp_date

    def __repr__(self):
        if self.value:
            return self.value.strftime('%d %B')
        return ''


if __name__ == '__main__':
    name = Name('Bill')
    name2 = Name('Bob')
    name3 = Name('Constantine')
    phone = [Phone('+380(99)296-87-89')]
    phone2 = [Phone('(95) 552 21 00'), Phone('0995552211')]
    phone3 = [Phone('0655221133')]
    birthday = Birthday('29.03.1995')
    birthday2 = Birthday('30.09.2005')
    rec = Record(name=name, phones=phone, birthday=birthday)
    rec2 = Record(name=name2, phones=phone2, birthday=birthday2)
    rec3 = Record(name=name3, birthday=birthday, phones=phone3)
    ab = AddressBook()
    ab.add_record(rec)
    ab.add_record(rec2)
    ab.add_record(rec3)
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    ab.save_data('save.pkl')
    reader = ab.read_data('save.pkl')
    print(reader)
    print(Record._instances == reader)
