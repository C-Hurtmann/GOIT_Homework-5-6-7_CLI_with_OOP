from handler import Handler, Request

while True:
    user_input = input('>')
    Handler()(Request(user_input))
    

