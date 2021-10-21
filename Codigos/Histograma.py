import cv2 as cv
import numpy as np

def showHistogram(imgGray):
    wbins = 256
    hbins = 256
    histr = cv.calcHist([imgGray], [0],None,[hbins],[wbins])
    print (histr)
    min_val,max_val,min_loc,max_loc = cv.minMaxLoc(histr)
    imgHist = np.zeros([hbins, wbins],np.uint8)
    for w in range(wbins):
        binVl = histr[w]
        intensity = binVal*(hbins-1)/max_val
        cv.line(imgHist,(w,hbins), (w,hbins-intensity),255)
    return imgHist

path1 = "21.jpg"
path2 = "22.2.jpg"
if __name__ == "__main__":
    img1 = cv.imread(path1,1)
    img2 = cv.imread(path2,0)
    imgGray = cv.imread(path1,0)
    cv.imshow("imColor",img1)
    showHistogram(imgGray)
    cv.imshow("imHisto",imgHist)
    
cv.waitKey(0)
cv.destroyAllWindows()
    
