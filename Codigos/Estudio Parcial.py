import cv2 as cv
import numpy as np

path1 = "gato.jpg"
path2 = "nega2.png" 
img1 = cv.imread(path1,0)
img2 = cv.imread(path2,0)

ret1, frame_binary1 = cv.threshold(img1, 200, 255, cv.THRESH_BINARY)
ret2, frame_binary2 = cv.threshold(img1, 100, 255, cv.THRESH_BINARY)
resta = cv.absdiff(frame_binary1,frame_binary2)
#suma = cv.subtract(img1,img2)

cv.imshow('cosa',resta)

cv.waitKey(0)
cv.destroyAllWindows()