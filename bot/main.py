from handler import Handler, Request
from serializer import Autosave

QUIT_WORDS = ('bye', 'quit', 'good bye', 'exit') 
with Autosave(Handler()) as handler:

    print('Bot Activated. Welcome')

    while True:
        user_input = input('>')
        if user_input.lower() in QUIT_WORDS:
            print('Good bye!')
            break
        handler.run(Request(user_input))

