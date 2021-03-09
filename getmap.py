import sys
import math
from PIL import Image

# 0 : red | 1 : green   | 2 : yellow    | 3 : blue   | 4 : purple | 5 : black |


colorlist = [(192, 64, 77),(147,180,89),(212,191,72),(78,142,203),(84,63,129),(70, 70, 70)]

offset = [135,500]
offset4 = [135,535]
tilesize = [68,68]

def closestcolor(color):
    index = 0
    minDifference = math.inf
    for i in range(len(colorlist)):
        difference = abs(colorlist[i][0]- color[0]) + abs(colorlist[i][1]- color[1]) + abs(colorlist[i][2]- color[2])
        if difference < minDifference:
            minDifference = difference
            index = i
    #print(minDifference)
    return index

def getmap(filename):
    map = [[0 for _ in range(8)] for _ in range(7)]
    im = Image.open(filename)
    pix = im.load()
    for y in range(7):
        for x in range(8):
            if y==4:    # needed to let it work when waiting for other player text is on screen
                map[y][x] = closestcolor(pix[offset4[0]+x*tilesize[0],offset4[1]+y*tilesize[1]])
            else:
                map[y][x] = closestcolor(pix[offset[0]+x*tilesize[0],offset[1]+y*tilesize[1]])
    return map


if __name__ == "__main__":
    if len(sys.argv) == 2:
        themap = getmap(sys.argv[1])


        print(themap)
        print("---")

        mapidstring = "mapid : "
        for i in themap:   # prints the mapid
            for j in i:
                mapidstring+=str(j)
        print(mapidstring)

    else:
        print("Missing argument. Use : python loading.py [image name]")
