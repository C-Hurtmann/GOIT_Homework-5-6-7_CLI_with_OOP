import re
from inspect import signature

import core.commands as cmd

main_commands = {'hello': cmd.hello,
                 'add': cmd.add,
                 'change': cmd.change,
                 'phone': cmd.phone,
                 'show all':cmd.show_all
                 }

def input_error(func):
    def inner(command, name, phone):
        if not command:
            commands_description = ''.join([f'{k}--{v.__doc__}\n' for k, v in main_commands.items()])
            return "Sorry, I don't understand you\n" + "Here is a list of commands I know:\n" + commands_description
        try:
            return func(''.join(command).lower(), name, ''.join(phone))
        except KeyError:
            return 'Your request must have only one command'
        except ValueError:
            return 'This command must contain more arguments'
    return inner
        
def input_proceccing(func):
    def inner(request: str):
        commands = '|'.join(i for i in main_commands.keys())
        command  = re.findall(r'{}'.format(commands), request, re.IGNORECASE)
        phone = re.findall(r'\+?\d+', request)
        name = request.replace(''.join(command), '').replace(''.join(phone), '').strip()
        return func(command, name, phone)
    return inner 


@input_proceccing
@input_error
def command_launch(command, name=None, phone=None):
    command = main_commands[command]
    if len(signature(command).parameters) == 2:
        if not name or not phone:
            raise ValueError
        return command(name, phone)
    elif len(signature(command).parameters) == 1:
        if not name:
            raise ValueError
        return command(name)
    elif len(signature(command).parameters) == 0:
        return command()
        

def testing():
    # print(command_launch('+3809849'))
    print(command_launch('add change Constantine Zagorodnyi 38099909'))    
    print(command_launch('add Constantine Zagorodnyi +308813510'))
    print(command_launch('change Constantine Zagorodnyi +30890999'))
    # print(command_launch('phone Constantine Zagorodnyi'))
    # print(command_launch(''))
    # find_command('add')
    # find_command('Add someone to mine phone book')
    # find_command('Could YOU ADD this number to my phone book')
    # find_command('Could you show me phone number without adding to my phone book?')
    # find_command('123')
    


if __name__ == '__main__':
    testing()