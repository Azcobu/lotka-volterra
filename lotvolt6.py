#Lotka Volterra sim rewritten for more efficiency

# Idea and rules from NANIA
# Each site has three states, wolf, empty, sheep.
# Rules are as follows:
#
#   1. Pick a site (only stochastic updates allowed), and a neighbour
#   2. If wolf is adjacent to sheep, sheep gets eaten (becomes wolf with probability r). Else wolf dies with probability p
#   3. If sheep is adjacent to empty ground, reproduces with probability q
#   4. If empty ground is adjacent to anything, the thing moves into empty ground

# Differs from v.5 in that animals do not randomly wander, but instead seek prey or
# free space more directly, although randomness does factor into which they pick.
# Arguably this results in a less attractive sim and may (?) incur performance costs.
# Also tidied up fox vs wolf/sheep vs rabbit and their dictionary symbols.

# v.6 adding population plotting and a timeout to make the graph readable.

import random, pygame, cProfile
import matplotlib.pyplot as plt
from pygame.locals import *

#constants
worldheight = 60  #75
worldwidth = 100
cellsize = 7 #7 size of rectangle in display
WINSIZE = [worldwidth * cellsize, worldheight * cellsize + 20]
TEXTPOS = [5, worldheight * cellsize + 5]
wolfrep = 0.75 #0.75
wolfdie = 0.2  #0.1
sheeprep = 0.2 #0.2

DEBUG = 0
FRAMERATE = 100 #update throttle, higher number = less frequent updates

red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0
black = 0, 0, 0
grey = 110, 110, 110
white = 255, 255, 255

#objects map, consisting of a dict with key being a tuple giving coords, and val being animal type
objects = {}
pophist = [[], []]

pygame.init()
screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption('Lotka-Volterra Sim')
screen.fill(green)

#-------------------------------------------------------------------
#populate map - 0 is bare ground (there by default), 1 is a sheep, 4 is a wolf

for a in range(200):
	objects[(random.randint(0, worldheight - 1), random.randint(0, worldwidth - 1))] = 'S'

for a in range(100):
	objects[(random.randint(0, worldheight - 1), random.randint(0, worldwidth - 1))] = 'W'

#-------------------------------------------------------------------

def limitcoords(x, y):
    #make sure coordinates for the world map wrap properly
    if x >= worldheight: x = 0
    if y >= worldwidth: y = 0
    if x < 0: x = worldheight - 1
    if y < 0: y = worldwidth - 1
    return x, y

#-------------------------------------------------------------------

def findobject(sqx, sqy, objtype):
    #returns a list of squares containing the desired object type surrounding given coords
    #Note that this always scans all 8 neighbours - a better solution may be to randomly scan
    #until either all neighbour cells are scanned or a match is found.
    objlist = []
    newx = newy = 0

    for x in range(-1, 2):
        for y in range(-1, 2):
            newx, newy = limitcoords(sqx + x, sqy + y)
            if objtype != 'G':
                if (newx, newy) in objects and (newx, newy) != (sqx, sqy) and objects[(newx, newy)] == objtype:
                    objlist.append((newx, newy))
            else: #looking for grass, which doesn't appear in objects dict
                if (newx, newy) not in objects and (newx, newy) != (sqx, sqy):
                    objlist.append((newx, newy))
    return objlist

#------------------------------------------------------------------
def picksquares(): #pick square to process and update array and display

    if objects != {}:
        newobj = random.choice(list(objects.items()))
        sq1x = newobj[0][0]
        sq1y = newobj[0][1]

        square1 = objects[(sq1x, sq1y)]

        if square1 == 'W': #wolf
            #scan for sheep
            sheep = findobject(sq1x, sq1y, 'S')
            if sheep != []:
                nearsheep = random.choice(sheep)
                sq2x = nearsheep[0]
                sq2y = nearsheep[1]
                #wolf moves to square and eats sheep, may reproduce
                objects[(sq2x, sq2y)] = 'W'
                renderpartmap(sq2x, sq2y, 'W')
                if random.random() > wolfrep:
                    #did not reproduce
                    del objects[(sq1x, sq1y)]
                    renderpartmap(sq1x, sq1y, 'G')
            else:
                #no sheep found so die or move
                del objects[(sq1x, sq1y)]
                renderpartmap(sq1x, sq1y, 'G')
                if (random.random() > wolfdie):
                    #wolf didn't die so moves instead
                    freespace = findobject(sq1x, sq1y, 'G')
                    if freespace != []: #note if no free space, wolf dies after all
                        newpos = random.choice(freespace)
                        sq2x = newpos[0]
                        sq2y = newpos[1]

                        objects[(sq2x, sq2y)] = 'W'
                        renderpartmap(sq2x, sq2y, 'W')

        if square1 == 'S':
            #scan for grass
            grass = findobject(sq1x, sq1y, 'G')
            if grass != []:
                #sheep next to empty ground so breed or move
                neargrass = random.choice(grass)
                sq2x = neargrass[0]
                sq2y = neargrass[1]

                if (random.random() < sheeprep):
                    objects[(sq2x, sq2y)] = 'S'
                    renderpartmap(sq2x, sq2y, 'S')
                else:
                    #move instead
                    del objects[(sq1x, sq1y)]
                    renderpartmap(sq1x, sq1y, 'G')
                    objects[(sq2x, sq2y)] = 'S'
                    renderpartmap(sq2x, sq2y, 'S')
    else:
        #life has gone extinct
        extinction()

    return objects == {}
#------------------------------------------------------------------
def renderpartmap(x, y, celltype):
	#given two cell coords and a celltype, updates map)
    obj = pygame.Rect(y * cellsize, x * cellsize, cellsize, cellsize)
    if celltype == 'G':
        screen.fill(green, obj)
    elif celltype == 'S':
        screen.fill(blue, obj)
    else:
        screen.fill(red, obj)

#------------------------------------------------------------------

def renderfullmap(): #used for testing, can now be removed
    for a in range(worldwidth):
        for b in range(worldheight):
            obj = pygame.Rect(a * cellsize, b * cellsize, cellsize, cellsize)
            if (a, b) in objects:
                if objects[(a, b)] == 1:
                    screen.fill(blue, obj)
                else:
                    screen.fill(red, obj)
            else:
                screen.fill(green, obj)
    pygame.display.update()

#------------------------------------------------------------------
def census(tick): # take a census of sheep and wolves

    wolfcount = list(objects.values()).count('W')
    sheepcount = list(objects.values()).count('S')

    pophist[0].append(wolfcount)
    pophist[1].append(sheepcount)

    font = pygame.font.Font(None, 16)
    text = "Wolves:" + str(wolfcount) + "  Sheep:" + str(sheepcount) + "  Tick:" + str(tick) + '  '
    size = font.size(text)
    ren = font.render(text, 0, black, white)
    screen.blit(ren, TEXTPOS)

    return wolfcount > 0 and sheepcount > 0
#------------------------------------------------------------------
def extinction():
    font = pygame.font.Font(None, 16)
    text = 'Simulation ended with both species extinct.'
    size = font.size(text)
    ren = font.render(text, 0, black, white)
    screen.blit(ren, TEXTPOS)
    pygame.display.update()

def plot_pop():
    #find max pop
    #maxpop = max([x for x in pophist[1]])
    #xs = range(maxpop)
    plt.plot(pophist[0], label="Wolf")
    plt.plot(pophist[1], label="Sheep")
    plt.legend(loc='best')
    plt.tight_layout()
    plt.grid()
    plt.show()

#------------------------------------------------------------------
#main loop

def main():
    done = 0
    count = 0
    tick = 0
    renderfullmap()

    while picksquares() == False and done == False and tick < 5000:
    	if count == FRAMERATE:
            pygame.display.update()
            tick += 1
            if not census(tick):
                break
            count = 0
    	count += 1

    	for e in pygame.event.get():
    		if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
    			done = True
    			break
    extinction()
    pygame.quit()
    plot_pop()

main()
#cProfile.run("main()")