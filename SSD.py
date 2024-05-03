import math
import pygame
import matplotlib as mpl
import random

from Vector2D import myVector
from Arrow import draw_arrow

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

WHITE = (255,255,255)
BLACK = (0,0,0)

MIDDLE = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

norm = mpl.colors.Normalize(200,18000)
cmap = mpl.colormaps['jet']
def generateSSD(other: myVector,alt: int, count: int):

    """ Generate 3-D SSD given altitude and another aircraft's position and saves to png

    Args:
        other (myVector): The position of the other aircraft
        altitude (integer): The altitude the controlled aircraft is at in feet. 
    
    """
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # pygame.display.set_caption("SSD for {aircraft1}")


    SCREEN.fill(WHITE)

    #other = myVector(3*SCREEN_WIDTH/4, 250)
    otherVel = myVector(-55,10)

    myVel = myVector(-20, -65)

    altRound = norm(int(math.ceil(alt/500.0) * 500))

    altColor = mpl.colors.to_rgb(cmap(altRound))

    realCol = tuple([255*altColor[0], 255*altColor[1], 255*altColor[2]])

    point0 = myVector(*MIDDLE) + otherVel
    relVec = other - point0
    opp = myVector(-relVec.y/relVec.x,1).toLength(35)
    point1 = other + opp
    point2 = other - opp

    pygame.draw.polygon(SCREEN,(150,150,150), [point0.toTuple(), point1.toTuple(), point2.toTuple()])

    pygame.draw.circle(SCREEN, BLACK, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2),50,2)
    pygame.draw.circle(SCREEN, BLACK, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 75,2)
    pygame.draw.circle(SCREEN, realCol, MIDDLE, 10)
    pygame.draw.circle(SCREEN, (255,0,0), other.toTuple(),10)
    draw_arrow(SCREEN, pygame.Vector2(other.toTuple()), pygame.Vector2((other + otherVel).toTuple()), BLACK, head_width=6,head_height=4)
    draw_arrow(SCREEN, pygame.Vector2(MIDDLE), pygame.Vector2((myVector(*MIDDLE) + myVel).toTuple()), BLACK, head_width=6,head_height=4)

    pygame.image.save(SCREEN, f"./imgs/SSD{count}.jpeg")

    pygame.display.flip()

    pygame.quit()

    count += 1
    return count

altitudes = random.sample(range(200, 18000, 100), 100)

f = open("altitues.txt", 'w')
count = 1

for alt in altitudes:
    otherX = random.uniform(10, SCREEN_WIDTH - 10)
    otherY = random.uniform(10, SCREEN_HEIGHT - 10)

    other = myVector(otherX, otherY)

    count = generateSSD(other, alt, count)
    f.write(f"{alt}\n")

f.close()

