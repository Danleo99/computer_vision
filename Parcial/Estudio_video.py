import cv2 as cv
import numpy as np
import time 

path = "videoParcial.mp4"

capture = cv.VideoCapture(path)
time.sleep(1)
pbox=0
spll=0
bpll=0
Sbox=0
Mbox=0
while (capture.isOpened()):
	
	ret, frame = capture.read()
	
	if (ret == False):
		break

	banda1 = frame[250:450,45:180]
	banda2 = frame[100:400,190:340]
	banda3 = frame[100:400,350:480]

	frame_gray1 = cv.cvtColor(banda1, cv.COLOR_BGR2GRAY)
	ret1, frame_binary1 = cv.threshold(frame_gray1, 160, 255, cv.THRESH_BINARY)
	contours1, hierarchy1 = cv.findContours(frame_binary1.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

	frame_gray2 = cv.cvtColor(banda2, cv.COLOR_BGR2GRAY)
	ret2, frame_binary2 = cv.threshold(frame_gray2, 180, 255, cv.THRESH_BINARY)
	contours2, hierarchy2 = cv.findContours(frame_binary2.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

	frame_gray3 = cv.cvtColor(banda3, cv.COLOR_BGR2GRAY)
	ret3, frame_binary3 = cv.threshold(frame_gray3, 120, 255, cv.THRESH_BINARY)
	contours3, hierarchy3 = cv.findContours(frame_binary3.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
	#print (hierarchy)

	h1,w1 = frame_gray1.shape
	img_contours1 = np.zeros((h1,w1,3), np.uint8)
	h2,w2 = frame_gray2.shape
	img_contours2 = np.zeros((h2,w2,3), np.uint8)
	h3,w3 = frame_gray3.shape
	img_contours3 = np.zeros((h3,w3,3), np.uint8)

	for cnt in contours1:
		x, y, wc, hc = cv.boundingRect(cnt)
		area = wc*hc
		if (14100<area and area<14300):
			#print(area)
			#cv.drawContours(img_contours1, cnt, -1, (255,0,0), 2)
			#cv.imshow('Contornos',img_contours1)
			pbox=pbox+1
			cv.waitKey(1)


		elif(3000<area and area<3100):
			#print(area)
			cv.drawContours(img_contours1, cnt, -1, (255,0,0), 2)
			cv.imshow('Contornos',img_contours1)
			spll=spll+1
			#print('Cantidad de small pallete ', spll)
			cv.waitKey(1)

		elif(3100<area and area<3300):
			#print(area)
			cv.drawContours(img_contours1, cnt, -1, (255,0,0), 2)
			cv.imshow('Contornos',img_contours1)
			bpll=bpll+1
			#print('Cantidad de small pallete ', spll)
			cv.waitKey(1)

	for cnt in contours2:
		x, y, wc, hc = cv.boundingRect(cnt)
		area = wc*hc
		if (3800<area and area<4000 and area!=4200 ):

			#print(area)
			#cv.drawContours(img_contours2, cnt, -1, (255,0,0), 2)
			#cv.imshow('Contornos',img_contours2)
			Sbox=Sbox+1
			#print('Cantidad de small box ', Sbox)
			cv.waitKey(1)

		elif(10000<area and area<15000):
			#print(area)
			#cv.drawContours(img_contours2, cnt, -1, (255,0,0), 2)
			#cv.imshow('Contornos',img_contours2)
			Mbox=Mbox+1
			#print('Cantidad de small pallete ', spll)
			cv.waitKey(1)

	for cnt in contours3:
		x, y, wc, hc = cv.boundingRect(cnt)
		area = wc*hc
		if (3180==area or area==3240):
			print(x)
			if (x<20):
				print('Material a la izquierda')
			if (x<50 and x>20):
				print('Material en el centro')
			if (x>50):
				print('Material a la derecha')
			#cv.drawContours(img_contours3, cnt, -1, (255,0,0), 2)
			#cv.imshow('Contornos',img_contours3)

	cv.imshow('Binarizado', frame_binary1)
	cv.waitKey(30)


print('Cantidad de plastic box ', pbox)
print('Cantidad de small pallete ', spll)
print('Cantidad de big pallete ', bpll)
print('Cantidad de small box ', Sbox)
capture.release()
cv.destroyAllWindows()
