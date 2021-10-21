import cv2 as cv
import numpy as np

#Binarizar una imagen
def binary(imgGray,u):
    h,w =imgGray.shape[:2]
    for i in range(0,h) :
        for j in range (0,w) :
            if (imgGray[i][j] >= u):
                imgGray[i][j] = 255
            else:
                imgGray[i][j] = 0
    return imgGray

#Funcion Pasar
def nothing(x):
	pass

cv.namedWindow("imgColor")
cv.createTrackbar("u1","imgColor",0,255,nothing)
cv.createTrackbar("u2","imgColor",0,255,nothing)
path1 = "22.jpg"


while (True):
	u1 = cv.getTrackbarPos("u1","imgColor")
	u2 = cv.getTrackbarPos("u2","imgColor")
	print(u1)
	print(u2)	
	img1 = cv.imread(path1,1)
	imgGray = cv.imread(path1,0)
	cv.imshow("imgColor",img1)
	#cv.imshow("imgGray",imgGray)
	dife= binary(imgGray.copy(),220)
	#cv.imshow("Diferencia",dife)  
	#cv.waitKey(0) 
cv.destroyAllWindows()