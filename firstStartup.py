import json

def firstStartUp():
    from os import mkdir, path
    from cryptography.fernet import Fernet
    # from errorHandler import handleError

    if not path.exists('allNotes/'):
        mkdir('allNotes')
    
    if not path.exists('allNotes/key.key'):
        key = Fernet.generate_key()
        with open('allNotes/key.key', 'wb') as file:
            file.write(key)
            file.close()
        
    if not path.exists('errors.txt'):
        with open('errors.txt', 'x') as create:
            create.close()
    
    if not path.exists('allNotes/allUsers.json'):
        with open('allNotes/allUsers.json', 'x') as create:
            jsonObject = json.dumps({})
            create.write(jsonObject)
            create.close()