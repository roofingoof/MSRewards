def checkFileExists():
    try:
        f=open("MSAccounts.txt")
        f.close()
        return True
    except FileNotFoundError:
            return False

class MSAccount:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    def getEmail(self):
        return self.email
    def getPassword(self):
        return self.password


class MSAccountManager:
    def __init__(self):
        self.accounts = []
    def getAccounts(self):
        return self.accounts
    def loadFile(self):
        if not checkFileExists():
            #create the file
            print("Creating MSAccounts file!")
            open("MSAccounts.txt", "w+")
            print("Populate your accounts in here!")
            return False
        else:
            #exists
            # Format: email:password
            print("Found MSAccounts File, reading!")
            with open("MSAccounts.txt", "r") as MSAccountFile:
                MSAccountsList =MSAccountFile.read().splitlines()
                for MSAccountStr in MSAccountsList:
                    try:
                        emailandPass=  MSAccountStr.split(":::")
                        print(emailandPass)
                        msAccount= MSAccount(emailandPass[0], emailandPass[1])
                        self.accounts.append(msAccount)
                    except IndexError:
                        print("Add colon to seperate email and password!")
                        print("e.g asdfasdf@gmail.com:::978asdf")
                        return False
                return True
        


