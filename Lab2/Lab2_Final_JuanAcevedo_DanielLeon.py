## Laboratorio 2 por Daniel Felipe León Gualdrón y Juan Esteban Acevedo Sánchez ##
#____________Librerias________________#
import cv2 as cv
import numpy as np
import time
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QFormLayout, QLabel, \
    QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, \
    QFileDialog,QTabWidget,QMainWindow, QGridLayout,QMessageBox
from PyQt5.QtGui import QIcon, QPixmap,QImage,QFont

#____________Variables________________#
# Contadores #
en = 1
a1 = 0
a2 = 0
a3 = 0
a4 = 0
a5 = 0
a6 = 0
b8 = 0

## Iniciamos los habilitadores ##
en1 = 1
en2 = 1
en3 = 1
en4 = 1
en5 = 1
en6 = 1

#____________Funciones________________#

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Laboratorio 2')
        self.setGeometry(500,300,800,500)
        
        self.Lab1 = Window(self)
        self.setCentralWidget(self.Lab1)

## Intefaz ##
class Window(QWidget):
    def __init__(self, parent):
        super(QWidget,self).__init__(parent)

        self.layout = QVBoxLayout(self)

        # Imagen
        self.imagenL = QLabel()
        self.imagenL.setText('OpenCV Video')
        self.imagenL.setAlignment(QtCore.Qt.AlignCenter)
        self.imagenL.setStyleSheet('border: gray; border-style:solid; border-width: 1px;')

        # Etiquetas
        inferior = QHBoxLayout(self)
        grid = QGridLayout(self)
        bolas = QLabel('Cantidad de bolas por agujero')
        bolas.setFont(QFont('Arial', 15))
        grid.addWidget(bolas, 0, 0, 1, 3)
        self.ag1 = QLabel('Agujero 1:')
        self.ag1.setFont(QFont('Arial', 13))
        grid.addWidget(self.ag1, 1, 0)
        self.ag2 = QLabel('Agujero 2:')
        self.ag2.setFont(QFont('Arial', 13))
        grid.addWidget(self.ag2, 1, 1)
        self.ag3 = QLabel('Agujero 3:')
        self.ag3.setFont(QFont('Arial', 13))
        grid.addWidget(self.ag3, 1, 2)
        self.ag4 = QLabel('Agujero 4:')
        self.ag4.setFont(QFont('Arial', 13))
        grid.addWidget(self.ag4, 2, 0)
        self.ag5 = QLabel('Agujero 5:')
        self.ag5.setFont(QFont('Arial', 13))
        grid.addWidget(self.ag5, 2, 1)
        self.ag6 = QLabel('Agujero 6:')
        self.ag6.setFont(QFont('Arial', 13))
        grid.addWidget(self.ag6, 2, 2)
        self.bola8 = QLabel()
        self.bola8.setFont(QFont('Arial', 15))
        grid.addWidget(self.bola8, 3, 0, 1, 3)
        self.wbola8 = QLabel()
        self.wbola8.setFont(QFont('Arial', 15))
        grid.addWidget(self.wbola8, 4, 0, 1, 3)

        #Boton de iniciar
        iniciar = QPushButton('Iniciar reconocimiento')
        iniciar.clicked.connect(self.click_imp)
        inferior.addLayout(grid)
        inferior.addWidget(iniciar)

        self.layout.addWidget(self.imagenL)
        self.layout.addLayout(inferior)
        self.setLayout(self.layout)

    def click_imp(self):
    	global en1, en2, en3, en4, en5, en6

    	(filename, _) = QFileDialog.getOpenFileName(self,
    		'Buscar Video', '.', 'Formato (*.mp4 )')

    	if filename != '':

        	capture = cv.VideoCapture(filename)

        	while (capture.isOpened()):
        		ret, frame = capture.read()
        		
        		if (ret == False):
        			break

        		self.update_image(frame)
        		agujero1 = self.procImagen(frame,10,35,15,35, "agujero1",0,135,240, en1)
        		agujero2 = self.procImagen(frame,2,28,311,343, "agujero2",2, 150, 240, en2)
        		agujero3 = self.procImagen(frame,10,35,620,640, "agujero3",0,110,240, en3)
        		agujero4 = self.procImagen(frame,300,326,15,41, "agujero4",0,120,240, en4)
        		agujero5 = self.procImagen(frame,308,339,311,343, "agujero5",2,135,240, en5)
        		agujero6 = self.procImagen(frame,300,321,615,636, "agujero6",1,120,240, en6)

        		cv.waitKey(1)
    
    def update_image(self, cv_img):
        # 
        qt_img = self.convert_cv_qt(cv_img)
        self.imagenL.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 500, QtCore.Qt.KeepAspectRatio)
        
        return QPixmap.fromImage(p)

    def procImagen(self,imagen, y1, y2, x1, x2, t,n, inf, sup, hab):

	    global en, a1, a2, a3, a4, a5, a6, b8, en1, en2, en3, en4, en5, en6
	    en = hab
	    ## ROI ##
	    im = imagen[y1:y2,x1:x2]

	    ## Binarizacion Bimodal ##
	    gray = cv.cvtColor (im, cv.COLOR_BGR2GRAY)
	    ret1, frame_binary1 = cv.threshold(gray, inf, 255, cv.THRESH_BINARY)
	    ret2, frame_binary2 = cv.threshold(gray, sup, 255, cv.THRESH_BINARY)
	    imgn = cv.absdiff(frame_binary1,frame_binary2)
	    
	    im = cv.resize(imgn, (160,160))
	    
	    ## Deteccion de contornos ##
	    contours, hierarchy = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
	    img = np.zeros((160,160,3), np.uint8)

	    ## Cambio de los habilitadores ##
	    if (len(contours)<= n):
	        if (t == "agujero1"):
	            en1 = 1
	            
	        if (t == "agujero2"):
	            en2 = 1
	            
	        if (t == "agujero3"):
	            en3 = 1
	            
	        if (t == "agujero4"):
	            en4 = 1
	            
	        if (t == "agujero5"):
	            en5 = 1
	            
	        if (t == "agujero6"):
	            en6 = 1
	            
	    for cnt in contours:
	        x, y, wc, hc = cv.boundingRect(cnt)
	        area = wc*hc
	        
	        if (wc/hc == 2.4642857142857144 ):
	        	self.bola8.setText("El Juego Ha Terminado")
	        	self.wbola8.setText("La bola 8 entro por el "+ t)
	        	en = 0
	        	b8 = 1
	        
	        if (wc/hc >= 0.908 and wc/hc < 1.169 and en == 1 and wc/hc != 1.0810810810810811 and b8 == 0):
	            if (wc/hc == 1 and hc/wc == 1):
	                en = 0
	            else:
	                if (t == "agujero1"):
	                    en1 = 0
	                    a1 = a1+1
	                    self.ag1.setText("Agujero 1: " + str(a1))
	                    
	                if (t == "agujero2"):
	                    en2 = 0
	                    a2 = a2+1
	                    self.ag2.setText("Agujero 2: " + str(a2))
	                    
	                if (t == "agujero3"):
	                    en3 = 0
	                    a3 = a3+1
	                    self.ag3.setText("Agujero 3: " + str(a3))
	                    
	                if (t == "agujero4"):
	                    en4 = 0
	                    a4 = a4+1
	                    self.ag4.setText("Agujero 4: " + str(a4))
	                    

	                if (t == "agujero5"):
	                    en5 = 0
	                    a5 = a5+1
	                    self.ag5.setText("Agujero 5: " + str(a5))
	                    

	                if (t == "agujero6"):
	                    en6 = 0
	                    a6 = a6+1
	                    self.ag6.setText("Agujero 6: " + str(a6))
	                            
	        cv.drawContours(img, cnt, -1, (255,0,0), 2)

	    return img
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())