#_Laboratorio 2 por Daniel Felipe León Gualdrón y Juan Esteban Acevedo Sánchez_
#____________Librerias________________#
import cv2 as cv
import numpy as np
import time

#____________Variables________________#
path = "Billar.mp4"
# Contadores #
en = 1
a1 = 0
a2 = 0
a3 = 0
a4 = 0
a5 = 0
a6 = 0
b8 = 0

#____________Funciones________________#

def procImagen(imagen, y1, y2, x1, x2, t,n, inf, sup, hab):

    global en, a1, a2, a3, a4, a5, a6, b8, en1, en2, en3, en4, en5, en6

    en = hab

    ## ROI ##
    im = imagen[y1:y2,x1:x2]

    ## Binarizacion Bimodal ##
    gray = cv.cvtColor (im, cv.COLOR_BGR2GRAY)
    ret1, frame_binary1 = cv.threshold(gray, inf, 255, cv.THRESH_BINARY)
    ret2, frame_binary2 = cv.threshold(gray, sup, 255, cv.THRESH_BINARY)
    imgn = cv.absdiff(frame_binary1,frame_binary2)
    
    im = cv.resize(imgn, (160,160))
    
    ## Deteccion de contornos ##
    contours, hierarchy = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    img = np.zeros((160,160,3), np.uint8)

    ## Cambio de los habilitadores ##
    if (len(contours)<= n):
        if (t == "agujero1"):
            en1 = 1
            
        if (t == "agujero2"):
            en2 = 1
            
        if (t == "agujero3"):
            en3 = 1
            
        if (t == "agujero4"):
            en4 = 1
            
        if (t == "agujero5"):
            en5 = 1
            
        if (t == "agujero6"):
            en6 = 1
            
    for cnt in contours:
        x, y, wc, hc = cv.boundingRect(cnt)
        area = wc*hc

        
        if (wc/hc == 2.4642857142857144 ):
            print ("EL JUEGO HA TERMINADO")
            print(wc/hc,"La bola 8 entro por el ", t)
            #cv.destroyAllWindows()
            en = 0
            b8 = 1
        
        if (wc/hc >= 0.908 and wc/hc < 1.169 and en == 1 and wc/hc != 1.0810810810810811 and b8 == 0):
            if (wc/hc == 1 and hc/wc == 1):
                en = 0
            else:
                if (t == "agujero1"):
                    en1 = 0
                    a1 = a1+1
                    print("Entró una bola por el ", t)
                    

                if (t == "agujero2"):
                    en2 = 0
                    a2 = a2+1
                    print("Entró una bola por el ", t)
                    

                if (t == "agujero3"):
                    en3 = 0
                    a3 = a3+1
                    print("Entró una bola por el ", t)
                    

                if (t == "agujero4"):
                    en4 = 0
                    a4 = a4+1
                    print("Entró una bola por el ", t)
                    

                if (t == "agujero5"):
                    en5 = 0
                    a5 = a5+1
                    print("Entró una bola por el ", t)
                    

                if (t == "agujero6"):
                    en6 = 0
                    a6 = a6+1
                    print("Entró una bola por el ", t)
                    

                
        cv.drawContours(img, cnt, -1, (255,0,0), 2)

    return hab,img
    
##_________Función principal_________ ##
if __name__ == "__main__":

    ## Importamos el video ##
    capture = cv.VideoCapture(path)
    #time.sleep(1)

    ## Iniciamos los habilitadores ##
    en1 = 1
    en2 = 1
    en3 = 1
    en4 = 1
    en5 = 1
    en6 = 1
    
    ## Reconocimiento de bolas ##
    while (capture.isOpened()):
        ret, frame = capture.read()
        if (ret == False):
            break

        cv.imshow("frame",frame)

        ## Deteccion por aspect ratio ##
        #agujero# = procImagen (imagen,(ubicacion Y,X), Identificador,(Umbrales), contador)
        agujero2 = procImagen (frame,2,28,311,343, "agujero2",2, 150, 240, en2)
        agujero1 = procImagen (frame,10,35,15,35, "agujero1",0,135,240, en1)
        agujero3 = procImagen (frame,10,35,620,640, "agujero3",0,110,240, en3)
        
        agujero5 = procImagen (frame,308,339,311,343, "agujero5",2,135,240, en5)
        agujero6 = procImagen (frame,300,321,615,636, "agujero6",1,120,240, en6)
        agujero4 = procImagen (frame,300,326,15,41, "agujero4",0,120,240, en4)
        
        cv.waitKey(1)

    ## Imprimimos los contadores ##
    print ("Por el agujero 1 entraron ", a1,"bolas")
    print ("Por el agujero 2 entraron ", a2,"bolas")
    print ("Por el agujero 3 entraron ", a3,"bolas")
    print ("Por el agujero 4 entraron ", a4,"bolas")
    print ("Por el agujero 5 entraron ", a5,"bolas")
    print ("Por el agujero 6 entraron ", a6,"bolas")

    capture.release()
    cv.destroyAllWindows()
