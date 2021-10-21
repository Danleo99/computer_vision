import cv2 as cv
import numpy as np


def nothing(x):
    pass
cv.namedWindow("imgGray")
cv.createTrackbar("u1","imgGray",0,255,nothing)
cv.createTrackbar("u2","imgGray",128,255,nothing)

def binaryThreshold(imgGray,u1,u2):
    h,w = imgGray.shape[:2]
    for i in range(h):
        for j in range(w):
            if (imgGray[i][j] >= u1) or (imgGray[i][j] < u2):
                imgGray[i][j] = 255
            else:
                imgGray[i][j] = 0
    return imgGray
            

def showImage(nameWindow,img,t):
    cv.imshow(nameWindow,img)
    cv.waitKey(t)
    return 0

def loadImage(path,a):
    return cv.imread(path, a)

def destroyWindow():
    cv.destroyAllWindows()

def pintar(img,color):
    img1 = img.copy()
    cv.imshow('aa',img1)
    h,w = img1.shape[:2]
    #Azul
    if (color == 0):
        for i in range(0,h):
            for j in range(0,w):
                if (img1[i,j] == 255):
                    img1[i,j] = 255
    return img1

def main(path):
    while(True):
        u1 = cv.getTrackbarPos("u1","imgGray")
        u2 = cv.getTrackbarPos("u2","imgGray")
        print(u1)
        img = loadImage(path,1)
        imgGray = loadImage(path, 0)
        imgBinary = binaryThreshold(imgGray.copy(),u1,u2)
        colorea=pintar(imgBinary,0)

        #showImage("imgColor",img,1)
        #showImage("img",img)
        showImage("imgGray",colorea,1)
    destroyWindow()
    


path ="gato.jpg"
main(path)
    
