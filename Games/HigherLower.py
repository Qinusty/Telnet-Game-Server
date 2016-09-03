from Games.Game import Game
import random


class HigherLower(Game):
    def __init__(self):     #Define variables to act as global.
        self.mode = None
        self.lastnum = 0
        self.nextnum = 0
        self.score = 0
        self.name = 'higherorlower'
        self.msg_HighorLow = "Will the next number be higher or lower?"

    def handle(self, userID, data, queue):     #Get user input in this format from server.  Returns must be in list format.
        display = []
        if "MODE" in data.upper():  #User wants to specify mode.
                #Assign mode;
            if "1" in data:
                self.mode = 1
                display.append("Mode set to Easy...  Generating number.")
            elif "2" in data:
                self.mode = 2
                display.append("Mode set to Medium...  Generating number.")
            elif "3" in data:
                self.mode = 3
                display.append("Mode set to Challenging...  Generating number.")
            elif "4" in data:
                self.mode = 4
                display.append("Mode set to Hard...  Generating number.")
            elif "5" in data:
                self.mode = 5
                display.append("Mode set to Insane...  Generating number.")
            else:   #Defaults to medium mode if user does not follow conventional assignment.
                self.mode = 2
                display.append("Mode not recognised.  Defaulted to Medium...")
            #Resets score and assigns new number from generateNumber function.
            self.score = 0
            self.nextnum = self.generateNumber()
            display.append("Number: " + str(self.nextnum))
            display.append(self.msg_HighorLow)
            return display

        elif "H" in data.upper() and self.mode != None:     #User guesses that number will be higher.
            #Generate next number;
            self.lastnum = self.nextnum
            self.nextnum = self.generateNumber()

            if self.checkGuess() == True:   #If number is higher, increase score by mode and output win message.
                self.score += self.mode
                display.append("You guessed correct!")
                display.append("Number: " + str(self.nextnum))
                display.append(self.msg_HighorLow)
                return display
            elif self.checkGuess() == False:    #If number is lower, remove mode assignment to prevent further guessing and display score.
                self.mode = None
                display.append("You guessed wrong!")
                queue.put(('higherorlower', userID, '<', self.score))
                display.append("Number: " + str(self.nextnum))
                display.append("Score: " + str(self.score))
                display.append("Select a mode to start a new game.")
                return display

        elif "L" in data.upper() and self.mode != None:     #User guesses that number will be lower.
            self.lastnum = self.nextnum
            self.nextnum = self.generateNumber()

            if self.checkGuess() == False:  #If number is lower, increase score by mode and output win message.
                self.score += self.mode
                display.append("You guessed correct!")
                display.append("Number: " + str(self.nextnum))
                display.append(self.msg_HighorLow)
                return display

            elif self.checkGuess() == True: #If number is higher, remove mode assignment and display score.
                self.mode = None
                queue.put(('higherorlower', userID, '<', self.score))
                display.append("You guessed wrong!")
                display.append("Number: " + str(self.nextnum))
                display.append("Score: " + str(self.score))
                display.append("Select a mode to start a new game.")
                return display

        elif "HELP" in data.upper():    #User asks for help; display commands
            return self.help()

        elif self.mode == None:         #User is trying to input before starting game.
            return ["Select a mode to start the game."]



        else:       #User inputs something not recognises as a command.
            return ["Your input was not understood.  Please type 'help' for a list of commands."]





    def welcome(self):
        return "--Welcome to Higher Or Lower!--"

    def help(self):
        return ["MODE [1/2/3/4/5]: Start a new game with varying difficulty.\n  1: Easy: 1-100\n  2: Medium: 1-50\n  3: Challenging: 1-25\n  4: Hard: 1-10\n  5: Insane: 1-2\n", "H: Guess higher", "L: Guess lower", "HELP: Display these instructions"]

    def generateNumber(self):   #Generates a random number based on the difficulty mode;
        if self.mode == 1:
            return random.randint(1,100)
        elif self.mode == 2:
            return random.randint(1,50)
        elif self.mode == 3:
            return random.randint(1,25)
        elif self.mode == 4:
            return random.randint(1,10)
        else:
            return random.randint(1,2)

    def checkGuess(self):       #Returns True if number is higher or the same, False if lower.
        if self.nextnum >= self.lastnum:
            return True
        if self.nextnum < self.lastnum:
            return False