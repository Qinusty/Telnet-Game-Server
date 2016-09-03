from Games.Game import Game
import random


class Mastermind(Game):
    def __init__(self):
        self.mode = ''
        self.number = []
        self.turns = 0
        self.correct = []
        self.digits = [str(x) for x in range(0,10)]
        self.name = 'mastermind'

    def handle(self, userID, data, queue):
        if "MODE" in data.upper():
            self.turns = 0
            self.correct = [False, False, False, False]
            self.number = self.generateNumber()
            self.mode = ''
            DataSplit = (data.upper()).split("MODE")
            for i in DataSplit:
                if "E" in i:
                    self.mode = 'e'
                    return ["EASY MODE selected... Number has been set.  Please make a guess."]
                elif "N" in i:
                    self.mode = 'n'
                    return ["NORMAL MODE selected... Number has been set.  Please make a guess."]
                elif "H" in i:
                    self.mode = 'h'
                    return ["HARD MODE selected... Number has been set.  Please make a guess."]
            if self.mode == '':
                self.mode = 'n'
                return ["No user specified mode has been dectected.  Defaulted to NORMAL MODE...  Number has been set.  Please make a guess."]
        elif "G" in data.upper():
            if len(self.number) != 4:
                return ["Guesses cannot be made before number assigned. Please select a MODE."]
            else:
                Guess = []
                for chara in data:
                    if chara == '0' or chara == '1' or chara == '2' or chara == '3' or chara == '4' or chara == '5' or chara == '6' or chara == '7' or chara == '8' or chara == '9':
                        Guess.append(chara)
                if len(Guess) != 4:
                    return ["Guess must be a four digit number.  Example: G 0201"]
                else:
                    self.turns += 1
                    return self.checkGuess(Guess)
        elif "HELP" in data.upper():
            return self.help()
        else:
            return ["Your input was not understood.  Please type 'help' for a list of commands."]


    def welcome(self):
        return "----Welcome to MASTERMIND!----"

    def help(self):
        return ["MODE [E/N/H]:  Reset the game and select a difficulty mode from easy, normal and hard\nExample; MODE E.", "G [Number]: Guess a four digit number.\nExample: G 2048", "\n* = Correct\n. = Wrong\nH = Actual number is higher than guess\nL = Actual number is lower than guess."]

    def generateNumber(self):
        return [random.choice(self.digits), random.choice(self.digits), random.choice(self.digits), random.choice(self.digits)]

    def checkGuess(self, Guess):
        Display = ''
        if Guess == self.number:
            return ["You have guessed the number!  It took you " + str(self.turns) + " turns!"]
        
        elif self.mode == 'e':
            Count = 0
            for i in Guess:
                if i == self.number[Count]:
                    Display = Display + '*'
                elif i > self.number[Count]:
                    Display = Display + 'L'
                else:
                    Display = Display + 'H'
                Count = Count + 1
            return [Display]
        
        else:
            if Guess[0] == self.number[0]:
                self.correct[0] = True
            if Guess[1] == self.number[1]:
                self.correct[1] = True
            if Guess[2] == self.number[2]:
                self.correct[2] = True
            if Guess[3] == self.number[3]:
                self.correct[3] = True
                
            Count = 0
            for i in self.correct:
                if i == True:
                    Display = Display + '*'
                elif self.mode == 'n':
                    Display = Display + '.'
            return [Display]
