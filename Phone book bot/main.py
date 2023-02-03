from core.parcing import command_launch

if __name__ == '__main__':
    print('Bot awakened.')
    while True:
        user_input = input('Enter your request:')
        if not user_input.lower() in ('"good bye", "close", "exit"'):
            print(command_launch(user_input))
            print('-' * 50)
        else:
            print("Good bye!")
            break
