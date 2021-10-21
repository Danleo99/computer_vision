import cv2 as cv
import numpy as np

def difImagen(img1,img2):
    resta = cv.subtract(img1,img2)
    h,w =resta.shape[:2]
    for i in range(0,h) :
        for j in range (0,w) :
            if (resta[i][j] >= 50):
                resta[i][j] = 255
            else:
                resta[i][j] = 0
    return resta

def posCount(imag):
    h,w =imag.shape[:2]
    colum= int (w/3)
    fil=int (h/4)
    conta = 0
    for i in range(0,4):
        for j in range(0,3):
            wht = cv.countNonZero(imag[i*fil:(i+1)*fil,j*colum:(j+1)*colum])
            if (wht > 2000):
                conta = conta + 1
                print ("Falta una pastilla en la posicion "+str(j+1) +","+ str(i+1))
    
    print("Faltan ",conta," pastillas")

path1 = "21.jpg"
path2 = "22.2.jpg"
if __name__ == "__main__":
    img1 = cv.imread(path1,1)
    img2 = cv.imread(path2,0)
    imgGray = cv.imread(path1,0)
    cv.imshow("imColor",img1)
    dife= difImagen(imgGray,img2)
    cv.imshow("Diferencia",dife)
    posCount(dife)

cv.waitKey(0)
cv.destroyAllWindows()