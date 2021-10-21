import cv2 as cv
import numpy as np

x1 = y1 = 0

# Binarizar una imagen

def binary(imgGray, u):
    (h, w) = imgGray.shape[:2]
    for i in range(0, h):
        for j in range(0, w):
            if imgGray[i][j] >= u:
                imgGray[i][j] = 255
            else:
                imgGray[i][j] = 0
    return imgGray


def roiImg(img):
    global x1, y1, x2, y2, bandRoi, vector1
    if bandRoi == True:
        roiImage = img[y1:y2, x1:x2]
        showImage('roiImage', roiImage, 1)


def mouseClick(event,x,y,flags,param,):
    global x1, y1, x2, y2, bandRoi, vector1

    if event == cv.EVENT_LBUTTONDOWN:
        x1 = x
        y1 = y

    if event == cv.EVENT_LBUTTONUP:
        x2 = x
        y2 = y
        bandRoi = True
        vector1.append([x1, y1, x2, y2])
        diagonal(x1, y1, x2, y2)
        distancia(x1, x2)

        # print(vector1)

    return vector1


path1 = '22.jpg'
if __name__ == '__main__':

    img1 = cv.imread(path1, 1)
    imgGray = cv.imread(path1, 0)
    cv.imshow('imgColor', img1)
    cv.namedWindow('imgColor')
    cv.setMouseCallback('imgColor', mouseClick)

cv.waitKey(0)
cv.destroyAllWindows()