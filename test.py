def savewrite(filterList, filename):
    f = open(filename, "a")
    f.write(filterList.lower()+ "\n")
    f.close()


def loadwrite(filename):
    f = open(filename, "r")
    filterList = f.readlines()

    for i in range(0, len(filterList)):
        filterList[i] = filterList[i][:len(filterList[i]) - 1]

    f.close()
    return filterList




username = input('username')
x = loadwrite('userid.txt')
if username.lower() not in x:
    newuser = input('youre not in here, add your username')
    savewrite(newuser.lower().title(),'userid.txt')
    print(loadwrite('userid.txt'))

elif username.lower().split() == '':
    print('failed to connect')

elif username.lower() in x:
    user = input('what would you liek to do')
    if user.lower() == 'change waifu':
        x = loadwrite('userwaifu.txt')
        user1 = input('who is your new waifu')
        savewrite(str(user1.lower()), 'userwaifu.txt')

        print(x[x.index(user1)])
    elif user.lower() == 'nothing':
        x = loadwrite('userwaifu.txt')
        print(x)
    if user.lower() == 'remove':

        x = loadwrite('userwaifu.txt')
        v = loadwrite('userid.txt')
        u1 = x[v.index(username)]

        # Read in the file
        with open('userwaifu.txt', 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(u1, 'towa')

        # Write the file out again
        with open('userwaifu.txt', 'w') as file:
            file.write(filedata)

        print(loadwrite('userwaifu.txt'))

print()