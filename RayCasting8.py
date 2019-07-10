import pygame
import math
#My first python project! by Nicholas Nord
#started on June 7, 2019

pygame.init()
clock = pygame.time.Clock()
obstacleList = []

# build display window
displayWidth = 800
displayHeight = 650

prevCenterX = 0
prevCenterY = 0
prevMouseX = 0
prevMouseY = 0
prevLOSX = 0
prevLOSY = 0

screen = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('RayCasting in Python')
background_color = (255,255,255)
black = pygame.Color(0,0,0)

# build player object   \Users\Nicho\.atom\My files
#playerImg = pygame.image.load('My files/PythonImages/ArmyPlayerTopViewFlipTrim.png')
playerImg = pygame.image.load('My files/PythonImages/PeaShooterResizeOpen.png')
obstacleImg = pygame.image.load('My files/PythonImages/Obstacle.png')
#playerImg = pygame.transform.scale(playerImg, (75, 75))
playerImg = pygame.transform.scale(playerImg, (31, 31))


def player(x,y):
    screen.blit(playerImg, (x,y))

# build class to hold obstacle coordinate
class Rectangle:
    def __init__(self, _x, _y, _width, _height):
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height

# build obstruction
def square_obstacle(obs_x, obs_y, obs_width, obs_height, _obstacleImg):
    #pygame.draw.rect(screen, (245,0,0), (obs_x - 1, obs_y - 1, obs_width + 2, obs_height + 2,))
    #pygame.draw.rect(screen, (245,245,220), (obs_x, obs_y, obs_width, obs_height))
    current = Rectangle(obs_x, obs_y, obs_width, obs_height)

    for box in obstacleList:
        if(box.x != obs_x and box.y != obs_y and box.height != obs_height and box.width != obs_height):
            obstacleList.append(current)
    if(len(obstacleList) == 0):
        obstacleList.append(current)

    #testing image instead of rectangles
    obstacleImgScaled = pygame.transform.scale(_obstacleImg, (obs_width, obs_height))
    screen.blit(obstacleImgScaled,(obs_x, obs_y))

# method to determine how many degrees to rotate player image
def findRotationDegrees(mouse_X, mouse_Y, center_X, center_Y):
    radians = math.atan2(mouse_Y - center_Y, mouse_X - center_X)
    degree = (radians * (180 / 3.1415) * -1) + 90
    return degree

# method to determine how many radians to rotate player image
def findRotationRadians(mouse_X, mouse_Y, center_X, center_Y):
    radians = math.atan2(mouse_Y - center_Y, mouse_X - center_X)
    return radians


# method to determine all points that make a circle in a 2d space.
# paramters are (x coord, y coord, radius, radiansRotated). returns array of points
def findCircle(x, y, radius, radiansRotated):
    radiansRotated = -radiansRotated + math.pi/2
    #rangeArr = [radiansRotated + math.pi/2 , radiansRotated, radiansRotated + (math.pi), radiansRotated -math.pi/2]
    rangeArr = [radiansRotated + math.pi/4, radiansRotated + math.pi/6,
    radiansRotated + math.pi/16, radiansRotated - math.pi/16,
     radiansRotated + math.pi/8, radiansRotated - math.pi/8,radiansRotated - math.pi/6, radiansRotated - (math.pi/4)]
    returnArr = []
    #for index in range(360):
    for index in rangeArr:
        return_X = y + (radius * math.cos(index))
        return_Y = x + (radius * math.sin(index))
        return_X = int(round(return_X))
        return_Y = int(round(return_Y))
        returnArr.append([return_X, return_Y])
    return returnArr


# method to draw the line of sight (change to include vision cone as well)
def drawLOS(mouse_X, mouse_Y, center_X, center_Y):
    global prevMouseX
    global prevMouseY
    global prevCenterX
    global prevCenterY
    global prevLOSX
    global prevLOSY

    if(mouse_X == prevMouseX and mouse_Y == prevMouseY and center_X == prevCenterX and center_Y == prevCenterY):
        pygame.draw.line(screen, black, (prevCenterX, prevCenterY), (prevLOSX, prevLOSY), 3)
        return

    lineThickness = 1

    prevMouseX = mouse_X
    prevMouseY = mouse_Y
    prevCenterX = center_X
    prevCenterY = center_Y
    noCollisionFound = True
    threshold = 11
    index = 0

    if mouse_X <= 0:
        mouse_X = 1
    if  mouse_Y <= 0:
        mouse_Y = 1

    if mouse_X == center_X:

        # code from here is a temporary fix. if slope is undefined or >25 or <25...
        if mouse_Y > center_Y:
            slope = -20
        else:
            slope = 20
        # to here. instead of multiplying slope and index, increment yCoord
        # until checkObstacleCollision/checkScreenCollision finds an edge

    slope = (center_Y - mouse_Y) / (center_X - mouse_X)

    if mouse_X > center_X:
        while noCollisionFound:
            yCoord = (slope * index) + center_Y
            if checkObstacleCollision(index + center_X, yCoord):
                pygame.draw.line(screen, black, (center_X, center_Y), (index + center_X, yCoord), lineThickness)
                #pygame.draw.line(screen, black, (center_X, center_Y), (x , y), 1)
                prevLOSX = index + center_X
                prevLOSY = yCoord
                noCollisionFound = False
            elif checkScreenCollision(index + center_X, yCoord):
                pygame.draw.line(screen, black, (center_X, center_Y), (index + center_X, yCoord), lineThickness)
                prevLOSX = index + center_X
                prevLOSY = yCoord
                noCollisionFound = False
            else :
                index = index + 1

    else:
        while noCollisionFound:
            yCoord = (-slope * index) + center_Y
            if checkObstacleCollision(center_X - index, yCoord):
                pygame.draw.line(screen, black, (center_X, center_Y), (center_X - index, yCoord), lineThickness)
                prevLOSX = center_X - index
                prevLOSY = yCoord
                noCollisionFound = False
            elif checkScreenCollision(center_X - index, yCoord):
                pygame.draw.line(screen, black, (center_X, center_Y), (center_X -index, yCoord), lineThickness)
                prevLOSX = center_X - index
                prevLOSY = yCoord
                noCollisionFound = False
            else :
                index = index + 1
            #end of test **

    #this draws the line from center to mouse
    #pygame.draw.line(screen, black, (center_X, center_Y), (mouse_X, mouse_Y), 1)
    #pygame.draw.line(screen, black, (center_X,center_Y), (playerImgRect.x, playerImgRect.y), 3)

#given a point, returns true if it is meets obstacle dimensions
def checkObstacleCollision(los_X, los_Y):
    for box in obstacleList:
        if(los_X >= box.x and los_X <= box.x + box.width):
            if(los_Y >= box.y and los_Y <= box.y + box.height):
                return True
    else:
        return False

#given a point, returns true if the point has exited the screen dimensions
def checkScreenCollision(los_X, los_Y):
    if(los_X <= 0 or los_X >= displayWidth):
        return True
    if(los_Y <= 0 or los_Y >= displayHeight):
        return True
    else :
        return False

#given a point (center of playerImg) and (int) d degree in radians, will create a circle around it and return a point along the
#circumference of the circle (45 degrees + d)
def drawConeLos(center_X, center_Y, circlePointList):
    for circleCoordPair in circlePointList:
        x = circleCoordPair[1]
        y = circleCoordPair[0]
        drawLOS(x, y, center_X, center_Y)
        #pygame.draw.line(screen, black, (center_X, center_Y), (x, y), 1)

# check and handle events while game is running
def game_loop():
    x = (displayWidth * .45)
    y = (displayHeight * .8)

    x_change = 0
    y_change = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_LEFT] or key[pygame.K_a]:
                    x_change = - 5
                if key[pygame.K_RIGHT] or key[pygame.K_d]:
                    x_change = + 5
                if key[pygame.K_UP] or key[pygame.K_w]:
                    y_change = - 5
                if key[pygame.K_DOWN] or key[pygame.K_s]:
                    y_change = + 5
                if key[pygame.K_ESCAPE]:
                    pygame.quit()
            if event.type == pygame.KEYUP:
                if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_a] or key[pygame.K_d]:
                    x_change = 0
                if key[pygame.K_UP] or key[pygame.K_DOWN] or key[pygame.K_s] or key[pygame.K_w]:
                    y_change = 0

        x += x_change
        y += y_change

        # define window boundaries
        if x >= displayWidth - playerImg.get_width() or x < 0:
            x -= x_change
        if y >= displayHeight - playerImg.get_height() or y < 0:
            y -= y_change

  # define interior of square_obstacle boundaries
        playerHeight = playerImg.get_height()
        playerWidth = playerImg.get_width()
        for box in obstacleList:
            if y < box.y + box.height and y + playerHeight > box.y:
                if x > box.x and x < box.x + box.width or x + playerWidth > box.x and x + playerWidth < box.x + box.width:
                    y -= y_change
                    x -= x_change

    # final adjustments
        screen.fill(background_color)
        square_obstacle(displayWidth//3,displayHeight//3,displayWidth//3, displayHeight//3, obstacleImg)
        # rotate playerImg s.t. player faces mouse position
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        centerX = x + (playerImg.get_width()/2)
        centerY = y + (playerImg.get_height()/2)

        degrees = findRotationDegrees(mouseX, mouseY, centerX, centerY)
        radians = findRotationRadians(mouseX, mouseY, centerX, centerY)
        drawLOS(mouseX, mouseY, centerX, centerY)
        circleArr = findCircle(centerX, centerY, 100, radians)
        drawConeLos(centerX, centerY, circleArr)
        playerImgRotated = pygame.transform.rotate(playerImg, degrees)
        screen.blit(playerImgRotated,(x,y))

        clock.tick(50)
        pygame.display.update()

game_loop()
pygame.quit()
