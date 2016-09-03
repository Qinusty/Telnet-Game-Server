from Games.Game import Game
from random import randint
class BattleshipGame(Game):

    def __init__(self):
        self.board = []
        self.size = 3
        self.shipCount = 2
        self.ships = []
        self.shots = 0
        self.generateBoard()
        self.sunken_ships = []
        self.name = 'battleships'

    def welcome(self):
        return "Welcome to the battleships," \
               " send help to get a list of commands"

    def help(self):
        return [  "start x y: starts a game with a grid size of <x> by <x> with <y> randomly placed ships",
                  "fire x y: fire followed by two integer arguments takes a shot at a location on the board"]


    def generateBoard(self):
        self.ships = []
        self.sunken_ships = []
        self.board = [["?" for _ in range(0,self.size)] for _ in range(0,self.size)]
        while len(self.ships) < self.shipCount:
            x = randint(0, self.size - 1)
            y = randint(0, self.size - 1)
            if (x, y) not in self.ships:
                self.ships.append((x,y))

    def formatBoard(self):
        xvals = [str(x) for x in range(0,self.size)]
        output = [" |" + " ".join(xvals), "-"*(self.size*2 + 2)]
        y = 0
        for row in self.board:
            output.append(str(y) + "|" + " ".join(row))
            y += 1
        return output

    def reset(self):
        self.generateBoard()
        self.shots = 0

    def handle(self, userID, data, queue):
        """
        Do everything in this function before super.handle()
        userID is the unique identifier for the user.
        data is the variable containing text sent by the client to the server.
        """
        if "help" in data.lower():
            return self.help()

        data = str(data).strip("\r\n").split(" ")
        if data[0].lower() == "start" and len(data) >= 3 \
            and data[1].isnumeric() and data[2].isnumeric():
            if int(data[2]) > int(data[1]) * int(data[1]):
                return ["There are too many ships for the defined grid size."]
            self.size = int(data[1])
            self.shipCount = int(data[2])
            self.generateBoard()
            retVal = ["Game Started!"]
            retVal.extend(self.formatBoard())
            return retVal
        elif data[0].lower() == "fire" and len(data) >= 3 and data[1].isnumeric() and data[2].isnumeric()\
                and int(data[1]) in range(0,self.size) and int(data[2]) in range(0,self.size):
            #print(self.ships) # CHEAT FOR ADMIN
            x = int(data[1])
            y = int(data[2])
            self.shots += 1
            if (x,y) in self.ships:
                self.board[y][x] = 'X'
                self.ships.remove((x,y))
                self.sunken_ships.append((x,y))
                retVal = ["HIT!"]
                retVal.extend(self.formatBoard())
                if len(self.ships) <= 0:
                    score = ((self.shipCount / self.shots) * 100) * ((self.size**2) /self.shipCount)
                    queue.put(('battleships', userID, '<', score))
                    retVal.extend(["You win!", "It took you {0} shots".format(self.shots), "A new game has started!"])
                    self.reset()
                    retVal.extend(self.formatBoard())
                return retVal
            else:
                if (x,y) not in self.sunken_ships:
                    self.board[y][x] = '-'
                    retVal = ["MISS!"]
                else:
                    retVal = ["You already sunk this ship!"]
                retVal.extend(self.formatBoard())
                return retVal

        else:
            retVal = ["Incorrect command, if you're trying to fire the correct format is", "fire <0-4> <0-4>"]
            retVal.extend(self.help())
            return retVal
        return ["Operation has no return..."]