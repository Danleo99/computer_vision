import cv2
import numpy as np
import xlsxwriter as xw
from glob import glob

row = 0
col = 0

i=1

#crear el archivo excel de forma global

workbook = xw.Workbook ("DataNumsTodos.xlsx")
worksheet = workbook.add_worksheet ("CaractNums")

vectorNums = ["0","1","2","3","4","5","6","7","8","9"]

for j in range (0, len(vectorNums)):
    for imgPath in glob("num/"+vectorNums[j]+"/*.png"):
        imgColor = cv2.imread(imgPath,1)
        imgColor = cv2.resize(imgColor, (25,50))
        img = cv2.imread(imgPath,0)
        img = cv2.resize(img, (25,50))

        ret, imgBin = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        #encontrar y almacenar contornos
        contours, hierarchy = cv2.findContours(imgBin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            a = cv2.contourArea(cnt)
            if(a>10):
                cv2.rectangle(imgColor, (x,y),(x+w, y+h), (255,0,0), 2)
                p = cv2.arcLength(cnt,True)
                ra = float(w/h)
                c = a/(pow(p,2))
                rg = a/(w*h)
                M = cv2.moments(cnt)
                Hu = cv2.HuMoments(M)
                #Diametro equivalente
                de = np.sqrt(4*a/np.pi)

                #Orientación(largo eje maor, largo eje menor y angulo)
                (xi,yi),(MA,ma),angle = cv2.fitEllipse(cnt)

                #mascara y color medio o intensidad media
                mask = np.zeros(img.shape,np.uint8)
                mv = cv2.mean(imgColor,mask = mask)

                #puntos extremos
                izq = tuple(cnt[cnt[:,:,0].argmin()][0])
                der = tuple(cnt[cnt[:,:,0].argmax()][0])
                sup = tuple(cnt[cnt[:,:,1].argmin()][0])
                inf = tuple(cnt[cnt[:,:,1].argmax()][0])

                #aproximación contorno
                epsilon = 0.01*p
                approx = cv2.approxPolyDP(cnt,epsilon,True)

                #número de vertices
                cantv = len(approx)

                #Envoltura convexa
                envoltura = cv2.convexHull(cnt)
                cantc = len(envoltura)

                #Solidez
                area_envoltura = cv2.contourArea(envoltura)
                solidez = float(a)/area_envoltura

                #Rectángulo rotado
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                im = cv2.drawContours(imgColor,[box],0,(0,0,255),2)

                #circulo mínimo de inclusión
                (xinc,yinc),radius = cv2.minEnclosingCircle(cnt)
                center = (int(xinc),int(yinc))
                radius = int(radius)
                imgCirculo = cv2.circle(imgColor,center,radius,(0,255,0),2)


                vectorCaract = np.array([a,p,ra,c,rg,de,MA,ma,angle,izq[0],izq[1],der[0],der[1],sup[0],sup[1],\
                                         inf[0],inf[1],cantv,cantc,Hu[0][0],Hu[1][0],Hu[2][0]], dtype = np.float32)
                for carac in vectorCaract:
                    worksheet.write(row,col,vectorNums[j])
                    worksheet.write(row,i,carac)
                    i = i + 1
                i = 1
                row = row + 1

workbook.close()
print ("fin")
