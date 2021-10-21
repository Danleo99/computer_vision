import numpy as np
import cv2 as cv
import math as math

x1 = 0
y1 = 0
x2 = 0
y2 = 0
bandRoi = False
vector1 = []

def roiImg(img):
    global x1,y1,x2,y2,bandRoi, vector1
    if (bandRoi == True):
        roiImage = img[y1:y2,x1:x2]
        showImage("roiImage",roiImage,1)

    
def mouseClick(event,x,y,flags,param):
    global x1,y1,x2,y2, bandRoi, vector1

    if(event == cv.EVENT_LBUTTONDOWN):
        x1 = x
        y1 = y
        

    if(event == cv.EVENT_LBUTTONUP):
        x2 = x
        y2 = y
        bandRoi = True
        vector1.append([x1,y1,x2,y2])
        diagonal(x1,y1,x2,y2)
        distancia(x1,x2)
        #print(vector1)


    return vector1

cv.namedWindow("Fusion de Imagen")
cv.setMouseCallback("Fusion de Imagen",mouseClick)


def loadImage(path,a):
    return cv.imread(path, a)

def showImage(nameWindow,img):
    cv.imshow(nameWindow,img)
    
    return 0

def destroyWindow():
    cv.destroyAllWindows()

def fusionar(img1,img2):
    fusion = cv.addWeighted(img1,0.6,img2,0.4,0)
    return fusion

def diagonal(x1, y1, x2, y2):
    hip = math.sqrt((x2-x1)**2+(y2-y1)**2)
    velocidad = hip/0.66
    print("La velocidad del auto azul es " + str(int(velocidad)) + " pixels/s")


def distancia(x1,x2):
    dis = x2 - x1
    print("La distancia total recorrida en el eje X es " + str(int(dis)) + " píxeles")
          
if __name__ == "__main__":
    while(True):
        fra1 = loadImage("Frame1.png",1)
        fra30 = loadImage("Frame2.png",1)
        fusion = fusionar(fra1,fra30)
        #showImage("Frame 1",fra1)
        #showImage("Frame 30",fra30)
        showImage("Fusion de Imagen",fusion)
        roiImg("Fusion de Imagen")
        cv.waitKey(0)
    destroyWindow()
