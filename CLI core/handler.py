import re

from commands import AddressBook, Record, Name, Phone, Birthday

class Handler:
    
    def __init__(self):
        self.address_book = AddressBook()
        self.main_commands = {'hello': None,
                              'add': self.add,
                              'change': self.change,
                              'search': None,
                              'show all': None,
                              'show': None,
                              'birthday': None}

    def add(self, request):
        command = request.create_command()[1]
        self.address_book.add_record(Record(**command))
        
    def change(self, request):
        command = request.create_command()[1]
        Record(name=command.pop('name')).change_field(**command)

class Request:
    def __init__(self, request: str):
        self.request = request
        self._request = None
        self.main_commands = Handler().main_commands
        
    def create_command(self):
        command = self.get_command()
        if command == 'add':
            name = self.get_name()
            birthday = self.get_birthday()
            phones = self.get_phone(self._request)
            return (command, {'name': name, 
                    'birthday': birthday, 
                    'phones': phones})
            
        elif command == 'change':
            name = Name(self.get_name())
            separator = self._request.find('to')
            first_half_request = self._request[:separator]
            second_half_request = self._request[separator:]
            old_field = self.get_phone(first_half_request)
            new_field = self.get_phone(second_half_request)
            return (command, {'name': name,
                              'old_field': old_field,
                              'new_field': new_field})
    
            
    def get_command(self):
        main_commands = self.main_commands.keys()
        for i in main_commands:
            command = re.search(fr'\b{i}\b', self.request, re.IGNORECASE)
            if command:
                self._request = re.sub(fr'{command.group()}', '', self.request).strip()
                return command.group().lower()
    
    def get_name(self):
        name = re.search(r"\b([A-Z][a-z]+)+", self._request)
        return Name(name.group())
    
    def get_phone(self, request):
        phones = re.findall(r'\b\+?[\(\)\-\d]+\b', request)
        if phones:
            return [Phone(i) for i in phones if Phone(i).value]
        
    def get_birthday(self):
        birthday = re.search(r'\d{,2}[/.-]\d{,2}[/.-]\d{,4}', self.request)
        if birthday:
            return Birthday(birthday.group())
    
test_req = Request('ADD Constantine  +3809894989, 6548941351, 135-2568-465 (23432)3423434 birthday 23/02/2023')
test_req2 = Request('change Constantine 3809894989, 6548941351 to 0951115544')
x = Handler()
x.add(test_req)
x.change(test_req2)
print(x.address_book)