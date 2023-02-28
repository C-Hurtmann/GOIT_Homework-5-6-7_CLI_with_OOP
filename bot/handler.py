from random import choice
import re

from commands import AddressBook, Record, Name, Phone, Birthday

class Handler:
    """
    Bot processor
    Keeps Address Book object
    Directs info prepared by the Request object to the command
    """
    def __init__(self):
        self.address_book = AddressBook()
        self.main_commands = {'hello': self.hello,
                              'add': self.add,
                              'change': self.change,
                              'search': self.search,
                              'show all': self.show_all,
                              'show': self.show,
                              'birthday': self.get_birthday}

    def run(self, request: tuple[str, dict]):
        return self.main_commands[request.create_command()[0]](request)
    
    def hello(self, request: None): # No need info for this command
        responces = ['Hi!',
                     'How can I help you?',
                     'How are you?',
                     ]
        print(choice(responces))

    def add(self, request: dict):
        command = request.create_command()[1]
        self.address_book.add_record(Record(**command))
        print('Line has been added')
        
    def change(self, request: dict):
        command = request.create_command()[1]
        record = Record(name=command.pop('name'))
        print(record.change_field(**command))
        
    def search(self, request: dict):
        command = request.create_command()[1]
        print("Here what I've found")
        print(self.address_book.search(**command))
        
    def get_birthday(self, request: dict):
        command = request.create_command()[1]
        print(Record(name=command['name']).days_to_birthday())
        
    def show(self, request: dict):
        command = request.create_command()[1]
        print("Here what I've got")
        for i in self.address_book.iterator(command):
            print(i)
        
    def show_all(self, request: None): # No need info for this command
        print(self.address_book)

class Request:
    """
    Receives user input
    Returns info in satisfying for Handler format
    """
    def __init__(self, request: str):
        self.request = request
        self.__request = None
        self.main_commands = Handler().main_commands
        
    def create_command(self) -> tuple[str, dict]:
        """
        Collecting info for the command

        Returns:
            tuple[str, dict]: (command name, command info dict)
        """
        command = self.__get_command()
        
        if command == 'add':
            name = self.__get_name()
            birthday = self.__get_birthday()
            phones = self.__get_phone(self.__request)
            return (command, {'name': name, 
                              'birthday': birthday, 
                              'phones': phones})
            
        elif command == 'change':
            name = self.__get_name()
            separator = self.__request.find('to')
            first_half_request = self.__request[:separator]
            second_half_request = self.__request[separator:]
            old_field = self.__get_phone(first_half_request)
            new_field = self.__get_phone(second_half_request)
            return (command, {'name': name,
                              'old_field': old_field,
                              'new_field': new_field})
            
        elif command == 'search':
            search = self.__request
            return (command, {'search': search})
            
        elif command == 'birthday':
            name = self.__get_name()
            return (command, {'name': name})
        
        elif command in ('hello', 'show all'):
            return (command, )
        
        elif command == 'show':
            page_length = re.search(r'\d+', self.__request).group()
            return (command, int(page_length))
            
    def __get_command(self):
        main_commands = self.main_commands.keys()
        for i in main_commands:
            command = re.search(fr'\b{i}\b', self.request, re.IGNORECASE)
            if command:
                self.__request = re.sub(fr'{command.group()}', '', self.request).strip()
                return command.group().lower()
    
    def __get_name(self):
        name = re.search(r"\b([A-Z][a-z]+)+", self.__request)
        return Name(name.group())
    
    def __get_phone(self, request: str):
        phones = re.findall(r'\b\+?[\(\)\-\d]+\b', request)
        if phones:
            return [Phone(i) for i in phones if Phone(i).value]
        
    def __get_birthday(self):
        birthday = re.search(r'\d{,2}[/.-]\d{,2}[/.-]\d{,4}', self.__request)
        if birthday:
            return Birthday(birthday.group())


if __name__ == '__main__':    
    test_req = Request('ADD Bill  +3809894989, 6548941351, 135-2568-465 (23432)3423434 birthday 25/02/2023')
    test_req2 = Request('change Bill 3809894989, 6548941351 to 0951115544')
    test_req3 = Request('get birthday Bill')
    test_req4 = Request('show 5 lines')

    x = Handler()
    x.add(test_req)
    x.change(test_req2)
    x.get_birthday(test_req3)
    x.show(test_req4)