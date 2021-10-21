#Importar librerías
import numpy as np
import cv2 as cv

def imagenOriginal(rutaImagen):
    imagen = cv.imread(rutaImagen,1)
    cv.imshow("Imagen Original",imagen)

def dejarColor(rutaImagen, color):
    imagen = cv.imread(rutaImagen,1)
    colores ={'azul':0, 'verde': 1, 'rojo': 2}
    h,w = imagen.shape[:2]

    for i in range(0,h):
        for j in range(0,w):
            for k in range(0,3):
                if colores[color]!=k:
                    if (imagen[i][j][k] > 0):
                         imagen[i][j][k] = 0

    cv.imshow("Imagen "+color,imagen)

def invertirEje(rutaImagen, eje):
    imagen = cv.imread(rutaImagen,1)
    copia = cv.imread(rutaImagen,1)
    h,w = imagen.shape[:2]

    if eje=="y":
        for i in range (0,h):
            for j in range (0,w):
                imagen[i][j] = copia[i][w-j-1]
        cv.imshow("Imagen invertida en Y", imagen)

    if eje=="x":
        for i in range (0,h):
            for j in range (0,w):
                imagen[i][j] = copia[h-i-1][j]
                # Se reescribe el valor de cada pixel de la imagen con el valor de la copia
        cv.imshow("Imagen invertida en X", imagen)

def dejarColorCuadricula(imagen, color):
    colores ={'azul':0, 'verde': 1, 'rojo': 2}
    h,w = imagen.shape[:2]

    for i in range(0,h):
        for j in range(0,w):
            for k in range(0,3):
                if colores[color]!=k:
                    if (imagen[i][j][k] > 0):
                         imagen[i][j][k] = 0
    return imagen
    
def cuadricula(rutaImagen):
    imagen = cv.imread(rutaImagen,1) 
    copia = cv.imread(rutaImagen,1)
    h,w = imagen.shape[:2]
    
    parte1 = imagen[0:int(h/2), 0:int(w/2)]
    parte2 = dejarColorCuadricula(imagen[0:int(h/2), int(w/2):w], 'azul')
    parte3 = dejarColorCuadricula(imagen[int(h/2):h , 0:int(w/2)], 'verde')
    parte4 = dejarColorCuadricula(imagen[int(h/2):h, int(w/2):w], 'rojo')

    copia[0:int(h/2), int(w/2):w] = parte2
    copia[int(h/2):h , 0:int(w/2)] = parte3
    copia[int(h/2):h, int(w/2):w] = parte4
    cv.imshow("Cuadricula",copia)


  
#-------------------------------------------------------------------------------------------------------------------#
foto = "gato.jpg" #Ruta de la imagen

imagenOriginal(foto)
#Primer Punto
dejarColor(foto, 'azul')
dejarColor(foto, 'verde')
dejarColor(foto, 'rojo')
#Segundo Punto
invertirEje(foto, "x")
#Tercer Eje
invertirEje(foto, "y")
#Cuarto Punto
cuadricula(foto)

cv.waitKey(0)
cv.destroyAllWindows()