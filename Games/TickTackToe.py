from Games.Game import Game
import random

class TickTackToe(Game):
    def __init__(self):
        self.gameover = True
        self.player = None
        self.square = [' ', '|', ' ', '|', ' ', '\n', '-+-+-', '\n', ' ', '|', ' ', '|', ' ', '\n', '-+-+-', '\n', ' ', '|',
                   ' ', '|', ' ', '\n']
        self.msg_playerturn = "---Player's Turn---"
        self.msg_compturn = "--Computer's Turn--"
        self.msg_compwin = "***Computer Wins!***"
        self.msg_playerwin = "****Player Wins!****\nType NEW to start a new game."
        self.name = 'ticktacktoe'

    def handle(self, UserID, data, queue):
        if "NEW" in data.upper():
            self.gameover = False
            self.player = random.choice([True, False])
            self.square = [' ', '|', ' ', '|', ' ', '\n', '-+-+-', '\n', ' ', '|', ' ', '|', ' ', '\n', '-+-+-', '\n',
                           ' ', '|', ' ', '|', ' ', '\n']
            display = ['-------NEW GAME STARTED-------']
            if self.player == False:    #Ensure that COMPUTER takes turn if self.player is False before returning square.
                display.append(self.msg_compturn)
                display.append(self.makeSquare(self.square))
                location = self.changeSquare(False, None)
                self.square[location] = 'O'
            display.append(self.msg_playerturn)
            display.append(self.makeSquare(self.square))

            return display

        elif "PLAY" in data.upper() and self.gameover == False:
            Axis = []
            data = str(data).split(" ")
            Axis.append(data[1])
            Axis.append(data[2])
            if len(Axis) != 2:
                return["Could not recognise coordinates.  Please try again or type 'HELP' for more instructions."]
            else:
                display = []
                location = self.changeSquare(True, Axis)
                if location == None:
                    return ["This is not a valid coordinate.  Please enter the coordinates of a blank slot."]
                else:
                    self.square[location] = 'X'
                    self.gameover = self.checkWin('X')
                    if self.gameover == True:
                        display.append(self.msg_playerwin)
                        display.append(self.makeSquare(self.square))
                    else:
                        display.append(self.msg_compturn)
                        display.append(self.makeSquare(self.square))
                        location = self.changeSquare(False, None)
                        self.square[location] = 'O'
                        self.gameover = self.checkWin('O')
                        if self.gameover == True:
                            display.append(self.msg_compwin)
                            display.append(self.makeSquare(self.square))
                        else:
                            display.append(self.msg_playerturn)
                            display.append(self.makeSquare(self.square))
                    return display

        elif "HELP" in data.upper():
            return self.help()

        else:
            return ["Your input was not understood.  Please type 'help' for a list of commands."]

    def welcome(self):
        return "--Welcome to Tick Tack Toe!--"

    def help(self):
        return ["NEW: Start a new game.", "PLAY [X,Y]: Place a cross in an area of the table, using X and Y axis to reference them.  Example; PLAY 1,2", "HELP: Display these instructions."]


    def makeSquare(self, Square):
        String = ''
        for item in self.square:
            String = String + item
        return String


    def changeSquare(self, Player, axis):
        if Player == False:
            axis = self.compAI()

        Location = -10
        for i in range(int(axis[0])):
            Location += 2
        for i in range(int(axis[1])):
            Location += 8

        if self.square[Location] != ' ':
            return None
        else:
            return Location


    def compAI(self):
        Square_Formatted = []
        for item in self.square:
            if item == 'X' or item == 'O' or item == ' ':
                Square_Formatted.append(item)

        #Check if self is about to win;
        if self.Check([Square_Formatted[0], Square_Formatted[1], Square_Formatted[2]], 'O') == True:
            if Square_Formatted[0] == ' ':
                return ['1', '1']
            elif Square_Formatted[1] == ' ':
                return ['2', '1']
            elif Square_Formatted[2] == ' ':
                return ['3', '1']
        if self.Check([Square_Formatted[3], Square_Formatted[4], Square_Formatted[5]], 'O') == True:
            if Square_Formatted[3] == ' ':
                return ['1', '2']
            elif Square_Formatted[4] == ' ':
                return ['2', '2']
            elif Square_Formatted[5] == ' ':
                return ['3', '2']
        if self.Check([Square_Formatted[6], Square_Formatted[7], Square_Formatted[8]], 'O') == True:
            if Square_Formatted[6] == ' ':
                return ['1', '3']
            elif Square_Formatted[7] == ' ':
                return ['2', '3']
            elif Square_Formatted[8] == ' ':
                return ['3', '3']
        if self.Check([Square_Formatted[0], Square_Formatted[4], Square_Formatted[8]], 'O') == True:
            if Square_Formatted[0] == ' ':
                return ['1', '1']
            elif Square_Formatted[4] == ' ':
                return ['2', '2']
            elif Square_Formatted[8] == ' ':
                return ['3', '3']
        if self.Check([Square_Formatted[2], Square_Formatted[4], Square_Formatted[6]], 'O') == True:
            if Square_Formatted[2] == ' ':
                return ['3', '1']
            elif Square_Formatted[4] == ' ':
                return ['2', '2']
            elif Square_Formatted[6] == ' ':
                return ['1', '3']
        if self.Check([Square_Formatted[0], Square_Formatted[3], Square_Formatted[6]], 'O') == True:
            if Square_Formatted[0] == ' ':
                return ['1', '1']
            elif Square_Formatted[3] == ' ':
                return ['1', '2']
            elif Square_Formatted[6] == ' ':
                return ['1', '3']
        if self.Check([Square_Formatted[1], Square_Formatted[4], Square_Formatted[7]], 'O') == True:
            if Square_Formatted[1] == ' ':
                return ['2', '1']
            elif Square_Formatted[4] == ' ':
                return ['2', '2']
            elif Square_Formatted[7] == ' ':
                return ['2', '3']
        if self.Check([Square_Formatted[2], Square_Formatted[5], Square_Formatted[8]], 'O') == True:
            if Square_Formatted[2] == ' ':
                return ['3', '1']
            elif Square_Formatted[5] == ' ':
                return ['3', '2']
            elif Square_Formatted[8] == ' ':
                return ['3', '3']

        # Check if user is about to win;
        if self.Check([Square_Formatted[0], Square_Formatted[1], Square_Formatted[2]], 'X') == True:
            if Square_Formatted[0] == ' ':
                return ['1', '1']
            elif Square_Formatted[1] == ' ':
                return ['2', '1']
            elif Square_Formatted[2] == ' ':
                return ['3', '1']
        if self.Check([Square_Formatted[3], Square_Formatted[4], Square_Formatted[5]], 'X') == True:
            if Square_Formatted[3] == ' ':
                return ['1', '2']
            elif Square_Formatted[4] == ' ':
                return ['2', '2']
            elif Square_Formatted[5] == ' ':
                return ['3', '2']
        if self.Check([Square_Formatted[6], Square_Formatted[7], Square_Formatted[8]], 'X') == True:
            if Square_Formatted[6] == ' ':
                return ['1', '3']
            elif Square_Formatted[7] == ' ':
                return ['2', '3']
            elif Square_Formatted[8] == ' ':
                return ['3', '3']
        if self.Check([Square_Formatted[0], Square_Formatted[4], Square_Formatted[8]], 'X') == True:
            if Square_Formatted[0] == ' ':
                return ['1', '1']
            elif Square_Formatted[4] == ' ':
                return ['2', '2']
            elif Square_Formatted[8] == ' ':
                return ['3', '3']
        if self.Check([Square_Formatted[2], Square_Formatted[4], Square_Formatted[6]], 'X') == True:
            if Square_Formatted[2] == ' ':
                return ['3', '1']
            elif Square_Formatted[4] == ' ':
                return ['2', '2']
            elif Square_Formatted[6] == ' ':
                return ['1', '3']
        if self.Check([Square_Formatted[0], Square_Formatted[3], Square_Formatted[6]], 'X') == True:
            if Square_Formatted[0] == ' ':
                return ['1', '1']
            elif Square_Formatted[3] == ' ':
                return ['1', '2']
            elif Square_Formatted[6] == ' ':
                return ['1', '3']
        if self.Check([Square_Formatted[1], Square_Formatted[4], Square_Formatted[7]], 'X') == True:
            if Square_Formatted[1] == ' ':
                return ['2', '1']
            elif Square_Formatted[4] == ' ':
                return ['2', '2']
            elif Square_Formatted[7] == ' ':
                return ['2', '3']
        if self.Check([Square_Formatted[2], Square_Formatted[5], Square_Formatted[8]], 'X') == True:
            if Square_Formatted[2] == ' ':
                return ['3', '1']
            elif Square_Formatted[5] == ' ':
                return ['3', '2']
            elif Square_Formatted[8] == ' ':
                return ['3', '3']

        else:
            valid = False
            while valid == False:
                axis = [random.randint(1,3), random.randint(1,3)]

                Location = -10
                for i in range(axis[0]):
                    Location = Location + 2
                for i in range(axis[1]):
                    Location = Location + 8

                if self.square[Location] == ' ':
                    valid = True

            return axis


    def Check(self, Square_Formatted, Lookup):      #Checks for number of two
        Count = 0
        for item in Square_Formatted:
            if item == Lookup:
                Count += 1
        if Count == 2:
            return True
        else:
            return False

    def Check3(self, Square_Formatted, Lookup):     #Checks for number of three
        Count = 0
        for item in Square_Formatted:
            if item == Lookup:
                Count += 1
        if Count == 3:
            return True
        else:
            return False

    def checkWin(self, Player):
        Square_Formatted = []
        for item in self.square:
            if item == 'X' or item == 'O' or item == ' ':
                Square_Formatted.append(item)

        if self.Check3([Square_Formatted[0], Square_Formatted[1], Square_Formatted[2]], Player) == True:
            return True
        elif self.Check3([Square_Formatted[3], Square_Formatted[4], Square_Formatted[5]], Player) == True:
            return True
        elif self.Check3([Square_Formatted[6], Square_Formatted[7], Square_Formatted[8]], Player) == True:
            return True
        elif self.Check3([Square_Formatted[0], Square_Formatted[4], Square_Formatted[8]], Player) == True:
            return True
        elif self.Check3([Square_Formatted[2], Square_Formatted[4], Square_Formatted[6]], Player) == True:
            return True
        elif self.Check3([Square_Formatted[0], Square_Formatted[3], Square_Formatted[6]], Player) == True:
            return True
        elif self.Check3([Square_Formatted[1], Square_Formatted[4], Square_Formatted[7]], Player) == True:
            return True
        elif self.Check3([Square_Formatted[2], Square_Formatted[5], Square_Formatted[8]], Player) == True:
            return True
        else:
            return False

