from errorHandler import handleError
from cryptography.fernet import Fernet

def getKey():
    key = (open('key.key', 'rb')).read()
    return key

def encrypyNote(noteId):
    key = getKey()
    fernet = Fernet(key)
    
    data = (open(f'allNotes/{noteId}.json', 'rb')).read()

    encrypyed = fernet.encrypt(data)
    
    with open(f'allNotes/{noteId}.json', 'wb') as outfile:
        outfile.write(encrypyed)
        
def decrypyNote(noteId):
    key = getKey()
    fernet = Fernet(key)
    
    data = (open(f'allNotes/{noteId}.json', 'r')).read()
    
    data_decoded = bytes(data, 'UTF-8')
    decrypyed = fernet.decrypt(data_decoded)
    
    with open(f'allNotes/{noteId}.json', 'wb') as outfile:
        outfile.write(decrypyed)
        
def fileCryption(cryptionType, noteId):
    try:
        if cryptionType == 'decrypt':
            decrypyNote(noteId)
        if cryptionType == 'encrypt':
            encrypyNote(noteId)
    except Exception as err:
        handleError(err)