import cv2 as cv
import numpy as np
from glob import glob
import joblib
import xlsxwriter as xw

model_mlpc = joblib.load('model_mlpc.pkl')  # Cargo el modelo
model_ssc = joblib.load('model_ssc.pkl')

j = 1
m = 3
n = 3
k = np.ones((m, n), np.uint8)

#imgPath = 'Prueba5.jpeg'
imgPath = 'Test/test_200/test_200.png'

imgColor = cv.imread(imgPath, 1)
img = cv.imread(imgPath, 0)

ret, imgBin = cv.threshold(img, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
img_dilate = cv.dilate(imgBin.copy(), kernel=k, iterations=j)


# encontrar y almacenar contornos
contours, hierarchy = cv.findContours(img_dilate.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
letra = ''
for cnt in contours:
    #Ajuste del contorno de la Imagen Test
    x, y, w, h = cv.boundingRect(cnt)
    area = cv.contourArea(cnt)
    if(area > 500):
        imgroi = imgColor[y:(y+h),x:(x+w)]
        imgroiResize = cv.resize(imgroi, (30,60))
        imgroiBinary = imgBin[y:(y+h),x:(x+w)]
        imgroiBinaryR = cv.resize(imgroiBinary,(30,60))
        cv.imshow('img', imgroiBinaryR)
        cv.waitKey(0)
        
        #Contorno de la imagen ajustada
        contour2, hierarchy2 = cv.findContours(imgroiBinaryR.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        for cnt2 in contour2:
            x1, y1, w1, h1 = cv.boundingRect(cnt2)
            area2 = cv.contourArea(cnt2)
            if(area > 500):
                cv.rectangle(imgColor, (x, y), (x+w, y+h), (255, 255, 0), 2)
                per = cv.arcLength(cnt2, True)  # Perimetro
                ra = w/h  # Relacicion de aspecto
                com = area / (pow(per, 2))  # Compacidad
                rec = area/(w*h)  # Rectangularidad
                mom = cv.moments(cnt2)  # Momentos
                HU = cv.HuMoments(mom)  # Momentos hu
                ex = area/(w*h)  # Extension
                cx = float(mom['m10']/mom['m00'])  # Centroide x
                cy = float(mom['m01']/mom['m00'])  # Centroide y
                hull = cv.convexHull(cnt2)
                hull_area = cv.contourArea(hull)  # Area envoltura convexa
                sol = float(area)/hull_area  # Solidez
                de = np.sqrt(4*area/np.pi)  # Diametro equivalente
                _, (MA, ma), angle = cv.fitEllipse(cnt2)  # eje mayor, eje menor, angulo

                # puntos extremos
                left = tuple(cnt2[cnt2[:, :, 0].argmin()][0])
                right = tuple(cnt2[cnt2[:, :, 0].argmax()][0])
                sup = tuple(cnt2[cnt2[:, :, 1].argmin()][0])
                inf = tuple(cnt2[cnt2[:, :, 1].argmax()][0])

                vectorCaract = np.array([area, per, com, rec, HU[0, 0], HU[1, 0], HU[2, 0], HU[3, 0], HU[4, 0], HU[5, 0],
                                        HU[6, 0], cx, cy, ex, hull_area, sol, de, MA, ma, angle, left[1],
                                        right[1], sup[0], inf[0]], dtype=np.float32)

                vectorCaract = vectorCaract.reshape(1, -1)
                vectorCaract = model_ssc.transform(vectorCaract)
                result = model_mlpc.predict(vectorCaract.reshape(1, -1))

                if(result == 0):  # Lleva las comillas porque es un string
                    letra = 'T'
                if(result == 1):  # Lleva las comillas porque es un string
                    letra = 'R'
                if(result == 2):  # Lleva las comillas porque es un string
                    letra = 'A'
                if(result == 3):  # Lleva las comillas porque es un string
                    letra = 'E'
                if(result == 4):  # Lleva las comillas porque es un string
                    letra = 'S'
                if(result == 5):  # Lleva las comillas porque es un string
                    letra = 'I'
                if(result == 6):  # Lleva las comillas porque es un string
                    letra = 'G'
                if(result == 7):  # Lleva las comillas porque es un string
                    letra = 'C'
                if(result == 8):  # Lleva las comillas porque es un string
                    letra = 'D'
                if(result == 9):  # Lleva las comillas porque es un string
                    letra = 'Z'

        cv.putText(imgColor, letra, (x+w-25, y+h+50),cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)
        cv.imshow('img', imgColor)
        cv.waitKey(0)
