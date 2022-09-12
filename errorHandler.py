from time import localtime

def get_current_time(): #this gets the current time
    time2 = localtime()
    hour = time2[3] - 12 if time2[3] > 12 else time2[3]
    amPm = 'PM' if time2[3] > 12 else 'AM'
    fullTime = f'{time2[1]}/{time2[2]}/{time2[0]} {hour}:{time2[4]}:{time2[5]} {amPm}'
    return fullTime

def handleError(error): #logs the errors to errors.txt
    currTime = get_current_time()
    with open('errors.txt', 'a') as outfile:
        outfile.write('\n')
        outfile.write(f'{error} | {currTime}')