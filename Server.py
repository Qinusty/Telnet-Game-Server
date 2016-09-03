import socket
import threading, queue
import json
from Games.Blackjack import Blackjack
from Games.Mastermind import Mastermind
from Games.Battleships import BattleshipGame
from Games.TickTackToe import TickTackToe
from Games.HigherLower import HigherLower


class HighscoreThread(threading.Thread):
    def __init__(self, shared):
        threading.Thread.__init__(self)
        self.queue = shared

    def run(self):
        while True:
            if not self.queue.empty():
                game, name, order, score = self.queue.get()
                name = name.lower()
                path = 'Highscores/{0}.json'.format(game)
                try:
                    file = open(path, 'rb')
                except FileNotFoundError:
                    file = open(path, 'w')
                    file.write('{}')
                    file.close()
                    file = open(path, 'rb')
                try:
                    json_data = file.read().decode('utf-8')
                    data = json.loads(json_data)
                    file.close()
                except EOFError:
                    data = {}
                    file.close()
                #data = dict(data)
                if name in data.keys():
                    if ((order == '>' and data[name] > score) or (order == '<' and data[name] < score)):
                        data[name] = score
                else:
                    data[name] = score

                with open(path, 'w') as file:
                    write_data = json.dumps(data)
                    file.write(write_data)



class ConnectionThread(threading.Thread):
    def __init__(self, threadID, conn, addr, newscores):
        threading.Thread.__init__(self)
        self.game = None
        self.games = ['Blackjack', 'Mastermind', 'Battleships', 'Ticktacktoe', 'HigherOrLower']
        self.ID = threadID
        self.connection = conn
        self.address = addr
        self.userID = ""
        self.queue = newscores

    def selectGame(self):
        gameChoice = self.sendMsg("Pick a game (" +
                                  ", ".join(self.games) +
                                  ")", waitResponse=True).strip("\r\n")
        self.sendMsg('High score supported games are battleships and HigherOrLower')
        self.sendMsg("HighScores can be accessed via sending the 'highscore' command once a game is selected")
        if gameChoice.lower() == "blackjack":
            self.game = Blackjack()
        elif gameChoice.lower() == "mastermind":
            self.game = Mastermind()
        elif gameChoice.lower() == "battleships":
            self.game = BattleshipGame()
        elif gameChoice.lower() == "ticktacktoe":
            self.game = TickTackToe()
        elif gameChoice.lower() == "higherorlower":
            self.game = HigherLower()
        else:
            self.sendMsg("That isn't one of our games...")

    def run(self):
        disconnected = False
        while not disconnected:
            try:
                if not self.userID:
                    self.sendMsg('Welcome to our Game Server!')
                    self.userID = self.sendMsg("Name: ", waitResponse=True).strip("\r\n")
                    print("Given name", self.userID)
                    while not self.game:
                        self.selectGame()
                    self.sendMsg("#"*10)
                    self.sendMsg(self.game.welcome())
                    [self.sendMsg(x) for x in self.game.help()]
                data = self.connection.recv(1024).decode('utf-8', 'strict')
                # print(data) # debug
                if 'highscore' in data.lower():
                    response = self.highScoreFormat(self.game)
                elif 'back' in data.lower():
                    self.sendMsg('-')
                    self.sendMsg('-')
                    self.selectGame()
                    self.sendMsg('*' * 5)
                    response = ['GAME CHANGED', '*'*5, '-', '-', self.game.welcome()]
                    response.extend(self.game.help())
                else:
                    response = self.game.handle(self.userID, data, self.queue)
                for line in response:
                    self.sendMsg(line)
            except BrokenPipeError:
                print("Client {0} disconnected".format(self.userID))
                disconnected = True

    def highScoreFormat(self, game):

        tmp = ['HIGHSCORES | {0}'.format(game.name.upper())]
        length = len(tmp[0])
        tmp.append('-'*length)
        retVal = ['-'*length]
        retVal.extend(tmp)
        if game.name in ['battleships', 'higherorlower']:
            pass
        else:
            return ['Sorry this game does not yet have high score capability.']
        with open('Highscores/{0}.json'.format(game.name), 'r') as file:
            json_data = json.loads(file.read())
            highscores = []
            for key, val in json_data.items():
                highscores.append((key,val))
            if game.name == 'battleships' or game.name == 'higherorlower':
                reversed = True
            else:
                reversed = False
            highscores.sort(key=lambda tup: tup[1], reverse=reversed)
            for score in highscores:
                string = score[0] + ": " + str(score[1])
                retVal.append(string)
        retVal.append('-'*length)
        return retVal


    def sendMsg(self, message, waitResponse=False):
        #print(message) #debug
        self.connection.send(str(message + "\r\n").encode('utf-8', 'strict'))
        if waitResponse:
            response = ""
            try:
                response = self.connection.recv(1024).decode('utf-8', 'strict')
            except:
                print("Something went wrong!")
            return response
        else:
            return None


## server code

HOST = '127.0.0.1'
PORT = 21
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
print("Port bound, Listening at {0}:{1}".format(HOST,PORT))
sock.listen(5)
threads = []
idCounter = 0
highscore_queue = queue.Queue()
highscore_thread = HighscoreThread(highscore_queue)
highscore_thread.start()
while 1:
    conn, addr = sock.accept()
    thread = ConnectionThread(idCounter, conn, addr, highscore_queue)
    threads.append(thread)
    threads[idCounter].start()
    idCounter += 1
    print("Connection from", addr)
    print("Given ThreadID", idCounter - 1)



sock.close()
