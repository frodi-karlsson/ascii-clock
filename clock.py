import os, msvcrt, time, sys, math, datetime, numpy as np
from typing import Dict
from scipy.ndimage import rotate

clear = lambda: os.system('cls')
RED = "\u001b[31m"
GREEN = "\u001b[32m"
BLUE = "\u001b[34m"
WHITE = "\u001b[37m"
RESET = "\u001b[0m"

def getHour(time):
    hour = int(time.split(":")[0])
    if hour > 12:
        hour = hour - 12
    return hour
def getMinutes(time):
    minute = int(time.split(":")[1])
    return minute
def getSeconds(time):
    return int(time.split(":")[2])
def calculateSecondHandAngle(second):
    return 6 * second
def calculateMinuteHandAngle(minute, second):
    minuteAngle = 6 * minute + 0.1 * second
    return minuteAngle
def calculateHourHandAngle(hour, minute):
    hourAngle = 30 * hour + 0.5 * minute
    return hourAngle

def isInRange(coordsa, coordsb, threshold):
    x1, y1 = coordsa
    x2, y2 = coordsb
    return abs(x1 - x2) <= threshold and abs(y1 - y2) <= threshold

def isOnEdgeOfCircle(x, y, radius, threshold):
    return abs(math.sqrt(math.pow(x - radius, 2) + math.pow(y - radius, 2)) - radius) <= threshold

def isInCircle(x, y, r):
    return math.sqrt(math.pow(x - r, 2) + math.pow(y - r, 2)) <= r

def getAngle(x, y, r):
    quadrant = -1
    cX = r
    cY = r
    dX = x - cX
    dY = y - cY
    theta = math.atan2(dY, dX)
    theta = math.degrees(theta) + 90
    theta = (theta + 360) % 360
    return theta

def modEqTh(i, mod, eq, threshold):
    return abs(i % mod - eq) <= threshold

def numberMatrix(r, th = 2, diff = 4):
    radius = r - int(diff/2)
    circle = np.zeros((radius * 2 + 1, radius * 2 + 1))
    circle = circle.astype(str)
    for y in range(radius * 2 + 1):
        for x in range(radius * 2 + 1):
            angle = getAngle(x, y, radius)
            diffs = {
                "12": modEqTh(angle, 360, 0, th),
                "01": modEqTh(angle, 360, 30, th),
                "02": modEqTh(angle, 360, 60, th),
                "03": modEqTh(angle, 360, 90, th),
                "04": modEqTh(angle, 360, 120, th),
                "05": modEqTh(angle, 360, 150, th),
                "06": modEqTh(angle, 360, 180, th),
                "07": modEqTh(angle, 360, 210, th),
                "08": modEqTh(angle, 360, 240, th),
                "09": modEqTh(angle, 360, 270, th),
                "10": modEqTh(angle, 360, 300, th),
                "11": modEqTh(angle, 360, 330, th),
            }
            if any(diffs.values()) and isOnEdgeOfCircle(x, y, radius, 0.5):
                for key, value in diffs.items():
                    if value:
                        circle[y, x] = key
                        break
            else:
                circle[y, x] = "  "
    return circle

def caseMatrix(radius):
    circle = np.zeros((radius * 2 + 1, radius * 2 + 1))
    circle = circle.astype(str)
    for y in range(radius * 2 + 1):
        for x in range(radius * 2 + 1):
            if isOnEdgeOfCircle(x, y, radius, 0.2):
                circle[y, x] = "* "
            elif isInCircle(x, y, radius):
                circle[y, x] = ". "
            else:
                circle[y, x] = "  "
    return circle

def convertAngleToTop(angle):
    return (angle - 90 + 360) % 360

def addMatrixInsideMatrix(matrix1, matrix2, padding = 2):
    matrix1 = matrix1.tolist()
    matrix2 = matrix2.tolist()
    for y in range(len(matrix2)):
        for x in range(len(matrix2[y])):
            if matrix2[y][x] != "  " and y + padding < len(matrix1) and x + padding < len(matrix1[y]):
                matrix1[y + padding][x + padding] = matrix2[y][x]
    return np.array(matrix1)

def lineAtAngle(r, length, angle):
    angle = convertAngleToTop(angle)
    x = r
    y = r
    line = []
    for i in range(length):
        line.append((x, y))
        x += math.cos(math.radians(angle)) 
        y += math.sin(math.radians(angle))
    return line

def convertLineToMatrix(line, r, threshold = 0.6):
    matrix = np.zeros((r * 2 + 1, r * 2 + 1))
    matrix = matrix.astype(str)
    for y in range(r * 2 + 1):
        for x in range(r * 2 + 1):
            for coords in line:
                if isInRange(coords, (x, y), threshold):
                    x2, y2 = coords
                    angle = getAngle(x2, y2, r)
                    if angle >= 337.5 and angle <= 360 or (angle >= 0 and angle <= 22.5) or (angle >=157.5 and angle <= 202.5):
                        matrix[y, x] = "| "
                    elif angle >=22.5 and angle <= 67.5 or (angle >=202.5 and angle <= 247.5):
                        matrix[y, x] = "/ "
                    elif angle >=67.5 and angle <= 112.5 or (angle >=247.5 and angle <= 292.5):
                        matrix[y, x] = "- "
                    elif angle >=112.5 and angle <= 157.5 or (angle >=292.5 and angle <= 337.5):
                        matrix[y, x] = "\\ "
                    break
                else:
                    matrix[y, x] = "  "
    return matrix

def timed_input(timeout, timer=time.monotonic):
    sys.stdout.flush()
    endtime = timer() + timeout
    while timer() < endtime:
        if msvcrt.kbhit():
            return msvcrt.getwch()
    return ""

def makeAllPartsMatrix(r):
    now = datetime.datetime.now()
    currentHour, currentMinute, currentSecond = now.hour, now.minute, now.second
    hourHandAngle = calculateHourHandAngle(currentHour, currentMinute)
    minuteHandAngle = calculateMinuteHandAngle(currentMinute, currentSecond)
    secondHandAngle = calculateSecondHandAngle(currentSecond)
    case = caseMatrix(r)
    numbers = numberMatrix(r)
    hourHand = convertLineToMatrix(lineAtAngle(r, int(2*(r/4)), hourHandAngle), r)
    minuteHand = convertLineToMatrix(lineAtAngle(r, int(3*(r/4)), minuteHandAngle), r)
    secondHand = convertLineToMatrix(lineAtAngle(r, r, secondHandAngle), r)
    return case, numbers, hourHand, minuteHand, secondHand

def makeClockMatrix(r):
    case, numbers, hourHand, minuteHand, secondHand = makeAllPartsMatrix(r)
    matrix = caseMatrix(r)
    matrix = addMatrixInsideMatrix(matrix, numbers)
    matrix = addMatrixInsideMatrix(matrix, secondHand, 0)
    matrix = addMatrixInsideMatrix(matrix, minuteHand, 0)
    matrix = addMatrixInsideMatrix(matrix, hourHand, 0)
    return matrix

def constructBackMatrix(caseMatrix):
    backMatrix = caseMatrix
    centerY, centerX = backMatrix.shape[0]//2, backMatrix.shape[1]//2
    backMatrix[centerY, centerX] = "o "
    return backMatrix

def constructSideMatrix(caseMatrix):
    sideMatrix = caseMatrix
    for z in range(sideMatrix.shape[0]):
        for y in range(sideMatrix.shape[1]):
            if sideMatrix[z, y] == "* ":
                sideMatrix[z, y] = "_ "
    return sideMatrix

def convertMatrixTo3d(matrixNp):
    ySize, xSize = matrixNp.shape
    zSize = max(ySize, xSize)
    matrix3d = np.zeros((xSize, ySize, zSize))
    matrix3d = matrix3d.astype(str)
    centerZ = int(zSize/2)
    for z in range(ySize):
        for y in range(xSize):
            for x in range(zSize):
                matrix3d[z, y, x] = "  "
    for y in range(ySize):
        for x in range(xSize):
            matrix3d[centerZ, y, x] = matrixNp[y, x]
    return matrix3d

def construct3dClock(r):
    case = caseMatrix(r)
    backMatrix = constructBackMatrix(case)
    sideMatrix = constructSideMatrix(case)
    clock2d = makeClockMatrix(r)
    clock3d = convertMatrixTo3d(clock2d)
    centerZ = int(clock3d.shape[0]/2)
    clock3d[centerZ + 1] = sideMatrix
    clock3d[centerZ + 2] = backMatrix
    return clock3d

def convertNp3dStrToInt(np3d):
    for z in range(np3d.shape[0]):
        for y in range(np3d.shape[1]):
            for x in range(np3d.shape[2]):
                letters = list(np3d[z, y, x])
                if len(letters) > 1:
                    for i in range(len(letters)):
                        letters[i] = ord(letters[i])
                    np3d[z, y, x] = int("00".join(map(str, letters)))
                else:
                    np3d[z, y, x] = ord(letters[0])
    np3d = np3d.astype(int)
    return np3d

def convertNp3dIntToStr(np3d):
    newNp3d = np.zeros((np3d.shape[0], np3d.shape[1], np3d.shape[2]))
    newNp3d = newNp3d.astype(str)
    for z in range(np3d.shape[0]):
        for y in range(np3d.shape[1]):
            for x in range(np3d.shape[2]):
                if np3d[z, y, x] == 0:
                    np3d[z, y, x] = 320032
    for z in range(np3d.shape[0]):
        for y in range(np3d.shape[1]):
            for x in range(np3d.shape[2]):
                letters = str(np3d[z, y, x]).split("00")
                newNp3d[z, y, x] = chr(int(letters[0])) + chr(int(letters[1]))
    return newNp3d
    

def rotate3dMatrix(matrix3d, angle, ax = 2):
    matrix3d = convertNp3dStrToInt(matrix3d)
    matrix3d = rotate(matrix3d, angle, axes=(0, ax), reshape=False, order=0)
    usedNumbers = []
    matrix3d = convertNp3dIntToStr(matrix3d)
    for z in range(matrix3d.shape[0]):
        for y in range(matrix3d.shape[1]):
                for x in range(matrix3d.shape[2]):
                    if any(char.isdigit() for char in matrix3d[z, y, x]):
                        if int(matrix3d[z, y, x]) not in usedNumbers:
                            usedNumbers.append(int(matrix3d[z, y, x]))
                        else:
                            matrix3d[z, y, x] = ". "
    return matrix3d

def project3dMatrix(matrix3d):
    matrix2d = np.zeros((matrix3d.shape[0], matrix3d.shape[2]))
    matrix2d = matrix2d.astype(str)
    for x in range(matrix3d.shape[2]):
        for y in range(matrix3d.shape[1]):
            val = "  "
            for z in range(matrix3d.shape[0]):
                if matrix3d[z, y, x] != "  ":
                    val = matrix3d[z, y, x]
                    break
            matrix2d[y, x] = val
    return matrix2d

def printNp2d(matrix):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] != "\n":
                print(matrix[y][x], end="")
        print()

def printNp3d(matrix):
    for z in range(len(matrix)):
        for y in range(len(matrix[z])):
            for x in range(len(matrix[z][y])):
                if matrix[z][y][x] != "\n":
                    print(matrix[z][y][x], end="")
            print()
        print("- "*len(matrix[z][0]))        

def runSpinAnimation():
    r = 14
    clock3d = construct3dClock(r)
    clock2d = project3dMatrix(clock3d)
    viewClock = clock3d
    stop = False
    angleY = 0
    lastTime = datetime.datetime.now().strftime("%H:%M:%S")
    while not stop:
        clock3d = construct3dClock(r)
        input = timed_input(0.5)
        if input == "q":
            stop = True
        elif input == "d":
            angleY += 10
        elif input == "a":
            angleY -= 10
        if angleY%360 != 0:
            viewClock = rotate3dMatrix(clock3d, angleY)
        clock2d = project3dMatrix(viewClock)
        clear()
        printNp2d(clock2d)
        print(lastTime)
        lastTime = datetime.datetime.now().strftime("%H:%M:%S")

runSpinAnimation()