import cv2 as cv
import numpy as np
import xlsxwriter as xw 
from glob import glob

row = 0
col = 0 

i=1 

#Abro el libro
wbook = xw.Workbook('DataNumsPairs.xlsx')

#Escojo la hoja
wsheet = wbook.add_worksheet('Caracteristicas')

#Nombre de las carpetas a recorrer
vectorNum = ['0','2','4','6','8',]

#Quiero recorrer las carpetas
for j in range(0,len(vectorNum)):
    #Dentro de las carpetas, recorro los archivos
    #El glob se encarga de recorrer los archivos dentro de la carpeta
    for imgPath in glob('num/'+ vectorNum[j]+ '/*.png'):
        
        #Llamo las imágenes a color y normal con el fin de dibujar sobre ella a color
        imgColor = cv.imread(imgPath, 1)
        img = cv.imread(imgPath, 0)
        #Necesito que todas las imagenes sean del mismo tamaño
        img = cv.resize(img, (25,50))
        imgColor = cv.resize(imgColor, (25,50))

        ret, imgBin = cv.threshold(img,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)        
        contours, hiteracy = cv.findContours(imgBin.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
        
        for cnt in contours:
            x,y,w,h = cv.boundingRect(cnt)
            a = cv.contourArea(cnt)
            #print(a)
            if (a > 10):
                cv.rectangle(imgColor, (x,y), (x+w, y+h), (255,0,0),2) #Me muevo desde un lugar X y Y, hasta el desplazamiento total, su espesor y su altura
                p = cv.arcLength(cnt,True) #Perímetro, longitud de arco
                ra = float(w/h) #Relación de aspecto, ancho/alto
                c = a/(pow(p,2)) #Compasidad
                rg = a/(w*h) #Rectangularidad, Area/wh
                M = cv.moments(cnt) #Momentos
                Hu = cv.HuMoments(M) #Momentos de Hu
                env = cv.convexHull(cnt)
                revcon = cv.isContourConvex(cnt) #Convexidad
                #print(Hu[0][0],Hu[1][0])
                
                
                vectorCarac = np.array([a,p,ra,c,rg,Hu[0][0],Hu[1][0],Hu[2][0]], dtype=np.float32)
                for carac in vectorCarac :
                    wsheet.write(row, col, vectorNum[j])
                    wsheet.write(row, i, carac)
                    i = i + 1
                
                i = 1
                row = row + 1

wbook.close()
print('Archivo Terminado')




