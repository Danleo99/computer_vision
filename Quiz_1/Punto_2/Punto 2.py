import cv2 as cv
import numpy as np

x1 = y1 = x2 = y2 = 0

def mouseClick(event,x,y,flags,param):
    global x1, y1, x2, y2

    if event == cv.EVENT_LBUTTONDOWN:
        x1 = x
        y1 = y

    if event == cv.EVENT_LBUTTONUP:
        x2 = x
        y2 = y

def showHistogram(imgGray):
    wbins = 256  #Como son imagenes de 8 bits
    hbins = 256
    #cv.calcHist(images, channels, mask, histSize, ranges)### La imagen siempre debe pasar en un canal
    histr = cv.calcHist([imgGray],[0],None,[hbins],[0,wbins])
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(histr)
    #Val cuantas veces se repite y Loc el pixeles que es
    imgHist = np.zeros([hbins, wbins], np.uint8) #Crear ventana negra
    for w in range(wbins):
        binVal = histr[w]
        intensity = binVal*(hbins-1)/max_val
        cv.line(imgHist, (w,hbins), (w,hbins-intensity),255)
    return imgHist,max_loc

def binaryThreshold(imgGrey,u1, u2):
    h,w = imgGrey.shape[:2]
    
    u = np.array([abs(u1),abs(u2)])
    u1 = np.amin(u)
    u2 = np.amax(u)
    
    #recorrer matriz de imagen
    for i in range(h):
        for j in range(w):
            #comparacion con umbral para conversion a blanco-negro
            if(imgGrey[i][j] <= u1 or imgGrey[i][j] >= u2):
                imgGrey[i][j] = 255
            else:
                imgGrey[i][j] = 0
    return imgGrey

if __name__ == '__main__':
    #Importamos las imagenes a color y en blanco y negro
    path = input('Ingrese la ubicacion de la imagen: ')
    img = cv.imread(path, 1)
    imgGr = cv.imread(path, 0)
    if img is None:
        print('No se encuentra la imagen')

    #Mostramos la imagen para poder sacar el ROI
    cv.namedWindow('XRay')
    cv.setMouseCallback('XRay', mouseClick)
    cv.imshow('XRay', img)
    cv.waitKey(0)

    #Realizamos el ROI y el Zoom a la imagen
    crop = img[x1:x2,y1:y2]
    cropGr = imgGr[x1:x2,y1:y2]
    zoom = cv.resize(crop, None, fx=10, fy=10,
                 interpolation=cv.INTER_LINEAR)
    zoomGr = cv.resize(cropGr, None, fx=10, fy=10,
                 interpolation=cv.INTER_LINEAR)
    cv.imshow('Zoom', zoom)

    #Hacemos el histograma de la region zoom
    imgHist, maxPos = showHistogram(cropGr)
    cv.imshow('Histograma', imgHist)

    #Binarizamos la region zoom
    imgBinary = binaryThreshold(zoomGr.copy(),maxPos[1] - 8, maxPos[1] + 8)
    cv.imshow('Binarizada', imgBinary)
    
    cv.waitKey(0)
    cv.destroyAllWindows()
