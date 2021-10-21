import cv2 as cv
import numpy as np

#Definimos los vectores para las imagenes
buenas = []
malas = []

#Creamos la funcion que nos compara si las imagenes son iguales
def compare(imagen1,imagen2):
	diferencia = cv.subtract(imagen1,imagen2)
	if not np.any(diferencia):
		#Si son iguales
		return 1
	else:
		#Si son diferentes
		return 0

#Cargamos las imagenes
def cargarImg():
	for i in range (1,6):
		print ('Cargando Imagen',i,'...')
		imgbn = cv.imread('placa_'+str(i)+'_Original.png',1)
		imgml = cv.imread('placa_'+str(i)+'_P1.png',1)
		buenas.append(imgbn)
		malas.append(imgml)

if __name__ == '__main__':
	#Usamos la Funcion de cargar imagenes
	cargarImg()

	#Mostramos las imagenes antes de ser corregidas
	for i in range(0,5):
		cv.imshow('Imagen mala '+str(i+1),malas[i])

	cv.waitKey(0)
	cv.destroyAllWindows()

	#Comparamos las imagenes para saber si toca rotarlas
	for i in range (0,5):
		print('Procesando imagen',i+1)
		change = compare(buenas[i],malas[i])
		if (change == 1):
			print('Imagen OK')
		else:
			#Rotamos sobre el eje x
			malas[i]=cv.flip(malas[i],0)
			#Comparamos por segunda vez para saber si es necesaria rotarla sobre y
			change2 = compare(buenas[i],malas[i])
			if (change2 == 1):
				print('Imagen OK')
			else:
				#Rotamos sobre el eje y
				malas[i]=cv.flip(malas[i],1)
				print('Imagen OK')

	#Mostramos las imagenes corregidas
	for i in range(0,5):
		cv.imshow('Imagen corregida '+str(i+1),malas[i])

	cv.waitKey(0)
	cv.destroyAllWindows()