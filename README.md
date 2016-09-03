## Telnet Game Server

### Group project by
- Josh
- Amy
- Matt
- Izzie

### About

This project was created over the course of 3 days as a group
programming project with minimal oversight. We had complete control 
over what to do the project on.

We chose to do a Telnet server with a variety of console based games
which are playable from any telnet client.

### How to

Ensure you are running python 3.4.3+
To check this use  `python -V`
```
git clone git@github.com:Qinusty/Telnet-Game-Server.git
cd Telnet-Game-Server/
python Server.py
```
By default the server will run at 127.0.0.1:21

To change the address to a public facing IP or change the port, edit
the Server.py file and find the assignment of the HOST and PORT variables.

```
HOST = '127.0.0.1'
PORT = 21
```

### Credit
- Server.py - Josh
- Games/
    - Game.py        - Josh
    - Battleships.py - Matt, Josh
    - Blackjack.py   - Amy, Josh
    - HigherLower.py - Izzie
    - Mastermind     - Izzie
    - TickTackToe    - Izzie


