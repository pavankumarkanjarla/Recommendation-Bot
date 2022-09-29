from rb_session import Session

session = Session()

print ('BOT: Hi! How may I assist you?')

while True:

    inp = input('User: ')
    if inp == "exit" :
        break
    print ('BOT:', session.reply(inp))
