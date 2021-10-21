import cv2 as cv
import numpy as np
import time 

path = "Billar.mp4"

capture = cv.VideoCapture(0)
time.sleep(2)

while (capture.isOpened()):
	
	ret, frame = capture.read()
	
	if (ret == False):
		break

	frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	ret1, frame_binary1 = cv.threshold(frame_gray, 173, 255, cv.THRESH_BINARY)
	ret2, frame_binary2 = cv.threshold(frame_gray, 218, 255, cv.THRESH_BINARY)
	resta = cv.absdiff(frame_binary1,frame_binary2)
	contours, hierarchy = cv.findContours(resta.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

	h,w = frame_gray.shape
	img_contours = np.zeros((h,w,3), np.uint8)
	
	for cnt in contours:
		x, y, wc, hc = cv.boundingRect(cnt)
		area = wc*hc
		if (area > 50):
			cv.drawContours(img_contours, cnt, -1, (255,0,0), 2)
			cv.imshow('Contornos',img_contours)
			cv.waitKey(1)

	#cv.imshow('Normal',frame)
	cv.imshow('Binarizado', resta)
	cv.waitKey(1)

capture.release()
cv.destroyAllWindows()