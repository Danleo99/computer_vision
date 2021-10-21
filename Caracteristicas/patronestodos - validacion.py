import cv2 as cv
import numpy as np
from glob import glob
import joblib
from sklearn.feature_selection import VarianceThreshold

model_mlpc = joblib.load('model_mlpc.pkl') #Cargo el modelo
model_ssc = joblib.load('model_ssc.pkl')
#Nombre de las carpetas a recorrer
vectorNum = ['0','1','2','3','4','5','6','7','8','9']
sel = VarianceThreshold(threshold=(.8 * (1 - .8)))

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
                cv.rectangle(imgColor, (x,y),(x+w, y+h), (255,0,0), 2)
                cv.imshow('img',imgColor)
                cv.waitKey(0)
                p = cv.arcLength(cnt,True)
                ra = float(w/h)
                c = a/(pow(p,2))
                rg = a/(w*h)
                M = cv.moments(cnt)
                Hu = cv.HuMoments(M)
                #Diametro equivalente
                de = np.sqrt(4*a/np.pi)

                #Orientación(largo eje maor, largo eje menor y angulo)
                (xi,yi),(MA,ma),angle = cv.fitEllipse(cnt)

                #mascara y color medio o intensidad media
                mask = np.zeros(img.shape,np.uint8)
                mv = cv.mean(imgColor,mask = mask)

                #puntos extremos
                izq = tuple(cnt[cnt[:,:,0].argmin()][0])
                der = tuple(cnt[cnt[:,:,0].argmax()][0])
                sup = tuple(cnt[cnt[:,:,1].argmin()][0])
                inf = tuple(cnt[cnt[:,:,1].argmax()][0])

                #aproximación contorno
                epsilon = 0.01*p
                approx = cv.approxPolyDP(cnt,epsilon,True)

                #número de vertices
                cantv = len(approx)

                #Envoltura convexa
                envoltura = cv.convexHull(cnt)
                cantc = len(envoltura)

                #Solidez
                area_envoltura = cv.contourArea(envoltura)
                solidez = float(a)/area_envoltura

                #Rectángulo rotado
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                im = cv.drawContours(imgColor,[box],0,(0,0,255),2)

                #circulo mínimo de inclusión
                (xinc,yinc),radius = cv.minEnclosingCircle(cnt)
                center = (int(xinc),int(yinc))
                radius = int(radius)
                imgCirculo = cv.circle(imgColor,center,radius,(0,255,0),2)

                vectorCarac = np.array([a,p,ra,c,rg,de,MA,ma,angle,izq[0],izq[1],der[0],der[1],sup[0],sup[1],\
                                         inf[0],inf[1],cantv,cantc,Hu[0][0],Hu[1][0],Hu[2][0]], dtype = np.float32)

                #Reshape según como sea el modelo
                vectorCarac = vectorCarac.reshape(1,-1)
                vectorCarac = model_ssc.transform(vectorCarac)
                result=model_mlpc.predict(vectorCarac.reshape(1,-1))

                if(result[0] == 0):
                    print("el número es: ", 0)

                elif(result[0] == 1):
                    print("el número es: ", 1)

                elif(result[0] == 2):
                    print("el número es: ", 2)

                elif(result[0] == 3):
                    print("el número es: ", 3)

                elif(result[0] == 4):
                    print("el número es: ", 4)

                elif(result[0] == 5):
                    print("el número es: ", 5)

                elif(result[0] == 6):
                    print("el número es: ", 6)

                elif(result[0] == 7):
                    print("el número es: ", 7)

                elif(result[0] == 8):
                    print("el número es: ", 8)

                elif(result[0] == 9):
                    print("el número es: ", 9)


print('Archivo Terminado')




