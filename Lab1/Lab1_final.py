import cv2 as cv
import numpy as np
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QFormLayout, QLabel, \
    QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, \
    QFileDialog,QTabWidget,QMainWindow
from PyQt5.QtGui import QIcon, QPixmap,QImage

x1=y1=0
vec1=[]
vec2=[]


def mouseClick(event,x,y,flags,param):
    global x1,y1,vec1,vec2

    if(event == cv.EVENT_LBUTTONDOWN):
        x1 = x
        y1 = y

    if (x1!=0 and y1!=0):
        vec1.append(x1)
        vec2.append(y1) 

    x1=y1=0
    return vec1        

def nothing(x):
    pass

def binaryThreshold(imgGray,u1,u2):
    imgGray1= imgGray.copy()
    h,w = imgGray1.shape[:2]
    u = np.array([abs(u1),abs(u2)])
    u1 = np.amin(u)
    u2 = np.amax(u)
    for i in range(h):
        for j in range(w):
            if ((imgGray1[i][j] <= u1) or (imgGray1[i][j] >= u2)):
                imgGray1[i][j] = 0
            else:
                imgGray1[i][j] = 255
    return imgGray1


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Laboratorio 1')
        self.setGeometry(700,300,500,500)
        
        self.Lab1 = Window(self)
        self.setCentralWidget(self.Lab1)
        

class Window(QWidget):
    def __init__(self, parent):
        super(QWidget,self).__init__(parent)

        self.layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()

        tabs.addTab(tab1,"Punto 1")
        tabs.addTab(tab2,"Punto 2")

        tab1.setLayout(self.layOut1())
        tab2.setLayout(self.layOut2())

        self.layout.addWidget(tabs)
        self.setLayout(self.layout)

    def pintar(self,imgB,orig,color):
        #cv.imshow('aa',orig)
        h,w = imgB.shape[:2]
        #Azul
        if (color == 0):
            for i in range(0,h):
                for j in range(0,w):
                    if (imgB[i,j] == 255):
                        orig[i,j] = (255,0,0)
        

        
        #Verde
        if (color == 1):
            for i in range(0,h):
                for j in range(0,w):
                    if (imgB[i,j] == 255):
                        orig[i,j] = (0,255,0)
       
        

        #Rojo
        if (color == 2):
            for i in range(0,h):
                for j in range(0,w):
                    if (imgB[i,j] == 255):
                        orig[i,j] = (0,0,255)
        
        
        #Amarillo
        if (color == 3):
            for i in range(0,h):
                for j in range(0,w):
                    if (imgB[i][j] == 255):
                        orig[i][j] = (0,255,255)
        

        return orig


    def layOut1(self):
        # Frame externo

        outerLayout = QVBoxLayout()

        # Imagen
        self.imagenL = QLabel()
        self.imagenL.setText('OpenCV Image')
        self.imagenL.setAlignment(QtCore.Qt.AlignCenter)
        self.imagenL.setStyleSheet('border: gray; border-style:solid; border-width: 1px;')

        # Creamos el boton de cargar

        imp = QPushButton('Cargar Imagen')
        imp.clicked.connect(self.click_imp)

        # Tags

        tags = QFormLayout()
        self.et1 = QLineEdit()
        self.et2 = QLineEdit()
        self.et3 = QLineEdit()
        self.et4 = QLineEdit()
        bt1 = QPushButton('Actualizar Anotaciones')
        tags.addRow('Etiqueta 1:', self.et1)
        tags.addRow('Etiqueta 2:', self.et2)
        tags.addRow('Etiqueta 3:', self.et3)
        tags.addRow('Etiqueta 4:', self.et4)
        tags.addRow(bt1)
        bt1.clicked.connect(self.click_bt1)

        # Llenamos el layout

        outerLayout.addWidget(imp)
        outerLayout.addWidget(self.imagenL)
        outerLayout.addLayout(tags)

        return outerLayout
    
    def layOut2(self):
        # Frame externo
        outerLayout = QVBoxLayout()

        #Boton de importar Tab2
        imp2 = QPushButton('Cargar Imagen')
        imp2.clicked.connect(self.click_imp2)

        #Creo las etiquetas de las dos imagenes del Tab2
        imagenes = QHBoxLayout()
        self.imagenO = QLabel()
        self.imagenO.setText('Imagen Original')
        self.imagenO.setAlignment(QtCore.Qt.AlignCenter)
        self.imagenO.setStyleSheet('border: gray; border-style:solid; border-width: 1px;')
        self.imagenMod = QLabel()
        self.imagenMod.setText('Imagen Alterada')
        self.imagenMod.setAlignment(QtCore.Qt.AlignCenter)
        self.imagenMod.setStyleSheet('border: gray; border-style:solid; border-width: 1px;')
        imagenes.addWidget(self.imagenO)
        imagenes.addWidget(self.imagenMod)

        #Creo los botones de colores
        botones = QHBoxLayout()
        b1 = QPushButton('Azul')
        b1.setStyleSheet("background-color : blue")
        b1.clicked.connect(self.blue)
        b2 = QPushButton('Verde')
        b2.setStyleSheet("background-color : green")
        b2.clicked.connect(self.green)
        b3 = QPushButton('Amarillo')
        b3.setStyleSheet("background-color : yellow")
        b3.clicked.connect(self.yellow)
        b4 = QPushButton('Rojo')
        b4.setStyleSheet("background-color : red")
        b4.clicked.connect(self.red)
        botones.addWidget(b1)
        botones.addWidget(b2)
        botones.addWidget(b3)
        botones.addWidget(b4)

        #Organizamos el layout exterior
        outerLayout.addWidget(imp2)
        outerLayout.addLayout(imagenes)
        outerLayout.addLayout(botones)

        return outerLayout

    def click_bt1(self):
        global vec1,vec2
        vec = [self.et1.text(),self.et2.text(),self.et3.text(),self.et4.text()]
        img=self.added.copy()
        h,w = img.shape[:2]
        for i in range(0,len(vec1)):
            if (vec1[i]+200 > w/2):
                cv.arrowedLine(img,(vec1[i]+200,vec2[i]),(w-65,vec2[i]-20),(0,0,255),2,2,0,0.1)
                cv.putText(img,vec[i],(w-80,vec2[i]-30),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2,cv.LINE_AA)
            else:
                cv.arrowedLine(img,(vec1[i]+200,vec2[i]),(65,vec2[i]-20),(0,0,255),2,2,0,0.1)
                cv.putText(img,vec[i],(25,vec2[i]-30),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2,cv.LINE_AA)
        self.mostrarImagen(img,self.imagenL)
        return 0
        
    def click_imp(self):
        (filename, _) = QFileDialog.getOpenFileName(self,
                'Buscar Imagen', '.', 'Formato (*.png *.jpg *.jpeg)')
        imagTo = cv.imread(filename, 1)
        cv.namedWindow("Marcar")
        cv.setMouseCallback("Marcar",mouseClick)
        cv.imshow("Marcar",imagTo)
        cv.waitKey(0)
        self.added = self.extendImag(imagTo,200)
        copy = self.etiquetas(self.added.copy())
        self.mostrarImagen(copy,self.imagenL)
        return 0

    def click_imp2(self):
        (filename, _) = QFileDialog.getOpenFileName(self,
                'Buscar Imagen', '.', 'Formato (*.png *.jpg *.jpeg)')
        self.tree = cv.imread(filename, 1)
        self.treeB = cv.imread(filename,0)
        self.mostrarImagen(self.tree,self.imagenO)

    def mostrarImagen(self, imag, wimag):
        size = imag.shape
        step = imag.size / size[0]
        qformat = QImage.Format_Indexed8

        if len(size) == 3:
            if size[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        imgL = QImage(imag, size[1], size[0], step, qformat)
        imgL = imgL.rgbSwapped()

        wimag.setPixmap(QPixmap.fromImage(imgL))
        #self.resize(self.imagen.pixmap().size())
    
    def etiquetas(self,img):
        #creo una funcion que me ubique lineas y numeros desde el punto que empezo hasta la zona que se extendio la imagen
        global vec1,vec2
        h,w = img.shape[:2]
        for i in range(0,len(vec1)):
            if (vec1[i]+200 > w/2):
                #se crea la flecha y el texto en la punta
                cv.arrowedLine(img,(vec1[i]+200,vec2[i]),(w-95,vec2[i]),(0,0,255),2,1,0,0.1)
                cv.putText(img,str(i+1),(w-80,vec2[i]),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2,cv.LINE_AA)
            else:
                cv.arrowedLine(img,(vec1[i]+200,vec2[i]),(95,vec2[i]),(0,0,255),2,1,0,0.1)
                cv.putText(img,str(i+1),(45,vec2[i]),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2,cv.LINE_AA)
        return img
    
    def extendImag(self,img,u):
        #Agrega la imagen negra a los laterales de la original
        h,w = img.shape[:2]
        imgAdd = self.createBlank(u,h)
        bimage = cv.hconcat([imgAdd,img,imgAdd])
        return bimage

    def createBlank(self,valX,valY):
        #Crea una imagen en zeros para agregar a los lados
        add = np.zeros((valY, valX, 3), np.uint8)
        return add

    def blue(self):
        self.copyblue=self.treeB.copy()

        #Empezar mostrando ventana 
        cv.namedWindow("Binarizar Azul")
        cv.createTrackbar("u1","Binarizar Azul",0,255,nothing)
        cv.createTrackbar("u2","Binarizar Azul",0,255,nothing)
        
        #Evento TrackBar y flag para salir del ciclo infinito
        flag = 1
        while (flag):
            u1 = cv.getTrackbarPos("u1","Binarizar Azul")
            u2 = cv.getTrackbarPos("u2","Binarizar Azul")
            self.imgBinary = binaryThreshold(self.copyblue,u1,u2)
            cv.imshow('Binarizar Azul',self.imgBinary)
            k = cv.waitKey(1)
            if (k != -1):
                flag = 0
                cv.destroyAllWindows()
        
        #multi=cv.addWeighted(copy,0.2,self.tree.copy(),0.8,0)
        #cv.imshow('aa',imgBinary)
        self.pintada = self.pintar(self.imgBinary,self.tree,0)
        self.mostrarImagen(self.pintada,self.imagenMod)
        return 0
    
    def red(self):
        self.copyblue=self.treeB.copy()

        #Empezar mostrando ventana 
        cv.namedWindow("Binarizar Rojo")
        cv.createTrackbar("u1","Binarizar Rojo",0,255,nothing)
        cv.createTrackbar("u2","Binarizar Rojo",0,255,nothing)
        
        #Evento TrackBar y flag para salir del ciclo infinito
        flag = 1
        while (flag):
            u1 = cv.getTrackbarPos("u1","Binarizar Rojo")
            u2 = cv.getTrackbarPos("u2","Binarizar Rojo")
            self.imgBinary = binaryThreshold(self.copyblue,u1,u2)
            cv.imshow('Binarizar Rojo',self.imgBinary)
            k = cv.waitKey(1)
            if (k != -1):
                flag = 0
                cv.destroyAllWindows()
        
        #multi=cv.addWeighted(copy,0.2,self.tree.copy(),0.8,0)
        #cv.imshow('aa',imgBinary)
        self.pintada = self.pintar(self.imgBinary,self.tree,2)
        self.mostrarImagen(self.pintada,self.imagenMod)
        return 0
    
    def green(self):
        self.copyblue=self.treeB.copy()

        #Empezar mostrando ventana 
        cv.namedWindow("Binarizar Verde")
        cv.createTrackbar("u1","Binarizar Verde",0,255,nothing)
        cv.createTrackbar("u2","Binarizar Verde",0,255,nothing)
        
        #Evento TrackBar y flag para salir del ciclo infinito
        flag = 1
        while (flag):
            u1 = cv.getTrackbarPos("u1","Binarizar Verde")
            u2 = cv.getTrackbarPos("u2","Binarizar Verde")
            self.imgBinary = binaryThreshold(self.copyblue,u1,u2)
            cv.imshow('Binarizar Verde',self.imgBinary)
            k = cv.waitKey(1)
            if (k != -1):
                flag = 0
                cv.destroyAllWindows()
        
        #multi=cv.addWeighted(copy,0.2,self.tree.copy(),0.8,0)
        #cv.imshow('aa',imgBinary)
        self.pintada = self.pintar(self.imgBinary,self.tree,1)
        self.mostrarImagen(self.pintada,self.imagenMod)
        return 0

    def yellow(self):
        self.copyblue=self.treeB.copy()

        #Empezar mostrando ventana 
        cv.namedWindow("Binarizar Amarillo")
        cv.createTrackbar("u1","Binarizar Amarillo",0,255,nothing)
        cv.createTrackbar("u2","Binarizar Amarillo",0,255,nothing)
        
        #Evento TrackBar y flag para salir del ciclo infinito
        flag = 1
        while (flag):
            u1 = cv.getTrackbarPos("u1","Binarizar Amarillo")
            u2 = cv.getTrackbarPos("u2","Binarizar Amarillo")
            self.imgBinary = binaryThreshold(self.copyblue,u1,u2)
            cv.imshow('Binarizar Amarillo',self.imgBinary)
            k = cv.waitKey(1)
            if (k != -1):
                flag = 0
                cv.destroyAllWindows()
        
        #multi=cv.addWeighted(copy,0.2,self.tree.copy(),0.8,0)
        #cv.imshow('aa',imgBinary)
        self.pintada = self.pintar(self.imgBinary,self.tree,3)
        self.mostrarImagen(self.pintada,self.imagenMod)
        return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())