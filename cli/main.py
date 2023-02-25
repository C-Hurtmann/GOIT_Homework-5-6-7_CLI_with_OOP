from handler import Handler, Request

print('Bot Activated. Welcome')
handler = Handler()
while True:
    user_input = input('>')
    handler.run(Request(user_input))
    

