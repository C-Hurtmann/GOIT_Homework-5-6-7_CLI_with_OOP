from pathlib import Path

from bot.commands import AddressBook


class Autosave:
    """
    Reads address book from pkl file if it created
    Writes address book in the pkl file when bot has been stopped
    """
    def __init__(self, handler, filename='save.pkl'):
        self.handler = handler
        self.filename = Path(filename)

    def __enter__(self):
        if self.filename.is_file():
            self.handler.address_book = AddressBook(self.filename)
        return self.handler

    def __exit__(self, type, value, traceback):
        self.handler.address_book.save_data(self.filename)
