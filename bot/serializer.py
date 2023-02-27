from pathlib import Path

from commands import AddressBook, Record

class Autosave:
    def __init__(self, handler, filename='save.pkl'):
        self.handler = handler
        self.filename = Path(filename)
        
    def __enter__(self):
        if self.filename.is_file():
            self.handler.address_book = AddressBook(self.filename)
        return self.handler
    
    def __exit__(self, type, value, traceback):
        self.handler.address_book.save_data(self.filename)
        
        