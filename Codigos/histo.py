#Importar Librerias
import numpy as np
import cv2 as cv

path = "pato.jpeg" 

def showImage(nameWindow,img,t):
    cv.imshow(nameWindow,img)
    cv.waitKey(t)
    return 0

def loadImage(path,a):
    return cv.imread(path,a)

def destroyWindow():
    cv.destroyAllWindows()

def showHistogram(imgGray):
    wbins = 256  #Como son imagenes de 8 bits
    hbins = 256
    #cv.calcHist(images, channels, mask, histSize, ranges)### La imagen siempre debe pasar en un canal
    histr = cv.calcHist([imgGray],[0],None,[hbins],[0,wbins])
    #print(histr)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(histr)
    #Val cuantas veces se repite y Loc el pixeles que es
    imgHist = np.zeros([hbins, wbins], np.uint8) #Crear ventana negra
    for w in range(wbins):
        binVal = histr[w]
        intensity = binVal*(hbins-1)/max_val
        cv.line(imgHist, (w,hbins), (w,hbins-intensity),255)
    return imgHist

     
if __name__ == "__main__":
    #iniciar programa
    img = loadImage(path,1)
    imgGray = loadImage(path,0)
    showImage("imgColor",img,1)
    imgHist = showHistogram(imgGray)
    showImage("imgHist", imgHist, 0)
    destroyWindow()
        
