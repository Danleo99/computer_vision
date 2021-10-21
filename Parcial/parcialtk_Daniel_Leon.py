#Librerias
import cv2 as cv
import numpy as np
import time
from tkinter import *
from tkinter import filedialog, ttk
import tkinter as tk
from PIL import Image
from PIL import ImageTk

#Variables de forma, ruta, y captura
path = ""
capture = None

#Contadores de la linea izquierda
bigPc = 0
smallPc = 0
plastica = 0
#Contadores de la linea central
sBox = 0
mBox = 0
lBox = 0
#Contadores de la linea derecha
azul = 0
verde = 0
gris = 0
conta1 = 0
conta2 = 0
conta3= 0

#Flags de las bandas, conteo y color
conteo1 = True
color = True
conteo = True

#Funciones para la interfaz gráfica, organizador grid, organizador de texto, organizador de wTab
def organ(label,columna,fila,espaciox,espacioy):
    label.grid(column = columna, row = fila, padx = espaciox, pady = espacioy)

def swText(texto1, variable, texto2):
    textfin = str(texto1 +str(variable)+ texto2)
    return textfin

def wTab(marco,texto):
    etq = Label(marco, text = texto)
    return etq

#Función para cargar vídeo
def loadVideo():
    global capture, path

    if capture is not None:
        videoViewer.image = ""
        capture.release()
        capture = None
    path = filedialog.askopenfilename(filetypes = [("video", ".mp4")])

    #Función para que comience cuando la ruta sea distinta a vacía
    if len(path) > 0:
        capture = cv.VideoCapture(path)
        lblpath = wTab(my_frame1,"Ruta: " + path)
        lblpath2 = wTab(my_frame2,"Ruta: " + path)
        lblpath3 = wTab(my_frame3,"Ruta: " + path)
        lblpath.grid(column = 0, row = 7, padx = 10, pady = 10, columnspan = 4)
        lblpath2.grid(column = 0, row = 7, padx = 10, pady = 10, columnspan = 4)
        lblpath3.grid(column = 0, row = 7, padx = 10, pady = 10, columnspan = 4)

def medicion1():
    global  plastica, capture, conteo1,smallPc, bigPc
    if capture is not None:
        ret, frame = capture.read()
        if (ret == True):
            frame_gray = cv.cvtColor (frame, cv.COLOR_BGR2GRAY)
            frame1 = cv.resize(frame[100:550,45:180],(200,600))
            h, w = frame_gray.shape

            ## Proceso de la izquierda ##

            ret2, frame_binaryini = cv.threshold(frame_gray, 180, 255, cv.THRESH_BINARY)
            roi1 = frame_binaryini[259:420,52:174]
            h1, w1 = roi1.shape
            img_contours1 = np.zeros((h1,w1,3), np.uint8)
            contours1, hierarchy1 = cv.findContours(roi1.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
            atotal1 = 0

            for cnt1 in contours1:
                x, y, wc1, hc1 = cv.boundingRect(cnt1)
                area1 = wc1*hc1
                atotal1 = atotal1 + area1

                if (area1>750):
                    cv.drawContours(img_contours1, cnt1, -1, (255,0,0), 2)

            #Defino un valor para el área sobre la cual comenzar a contar
            if (atotal1 < 750):
                conteo1 = True

            #Defino un lugar para contar
            if (atotal1 > 750 and (img_contours1[1][10][0] != 0)):

                for cnt1 in contours1:
                    x, y, wc1, hc1 = cv.boundingRect(cnt1)
                        
                    area1 = wc1*hc1
                    #Área para plasticBox
                    if (area1 > 9000 and conteo1 == True):
                        conteo1 = False
                        plastica = plastica + 1
                        #Funciones de texto
                        plastic = swText("Han pasado ", plastica, " Plastic Box")
                        #Funciones para las label
                        lbplastic = wTab(my_frame1, plastic)
                        #Funciones organizadoras
                        organ(lbplastic, 5, 1, 0, 0)

                    #Área para Big Pallet
                    if (area1>=2100 and area1<7000 and conteo1 == True):
                        conteo1 = False
                        bigPc = bigPc + 1
                        #Funciones de texto
                        bigP = swText("Han pasado ", bigPc, " Big Pallet")
                        #Funciones para las label
                        lbigp = wTab(my_frame1, bigP)
                        #Funciones organizadoras
                        organ(lbigp, 5, 2, 0, 0)

                    #Área para Small Pallet
                    if (area1>750 and area1<1900 and conteo1 == True):
                        conteo1 = False
                        smallPc = smallPc + 1
                        #Funciones de texto
                        smallP = swText("Han pasado ", smallPc, " Small Pallet")
                        #Funciones para las label
                        lsmallp = wTab(my_frame1, smallP)
                        #Funciones organizadoras
                        organ(lsmallp, 5, 3, 0, 0)

            videoc = Image.fromarray(frame1)
            framemov = ImageTk.PhotoImage(image = videoc)
            videoViewer1.configure(image = framemov)
            videoViewer1.image = framemov
            videoViewer1.after(1, medicion1)
        else:
            capture.release()
            capture = None
            capture = cv.VideoCapture(path)
                
def medicion2():
    global  sBox, mBox, lBox, capture, conteo
    if capture is not None:
        ret, frame = capture.read()
        if (ret == True):
            frame_gray = cv.cvtColor (frame, cv.COLOR_BGR2GRAY)
            h, w = frame_gray.shape
            frame2 = cv.resize(frame[100:550,200:340],(200,600))
            ## Estudio banda central ##

            #Binarizacion bimodal 
            ret3, frame_binary_2 = cv.threshold(frame_gray, 230, 255, cv.THRESH_BINARY)
            ret4, frame_binary_3 = cv.threshold(frame_gray, 180, 255, cv.THRESH_BINARY)
            Img_binary = cv.absdiff(frame_binary_2, frame_binary_3)
            ret5, frame_binary_4 = cv.threshold(Img_binary, 200, 255, cv.THRESH_BINARY)

            #Defino un ROI para la zona a analizar
            roi2 = frame_binary_4[130:218, 202:320]
            h2, w2 = roi2.shape
            
            #Creo una imagen para los contornos
            img_contours2 = np.zeros((h2, w2, 3), np.uint8)
            contours2, hierarchy2 = cv.findContours(roi2.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
            area_place = 0
                
            for cnt in contours2:
                x, y, wc, hc = cv.boundingRect(cnt)
                area = wc*hc
                #Defino área_place en función del área para que no me la referencie antes de asignar
                area_place = area_place + area

                if (area > 1000):
                    cv.drawContours(
                        img_contours2, cnt, -1, (255, 0, 0), 2)
                    pass
                
            #Conteo cuando el área sea mayor a 100
            if (area_place < 1000):
                conteo = True
                    
            #Defino las posibles zonas en la que va a pasar las cajas
            if (area_place > 1000 and (img_contours2[1][10][0] != 0 or img_contours2[1][60][0] != 0 or img_contours2[1][115][0] != 0)):
                for cnt in contours2:
                    x, y, wc, hc = cv.boundingRect(cnt)
                    area = wc*hc

                    #Area para la sBox
                    if (area > 1250 and area < 2500 and conteo == True):
                        sBox = sBox + 1
                        conteo = False
                        #Funciones de texto
                        boxs = swText("Han pasado ", sBox, " cajas tamaño S ")
                        #Funciones para las label
                        lbSbox = wTab(my_frame2, boxs)
                        #Funciones organizadoras
                        organ(lbSbox, 5, 1, 0, 0)
                        break

                    #Area para la mBox        
                    if (area>2510 and area<3000 and conteo == True):
                        mBox = mBox + 1
                        conteo = False
                        #Funciones de texto
                        boxm = swText("Han pasado ", mBox, " cajas tamaño M ")
                        #Funciones para las label
                        lbMbox = wTab(my_frame2, boxm)
                        #Funciones organizadoras
                        organ(lbMbox, 5, 2, 0, 0)
                        break

                    #Area para la lBox  
                    if (area>3000 and conteo == True):
                        lBox = lBox + 1
                        conteo = False
                        #Funciones de texto
                        boxl = swText("Han pasado ", lBox, " cajas tamaño L ")
                        #Funciones para las label
                        lbBbox = wTab(my_frame2, boxl)
                        #Funciones organizadoras
                        organ(lbBbox, 5, 3, 0, 0)
                        break

            videoc = Image.fromarray(frame2)
            framemov = ImageTk.PhotoImage(image = videoc)
            videoViewer2.configure(image = framemov)
            videoViewer2.image = framemov
            videoViewer2.after(1, medicion2)
        else:
            capture.release()
            capture = None
            capture = cv.VideoCapture(path)
    

def medicion3():
    global azul, gris, verde, capture, color, conta3, conta2, conta1
    if capture is not None:
        ret, frame = capture.read()
        if (ret == True):
            frame_gray = cv.cvtColor (frame, cv.COLOR_BGR2GRAY)
            frame3 = cv.resize(frame[100:550,350:500],(200,600))
            h, w = frame_gray.shape

            regioncolor = frame[190:210,405:425]
            regioncolor = cv.resize(regioncolor,(200,200))

            #Pixel en el que todos los elementos van a pasar, defino un rango en el que van todos los colores
            if((int(frame[200][415][1]) + int (frame[200][415][0]))^2 <130 and  (int(frame[200][415][1]) + int (frame[200][415][0]))^2 >100):
                color = True
            else:
                if (color == True):

                    #Defino un umbral, un ROI, y los contornos dentro de mi ROI
                    ret6, frame_binary_5 = cv.threshold(frame_gray, 130, 255, cv.THRESH_BINARY)
                    region2 = frame_binary_5[138:252, 355:467]
                    h3, w3 = region2.shape
                    contours3, hierarchy3 = cv.findContours(region2.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                    img_contours3 = np.zeros((h3, w3, 3), np.uint8)

                    #Defino el color azul claro, azul canal 0, verde canal 1, rojo canal 2
                    if ((int(frame[190][415][1]) + int(frame[195][415][0]) > 400)):
                        color = False
                        azul = azul + 1
                        #Funciones de texto
                        azulc = swText("Pasaron ", azul, " cajas de material azul ")
                        #Funciones para las label
                        lbBlue = wTab(my_frame3, azulc)
                        #Funciones organizadoras
                        organ(lbBlue, 5, 1, 0, 0)

                        for cnt in contours3:
                            x, y, wc, hc = cv.boundingRect(cnt)
                            area = wc*hc
                             #Contadores para cada una de las zonas de la banda según el ROI
                            if (area > 1000):
                                cv.drawContours(
                                    img_contours3, cnt, -1, (255, 0, 0), 2)

                                if (x < 10):
                                    conta3 = conta3 + 1

                                if (x < 35 and x > 25):
                                    conta2 = conta2 + 1

                                if (x > 50):
                                    conta1 = conta1 + 1
                                break

                    #Defino el color verde, azul canal 0, verde canal 1, rojo canal 2
                    if ((int(frame[192][415][1]) + int (frame[193][415][0])>240 and (int(frame[200][415][1]) + int (frame[200][415][0])<260))):
                        color = False
                        verde = verde + 1
                        #Funciones de texto
                        verdec = swText("Pasaron ",verde," cajas de material verde ")
                        #Funciones para las label
                        lbGreen = wTab(my_frame3, verdec)
                        #Funciones organizadoras
                        organ(lbGreen, 5, 2, 0, 0)
                            
                        for cnt in contours3:
                            x, y, wc, hc = cv.boundingRect(cnt)
                            area = wc*hc
                            #Contadores para cada una de las zonas de la banda según el ROI
                            if (area>1000):
                                cv.drawContours(img_contours3, cnt, -1, (255,0,0), 2)
                                if (x<10):
                                    conta3 = conta3 + 1
                                        
                                if (x<35 and x>25): 
                                    conta2 = conta2 + 1

                                if (x>50):
                                    conta1 = conta1 + 1
                                break

                    #Defino el color gris, azul canal 0, verde canal 1, rojo canal 2
                    if ((int(frame[200][415][1]) + int (frame[200][415][0])>280 and (int(frame[200][415][1]) + int (frame[200][415][0])<330))):
                        color = False
                        gris = gris + 1
                        #Funciones de texto
                        grisc = swText("Pasaron ",gris," cajas de material gris ")
                        #Funciones para las label
                        lbGray = wTab(my_frame3, grisc)
                        #Funciones organizadoras
                        organ(lbGray, 5, 3, 0, 0)

                        for cnt in contours3:
                            x, y, wc, hc = cv.boundingRect(cnt)
                            area = wc*hc
                            #Contadores para cada una de las zonas de la banda según el ROI
                            if (area>1000):
                                cv.drawContours(img_contours3, cnt, -1, (255,0,0), 2)
                                if (x<10):
                                    conta3 = conta3 + 1
    
                                if (x<35 and x>25):
                                    conta2 = conta2 + 1

                                if (x>50):
                                    conta1 = conta1 + 1
                            break

                    #Defino por donde se movieron las cajas de material
                    circulacion = str("Pasaron "+str(conta3)+" por la izquierda de la banda, "+str(conta2)+" por el centro y "+str(conta1)+" por la derecha de la banda")
                    lbposition = wTab(my_frame3,circulacion)
                    total = conta3 + conta2 + conta1
                    #Escribo el total de cajas que transcurrieron
                    cirtot = swText("Circularon ",total," cajas de material en total")
                    lbtotal = wTab(my_frame3,cirtot)
                    lbposition.grid(column = 0, row = 8, padx = 10, pady = 10, columnspan = 4)
                    lbtotal.grid(column = 0, row = 9, padx = 10, pady = 10, columnspan = 4)
  
            #Interfaz gráfica
            videoc3 = Image.fromarray(frame3)
            framemov3 = ImageTk.PhotoImage(image = videoc3)
            videoViewer3.configure(image = framemov3)
            videoViewer3.image = framemov3
            videoViewer3.after(1, medicion3)

        else:
            capture.release()
            capture = None
            capture = cv.VideoCapture(path)

            
if __name__ == "__main__":
    root = Tk()
    notebook = ttk.Notebook(root)
    notebook.pack()
    my_frame1 = Frame(notebook, width=200, heigh=200, bg="light gray")
    my_frame2 = Frame(notebook, width=200, heigh=200, bg="light gray")
    my_frame3 = Frame(notebook, width=200, heigh=200, bg="light gray")

    notebook.add(my_frame1, text="Banda Izquierda")
    notebook.add(my_frame2, text="Banda Central")
    notebook.add(my_frame3, text="Banda Derecha")

    videoViewer1 = Label(my_frame1,text="Open CV Image", bg= "gray",font = "Times")
    videoViewer1.grid(column = 0, row = 1,padx = 30, pady = 30, rowspan = 5, columnspan = 4)
    videoViewer2 = Label(my_frame2,text="Open CV Image", bg= "gray",font = "Times")
    videoViewer2.grid(column = 0, row = 1,padx = 30, pady = 30, rowspan = 5, columnspan = 4)
    videoViewer3 = Label(my_frame3,text="Open CV Image", bg= "gray",font = "Times")
    videoViewer3.grid(column = 0, row = 1,padx = 30, pady = 30, rowspan = 5, columnspan = 4)

    btnLoad = Button(my_frame1, text = "Cargar video", width = 20, command = loadVideo)
    btnLoad.grid(column = 0, row = 6, padx = 10, pady = 10, columnspan = 2)
    bti1 = Button(my_frame1, text = "Inicio", width = 20, command = medicion1)
    bti1.grid(column = 2, row = 6, padx = 10, pady =10 , columnspan = 2)
    btnLoad2 = Button(my_frame2, text = "Cargar video", width = 20, command = loadVideo)
    btnLoad2.grid(column = 0, row = 6, padx = 10, pady = 10, columnspan = 2)
    bti2 = Button(my_frame2, text = "Inicio", width = 20, command = medicion2)
    bti2.grid(column = 2, row = 6, padx = 10, pady =10 , columnspan = 2)
    btnLoad3 = Button(my_frame3, text = "Cargar video", width = 20, command = loadVideo)
    btnLoad3.grid(column = 0, row = 6, padx = 10, pady = 10, columnspan = 2)
    bti3 = Button(my_frame3, text = "Inicio", width = 20, command = medicion3)
    bti3.grid(column = 2, row = 6, padx = 10, pady =10 , columnspan = 2)

    root.mainloop()