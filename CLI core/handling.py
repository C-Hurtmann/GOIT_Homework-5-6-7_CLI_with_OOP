import re

from commands import AddressBook, Record, Name, Phone, Birthday

class Interface:
    
    main_commands = {'hello': None,
                     'add': None,
                     'change': None,
                     'search': None,
                     'show all': None,
                     'show': None,
                     'birthday': None}
    
    def __init__(self):
        self.address_book = AddressBook()

    def add(self, request):
        command = request.create_command()
        del command['command']
        self.address_book.add_record(Record(**command))

class Request:
    def __init__(self, request: str):
        self.request = request
        self._request = None
        
    def create_command(self):
        command = self.get_command()
        name = Name(self.get_name())
        birthday = Birthday(self.get_birthday())
        phones = [Phone(i) for i in self.get_phone() if Phone(i).value]
        return {'command': command, 
                'name': name, 
                'birthday': birthday, 
                'phones': phones}
        
        
    def __cut_request(self, value):
        self._request = re.sub(fr'{value}', '', self.request).strip()

    def get_command(self):
        main_commands = Interface.main_commands.keys()
        for i in main_commands:
            command = re.search(fr'\b{i}\b', self.request, re.IGNORECASE)
            if command:
                self.__cut_request(command.group())
                return command.group().lower()
    
    def get_name(self):
        name = re.search(r"\b([A-Z][a-z]+)+", self._request)
        return name.group()
    
    def get_phone(self):
        phones = re.findall(r'\b\+?[\(\)\-\d]+\b', self.request)
        if phones:
            return phones
        
    def get_birthday(self):
        birthday = re.search(r'\d{,2}[/.-]\d{,2}[/.-]\d{,4}', self.request)
        if birthday:
            return birthday.group()
    
test_req = Request('ADD Constantine Zagorodnyi  +3809894989, 6548941351, 135-2568-465 (23432)3423434 birthday 23/02/2023')

x = Interface()
x.add(test_req)
print(x.address_book)