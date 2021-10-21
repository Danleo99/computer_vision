#Importar librerías
import numpy as np
import cv2 as cv
def blankImage(h,w,sizew):
        blank = np.zeros((h, w, 3), np.uint8) 
        blank[:,0:w//3] = (255,0,0)
        blank[:,w//3:2*w//3] = (0,255,0)
        blank[:,2*w//3:w] = (0,0,255)
        return blank

h = int(input('Ingrese el alto de la imagen: '))
w = int(input('Ingrese el ancho de la imagen: '))
n = int(input('Ingrese el tamano del recuadro: '))

sizeh = h/n
sizew = w/n


image = blankImage(h, w,sizew)

cv.imshow('Imagen', image)
cv.waitKey(0)
cv.destroyAllWindows()