import csv
import cv2
import glob
import numpy as np
import os.path
import shutil

path = 'imagesYOLO/'
COLOR = [(255, 0, 0), (0, 0, 255), (0, 255, 255)]
EXIT = False

def readCSV(fileTXT):
    global EXIT
    with open(fileTXT) as File:
        reader = csv.reader(File, delimiter=' ')
        fileImg = fileTXT[:fileTXT.find('.')] + '.jpg'
        img = cv2.imread(fileImg)
        H, W = img.shape[:2]
        for row in reader:
            cx = int(float(row[1]) * W)
            cy = int(float(row[2]) * H)
            x1 = cx - int(float(row[3]) * W / 2)
            x2 = cx + int(float(row[3]) * W / 2)
            y1 = cy - int(float(row[4]) * H / 2)
            y2 = cy + int(float(row[4]) * H / 2)
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)  
            cv2.rectangle(img, (x1, y1), (x2, y2), COLOR[int(row[0])], 5)
            
        cv2.imshow("image", cv2.resize(img, (920, 640)))                  
        key = cv2.waitKey()      
        if key == ord('q'):
            EXIT = True
        #cv2.destroyAllWindows()
        
for p in glob.glob(path + "\*.txt"):
    print(p)
    readCSV(p)
    if EXIT:
        break
print("FIN")
