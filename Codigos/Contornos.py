import cv2 as cv
import numpy as np

path = 'gato.jpg'
img_gray = cv.imread(path, 0)

#Hacer un blur = cv.medianBlur(copia de la imagen, kernel=#impar-cantidad de blur)
img_median = cv.medianBlur(img_gray.copy(), 9)

i=1 
m=3
n=3
k=np.ones((m,n),np.uint8)

## Funcion de binarizar ##

#Binarizado= cv.threshold(imagen en B&W,u1,u2,cv.THRESH_BINARY_INV)
ret_, img_binary = cv.threshold(img_gray,160,255,cv.THRESH_BINARY)

## Filtros morfologicos ##

img_dilate = cv.dilate(img_binary.copy(), kernel=k, iterations=i)
img_erode = cv.erode(img_binary.copy(), kernel=k, iterations=i)

## Contornos ##
contours, hierarchy = cv.findContours(img_binary.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
print(hierarchy)

h,w = img_gray.shape
img_contours = np.zeros((h,w,3), np.uint8)

for cnt in contours:
	cv.drawContours(img_contours, cnt, -1, (255,0,0), 2)
	cv.imshow('Contornos',img_contours)
	cv.waitKey(0)

cv.imshow('Original',img_gray)
cv.imshow("Binarizada", img_binary)
#cv.imshow("Blur", img_median)
#cv.imshow("Dilatada", img_dilate)
#cv.imshow("Contraer", img_erode)

#

cv.waitKey(0)
cv.destroyAllWindows()
