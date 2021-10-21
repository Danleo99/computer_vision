import cv2 as cv
import numpy as np
import xlsxwriter as xw 
from glob import glob

row = 0
col = 0 

i=1 

wbook = xw.Workbook('DataNums.xlsx')
wsheet = wbook.add_worksheet('Caracteristicas')

vectorNum = ['0','1','2','3','4','5','6','7','8','9']

for j in range(0,len(vectorNum)):
    for imgPath in glob('num/'+ vectorNum[j]+ '/*.png'):
        
        imgColor = cv.imread(imgPath, 1)
        img = cv.imread(imgPath, 0)
        img = cv.resize(img, (25,50))
        imgColor = cv.resize(imgColor, (25,50))
        #cv.imshow('img_gray',img)
        #cv.waitKey(0)

        ret, imgBin = cv.threshold(img,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)        
        contours, hiteracy = cv.findContours(imgBin.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
        
        for cnt in contours:
            x,y,w,h = cv.boundingRect(cnt)
            a = cv.contourArea(cnt)
            #print(a)
            if (a > 10):
                cv.rectangle(imgColor, (x,y), (x+w, y+h), (255,0,0),2)
                p = cv.arcLength(cnt,True)
                ra = float(w/h)
                c = a/(pow(p,2))
                rg = a/(w*h)
                M = cv.moments(cnt)
                Hu = cv.HuMoments(M)
                env = cv.convexHull(cnt)
                revcon = cv.isContourConvex(cnt)
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