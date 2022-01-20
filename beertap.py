#!/usP/bin/python3

##
#
# Prerequisites:
# A Touchscreen properly installed on your system:
# - a device to output to it, e.g. /dev/fb1
# - a device to get input from it, e.g. /dev/input/touchscreen
# Side by Side Image display - touchscreen enabled
# Updated for Adafruit PITFT
##

import pygame, time, evdev, select, math, os

# Very important: the exact pixel size of the TFT screen must be known so we can build graphics at this exact format
width = 480
height = 320
SurfaceSize = (480, 320)
DEFAULT_IMAGE_SIZE = (240, 320)
pic1Dim = (0, 240)
pic2Dim = (241, 480)
plotdone = False;


# Note that we don't instantiate any display!
pygame.init()

# The pygame surface we are going to draw onto. 
# /!\ It must be the exact same size of the target display /!\
lcd = pygame.Surface(SurfaceSize)

# This is the important bit
def refresh():
    # We open the TFT screen's framebuffer as a binary file. Note that we will write bytes into it, hence the "wb" operator
    f = open("/dev/fb1","wb")
    # According to the TFT screen specs, it supports only 16bits pixels depth
    # Pygame surfaces use 24bits pixels depth by default, but the surface itself provides a very handy method to convert it.
    # once converted, we write the full byte buffer of the pygame surface into the TFT screen framebuffer like we would in a plain file:
    f.write(lcd.convert(16,0).get_buffer())
    # We can then close our access to the framebuffer
    f.close()
    time.sleep(0.1)

# Now we've got a function that can get the bytes from a pygame surface to the TFT framebuffer, 
# we can use the usual pygame primitives to draw on our surface before calling the refresh function.

# Here we just blink the screen background in a few colors with the "Hello World!" text
pygame.font.init()
defaultFont = pygame.font.SysFont(None,30)
beerIdx1 = 0
beerIdx2 = 0
beerList1 = []
beerList2 = []
currIdx1 = 0
currIdx2 = 0

def loadImages():
   # Look in beer1 and beer2 directories
   global beerList1, beerList2
   global beerIdx1, beerIdx2

   beerpath1 = '/home/pi/beertap/images/beer1'
   beerpath2 = '/home/pi/beertap/images/beer2'
   for image_path1 in os.listdir(beerpath1):
      input_path1 = os.path.join(beerpath1, image_path1)
      print("Images beer1 {0}".format(input_path1))
      beerList1.append(pygame.image.load(input_path1))
      beerIdx1 += 1
   for image_path2 in os.listdir(beerpath2):
      input_path2 = os.path.join(beerpath2, image_path2)
      print("Image beer2 {0}".format(input_path2))
      beerList2.append(pygame.image.load(input_path2))
      beerIdx2 += 1
 
loadImages()

#beerImg1 = pygame.image.load('./images/beer1.png')
#beerImg1.convert()
beerImg = pygame.transform.scale(beerList1[0], DEFAULT_IMAGE_SIZE)
imgPos1 = beerImg.get_rect(topleft = (0, 0))
lcd.blit(beerImg, imgPos1)
#beerImg1 = pygame.image.load('./images/beer2.png')
#beerImg2.convert()
beerImg = pygame.transform.scale(beerList2[0], DEFAULT_IMAGE_SIZE)
imgPos2 = beerImg.get_rect(topleft = (240, 0))
lcd.blit(beerImg, imgPos2)
refresh()

##
# Everything that follows is for handling the touchscreen touch events via evdev
##

# Used to map touch event from the screen hardware to the pygame surface pixels. 
# (Those values have been found empirically, but I'm working on a simple interactive calibration tool
# 
tftOrig = (3750, 180)
tftEnd = (150, 3750)
tftDelta = (tftEnd [0] - tftOrig [0], tftEnd [1] - tftOrig [1])
tftAbsDelta = (abs(tftEnd [0] - tftOrig [0]), abs(tftEnd [1] - tftOrig [1]))

# We use evdev to read events from our touchscreen
# (The device must exist and be properly installed for this to work)
#touch = evdev.InputDevice('/dev/input/touchscreen')
touch = evdev.InputDevice('/dev/input/event0')

# We make sure the events from the touchscreen will be handled only by this program
# (so the mouse pointer won't move on X when we touch the TFT screen)
touch.grab()
# Prints some info on how evdev sees our input device
#print(touch)
# Even more info for curious people
#print(touch.capabilities())

# Here we convert the evdev "hardware" touch coordinates into pygame surface pixel coordinates
def getPixelsFromCoordinates(coords):
    # TODO check divide by 0!
    #Screen seems to be X axis up down and Y Right Left so invert
    # Very Hacky for chealp 3.5" screen!
#    x = int( 480 - ((coords[1] -350) / (4000-350) * 480))
#    y = int( (coords[0] -300) / (3900-300) * 320) 
    # Very Hacky for chealp 3.5" screen!
    x = int( (coords[1] -350) / (4000-350) * 480)
    y = int( (coords[0] -300) / (3900-300) * 320) 

#    print("X Value: {0}".format(x))
#    print("Y Value: {0}".format(y))
  

#    if tftDelta [0] < 0:
#        x = float(tftAbsDelta [0] - coords [0] + tftEnd [0]) / float(tftAbsDelta [0]) * float(SurfaceSize [0])
#    else:    
#        x = float(coords [0] - tftOrig [0]) / float(tftAbsDelta [0]) * float(surfaceSize [0])
#    if tftDelta [1] < 0:
#        y = float(tftAbsDelta [1] - coords [1] + tftEnd [1]) / float(tftAbsDelta [1]) * float(SurfaceSize [1])
#    else:        
#        y = float(coords [1] - tftOrig [1]) / float(tftAbsDelta [1]) * float(SurfaceSize [1])
    return (int(x), int(y))

# Was useful to see what pieces I would need from the evdev events
#def printEvent(event):
#    print(evdev.categorize(event))
#    print("Value: {0}".format(event.value))
#    print("Type: {0}".format(event.type))
#    print("Code: {0}".format(event.code))

def cyclePics(coords):
    # check x value
    global currIdx1, currIdx2
    global beerList1, beerList2
    global beerIdx1, beerIdx2

    if coords[0] >= pic1Dim[0] and coords[0] <= pic1Dim[1]:
#       print("Pic 1") 
       if coords[1] <= 160:
          # assume down
          if currIdx1 == 0:
             currIdx1 = beerIdx1-1 
          else:
             currIdx1 -= 1 
       else:
         #assume up
         if currIdx1 == (beerIdx1-1):
            currIdx1 = 0
         else:
            currIdx1 += 1
       beerImg1 = pygame.transform.scale(beerList1[currIdx1], DEFAULT_IMAGE_SIZE)
       imgPos1 = beerImg1.get_rect(topleft = (0, 0))
       lcd.blit(beerImg1, imgPos1)
#       print("IDX 2 = {0}".format(currIdx2))
    elif coords[0] >= pic2Dim[0] and coords[0] <= pic2Dim[1]:
#       print("Pic 2") 
       if coords[1] <= 160:
          # assume down
          if currIdx2 == 0:
             currIdx2 = beerIdx2-1 
          else:
             currIdx2 -= 1 
       else:
         #assume up
         if currIdx2 == (beerIdx2-1):
            currIdx2 = 0
         else:
            currIdx2 += 1
#       print("IDX 2 = {0}".format(currIdx2))

       beerImg2 = pygame.transform.scale(beerList2[currIdx2], DEFAULT_IMAGE_SIZE)
       imgPos2 = beerImg2.get_rect(topleft = (240, 0))
       lcd.blit(beerImg2, imgPos2)
    else:
       print("Out of Bounds") 
    refresh()
    res = 1;
    return (int(res))


# This loop allows us to write red dots on the screen where we touch it 
while True:
    # TODO get the right ecodes instead of int
    r,w,x = select.select([touch], [], [])
    for event in touch.read():
#        printEvent(event)
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == 0:
                X = event.value
#                print("X:{0}".format(X))
            elif event.code == 1:
                Y = event.value
#                print("Y:{0}".format(Y))
            elif event.code == 24:
                PRESSURE = event.value
#                print("PRESSURE:{0}".format(PRESSURE))
        elif event.type == evdev.ecodes.EV_KEY:
#            print("KEY:{0}".format(type))
            if event.code == 330 and event.value == 0:
#                printEvent(event)
                p = getPixelsFromCoordinates((X, Y))
#                print("TFT: {0}:{1} | Pixels: {2}:{3}".format(X, Y, p [0], p [1]))
#                pygame.draw.circle(lcd, (255, 0, 0), p , 2, 2)
                res = cyclePics(p)
                refresh()
                plotdone = True;
#        elif event.type == evdev.ecodes.EV_SYN:
#                print("SYN {0}".format(event.type))
#                p = getPixelsFromCoordinates((X, Y))
#                print("TFT: {0}:{1} | Pixels: {2}:{3}".format(X, Y, p [0], p [1]))
#                pygame.draw.circle(lcd, (255, 0, 0), p , 2, 2)
#                refresh()
#                plotdone = True;
        elif plotdone == True:
                plotdone = False;
                break 
        else:
           refresh()
#                print("type not found {0}".format(event.type))

exit()
