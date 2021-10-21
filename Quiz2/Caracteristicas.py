import cv2 as cv
import numpy as np
import xlsxwriter as xw
from glob import glob

row = 0
col = 0

i=1
j=1 
m=3
n=3
k=np.ones((m,n),np.uint8)
#crear el archivo excel de forma global

workbook = xw.Workbook ("Letras10.xlsx")
worksheet = workbook.add_worksheet ("CaractLetras")

vectorLetras = ["T","R","A","E","S","I","G","C","D","Z"]

for j in range (0, len(vectorLetras)):
    for imgPath in glob("Letras/"+vectorLetras[j]+"/*.jpg"):
        imgColor = cv.imread(imgPath,1)
        imgColor = cv.resize(imgColor, (50,100))
        img = cv.imread(imgPath,0)
        img = cv.resize(img, (50,100))

        ret, imgBin = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        img_dilate = cv.dilate(imgBin.copy(), kernel=k, iterations=j)
        

        #encontrar y almacenar contornos
        contours, hierarchy = cv.findContours(img_dilate.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        for cnt in contours:
            x,y,w,h = cv.boundingRect(cnt)
            area = cv.contourArea(cnt)
            if(area>500):
                per = cv.arcLength(cnt, True)      #perimetro
                ra = w/h                           #razon aspecto
                com= area / (pow(per,2))           #compacidad
                rec = area/(w*h)                   #rectangularidad
                mom = cv.moments(cnt)              #momentos
                HU = cv.HuMoments(mom)             #momentos hu
                ex = area/(w*h)                    #Extension   
                cx = float(mom['m10']/mom['m00'])  #centroide x
                cy = float(mom['m01']/mom['m00'])  #centroide y
                hull = cv.convexHull(cnt)
                hull_area = cv.contourArea(hull)   #area envoltura convexa
                sol = float(area)/hull_area        #solidez
                de = np.sqrt(4*area/np.pi)         #diametro equivalente
                _,(MA,ma),angle = cv.fitEllipse(cnt) #eje mayor, eje menor, angulo
                
                #puntos extremos
                left = tuple(cnt[cnt[:,:,0].argmin()][0])
                right = tuple(cnt[cnt[:,:,0].argmax()][0])
                sup = tuple(cnt[cnt[:,:,1].argmin()][0])
                inf = tuple(cnt[cnt[:,:,1].argmax()][0])
                
                
                vectorCaract = np.array([area, per, com, rec, HU[0,0], HU[1,0], HU[2,0], HU[3,0], HU[4,0], HU[5,0], 
                                            HU[6,0], cx, cy, ex, hull_area, sol, de, MA, ma, angle, left[1], right[1], 
                                            sup[0], inf[0]], dtype = np.float32)
                for carac in vectorCaract:
                    worksheet.write(row,col,vectorLetras[j])
                    worksheet.write(row,i,carac)
                    i = i + 1
                i = 1
                row = row + 1

workbook.close()
print ("Caracteristicas Encontradas")
