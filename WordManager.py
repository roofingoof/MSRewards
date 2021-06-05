def checkFileExists():
    try:
        f=open("words.txt")
        f.close()
        return True
    except FileNotFoundError:
            return False



class WordManager:
    def __init__(self):
        self.words =[]
    def getWords(self):
        return self.words
    def loadFile(self):
        if not checkFileExists():
            print("Dictionary File does not exist!")
            print("Download it from: https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt")
            return False
        else:
            #exists
            print("Found Dictionary File! Reading!")
            with open("words.txt") as f:
                self.words = f.read().splitlines()
                return True