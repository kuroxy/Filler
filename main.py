import sys, os, math, time
import Filler
import getmap
import json
import socket


# fuctions
def get2dindex(i, amount):
    return (math.floor(i / amount), i % amount)
    # returns y then x


def playerinput(intypes): # types always in lowercase
    # print("Choises are : " + ", ".join(intypes))
    while True:
        inp = input().lower()
        if inp in intypes:
            return inp


def cls(attri=True):
    if attri:
        os.system("cls||clear")


def setbotinfo(game, depth, move,score,prediction,bottime):
    # info time gameturn depth botmove score prediction bottime
    info = {"time" : time.time(), "gameturn" : game.counter, "depth" : depth, "botcolor" : move, "score" : score, "prediction":prediction, "calctime" : bottime}
    info = json.dumps(info, separators=(',', ':'))
    # appending to file
    f = open("botinfo.json", "a")
    f.write(info + "\n")
    f.close()


def getbotinfo(attri=True):
    if attri:
        last_line = None
        with open("botinfo.json", 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]

        info = json.loads(last_line)
        print(f"Bot chose : {Filler.colorcode[info['botcolor']]} | Score : {info['score']}| prediction : in {info['depth']} steps eval is {info['prediction']} | calculation time : {info['calctime']}")


# first load map
# then ask type of game 1v1 1vbot botv1 botvbot (+ bot depth)

# GET MAP
print("LOAD MAP OPTIONS:")
print("1 - load manually")
print("2 - load with id")
print("3 - load image")
print("4 - load from server")

map = [[0 for _ in range(8)] for _ in range(7)]

loadinginp = input()

if loadinginp=="1":
    print("colors are : red:0 green:1 yellow:2 blue:3 magenta:4 grey:5")
    print("Type a long string per row. Like : \"12304205\"")
    for i in range(len(map)):
        temp = input()
        if len(temp) != len(map[0]):
            print("Unusable length, length should be 8")
            sys.exit()
        for j in range(len(temp)):
            map[i][j] = int(temp[j])


elif loadinginp=="2":
    print("Paste the map id.")
    mapid = input()
    if len(mapid) != len(map)*len(map[0]):
        print("Non valid mapid")
        time.sleep(2)
        sys.exit()
    for i in range(len(mapid)):
        i2d = get2dindex(i, len(map[0]))
        map[i2d[0]][i2d[1]] = mapid[i]
elif loadinginp=="3":
    print("Paste the full path to the img. Like \"C:\\Users\\user\\Desktop\\IMG.png\" if empty it uses img in uploads")
    path = input()
    if path:
        map = getmap.getmap(path)
    else:
        map = getmap.getmap('uploads/image.png')
elif loadinginp=="4":
    if os.path.isfile('uploads/image.png'):
        os.remove("uploads/image.png")
    print("Starting server on {0}:5000".format(socket.gethostbyname(socket.gethostname())))
    os.system('start getimg.py')
    print("Waiting for POST")
    while True:
        time.sleep(.5)
        if os.path.isfile('uploads/image.png'):
            print("File found")
            break
    map = getmap.getmap('uploads/image.png')
else:
    print("Not a load type")
    time.sleep(2)
    sys.exit()


for i in map:
    print(",".join(str(j) for j in i))

time.sleep(.5)
cls()
# MAP LOADED
# SETTINGS

#player1 is top right
#player2 is bottem left
player1 = None # human or bot
player2 = None # humab or bot
botinfo = False
clearscreen = False

print("What is player1 human or bot. h or b")
player1 = playerinput(["h","b"])
if player1=="b":
    print("What depth search. 0,1,2,etc..")
    depths = playerinput([str(i) for i in range(0,20)])
    player1+=depths

print("What is player2 human or bot. h or b")
player2 = playerinput(["h","b"])
if player2=="b":
    print("What depth search. 0,1,2,etc..")
    depths = playerinput([str(i) for i in range(0,20)])
    player2+=depths

if player1[0] == "b" or player2[0] == "b":
    print("Do you want bot info.y/n (y default)")
    botinf = playerinput(["y", "n", ""])
    if botinf == "y" or botinf == "":
        botinfo = True

print("Do you want Clear screen .y/n (n default)")
if playerinput(["y", "n", ""]) == "y":
    clearscreen = True

time.sleep(.5)
cls()


print(f"Player1 : {player1}")
print(f"Player2 : {player2}")
print(f"Bot info : {botinfo} ")
print(f"Clear screen : {clearscreen}")

time.sleep(.5)
cls()



# STARTING GAME

maingame = Filler.Filler(map)
isPlayer1Turn = False       # player 2 usually starts

setbotinfo(maingame, 4, 0, -5.578, 7, 0.1)


while True: # game
    time.sleep(.5)
    cls(clearscreen)
    getbotinfo(botinfo)
    maingame.printboard()

    if maingame.gameover(): # check if game is over
        break


    if isPlayer1Turn:
        if player1 == "h":
            print("Color options are")
            print(", ".join(f"{i} : {Filler.colorcode[i]}" for i in maingame.getmoves()))
            maingame.updateboard(Filler.playerinput(maingame.getmoves()), True)
        else:
            move,score,prediction,calctime = Filler.bestmove(maingame, int(player1[1:]), True)
            setbotinfo(maingame, int(player1[1:]), move, score, prediction, calctime)
            maingame.updateboard(move, True)
    else:
        if player2 == "h":
            print("Color options are")
            print(", ".join(f"{i} : {Filler.colorcode[i]}" for i in maingame.getmoves()))
            maingame.updateboard(Filler.playerinput(maingame.getmoves()), False)
        else:
            move,score,prediction,calctime = Filler.bestmove(maingame, int(player2[1:]), False)
            setbotinfo(maingame, int(player2[1:]), move, score, prediction, calctime)
            maingame.updateboard(move, False)

    isPlayer1Turn = not isPlayer1Turn   # next turn

print(f"Player 1 score : {len(maingame.player1tiles)}")
print(f"Player 2 score : {len(maingame.player2tiles)}")
