import cv2 as cv
import numpy as np
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, \
    QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,\
    QFileDialog, QTabWidget, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont
from functools import partial
import time

conta = conta2 = conta3 = conta4 = conta5 = conta6= conta7 = conta8 = conta9 = conta10 = conta11 = conta12 = conta13 = conta14 = en = 0

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Parcial Daniel Leon')
        self.setGeometry(700, 300, 700, 500)
        self.Lab1 = Window(self)
        self.setCentralWidget(self.Lab1)

class Window(QWidget):
    def __init__(self, *args):
        super(QWidget, self).__init__()

        self.layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        tabs.addTab(tab1, "Linea Izquierda")
        tabs.addTab(tab2, "Liena Central")
        tabs.addTab(tab3, "Linea Derecha")

        tab1.setLayout(self.layOut1())
        tab2.setLayout(self.layOut2())
        tab3.setLayout(self.layOut3())

        self.layout.addWidget(tabs)
        self.setLayout(self.layout)

    def layOut1(self):
        # Frame externo
        outerLayout = QVBoxLayout()

        # Imagen
        self.imagen1 = QLabel()
        self.imagen1.setText('OpenCV Video')
        self.imagen1.setAlignment(QtCore.Qt.AlignCenter)
        self.imagen1.setStyleSheet(
            'border: gray; border-style:solid; border-width: 1px;')

        ## Creamos el Layout inferior ##
        downLayout = QHBoxLayout()
        form = QFormLayout()
        self.spal = QLabel('Small Pallete:')
        self.spal.setFont(QFont('Arial', 11))
        form.addRow(self.spal)
        self.bpal = QLabel('Big Pallete:')
        self.bpal.setFont(QFont('Arial', 11))
        form.addRow(self.bpal)
        self.pbox = QLabel('Plastic Box:')
        self.pbox.setFont(QFont('Arial', 11))
        form.addRow(self.pbox)
        ini = QPushButton('Cargar Iniciar')
        ini.clicked.connect(partial(self.click_imp, 1))
        downLayout.addLayout(form)
        downLayout.addWidget(ini)

        ## Llenamos el layout ##
        outerLayout.addWidget(self.imagen1)
        outerLayout.addLayout(downLayout)
        return outerLayout

    def layOut2(self):
        # Frame externo
        outerLayout = QVBoxLayout()

        # Imagen
        self.imagen2 = QLabel()
        self.imagen2.setText('OpenCV Video')
        self.imagen2.setAlignment(QtCore.Qt.AlignCenter)
        self.imagen2.setStyleSheet(
            'border: gray; border-style:solid; border-width: 1px;')

        ## Creamos el Layout inferior ##
        downLayout = QHBoxLayout()
        grid = QGridLayout()
        self.sbox = QLabel('S-Box:')
        self.sbox.setFont(QFont('Arial', 11))
        grid.addWidget(self.sbox, 0, 0)
        self.mbox = QLabel('M-Box:')
        self.mbox.setFont(QFont('Arial', 11))
        grid.addWidget(self.mbox, 0, 1)
        self.lbox = QLabel('L-Box:')
        self.lbox.setFont(QFont('Arial', 11))
        grid.addWidget(self.lbox, 0, 2)
        self.codi = QLabel('Codigo:')
        self.codi.setFont(QFont('Arial', 11))
        grid.addWidget(self.codi, 1, 0)
        self.cint = QLabel('Cinta:')
        self.cint.setFont(QFont('Arial', 11))
        grid.addWidget(self.cint, 1, 1)
        ini = QPushButton('Cargar Iniciar')
        ini.clicked.connect(partial(self.click_imp, 2))
        downLayout.addLayout(grid)
        downLayout.addWidget(ini)

        ## Llenamos el layout ##
        outerLayout.addWidget(self.imagen2)
        outerLayout.addLayout(downLayout)
        return outerLayout

    def layOut3(self):
        # Frame externo
        outerLayout = QVBoxLayout()

        # Imagen
        self.imagen3 = QLabel()
        self.imagen3.setText('OpenCV Video')
        self.imagen3.setAlignment(QtCore.Qt.AlignCenter)
        self.imagen3.setStyleSheet(
            'border: gray; border-style:solid; border-width: 1px;')

        ## Creamos el Layout inferior ##
        downLayout = QHBoxLayout()
        grid = QGridLayout()
        self.col1 = QLabel('Blue:')
        self.col1.setFont(QFont('Arial', 11))
        grid.addWidget(self.col1, 0, 0)
        self.col2 = QLabel('Green:')
        self.col2.setFont(QFont('Arial', 11))
        grid.addWidget(self.col2, 0, 1)
        self.col3 = QLabel('Metal:')
        self.col3.setFont(QFont('Arial', 11))
        grid.addWidget(self.col3, 0, 2)
        self.ub1 = QLabel('Izquierda:')
        self.ub1.setFont(QFont('Arial', 11))
        grid.addWidget(self.ub1, 1, 0)
        self.ub2 = QLabel('Centro:')
        self.ub2.setFont(QFont('Arial', 11))
        grid.addWidget(self.ub2, 1, 1)
        self.ub3 = QLabel('Derecha:')
        self.ub3.setFont(QFont('Arial', 11))
        grid.addWidget(self.ub3, 1, 2)
        ini = QPushButton('Cargar Iniciar')
        ini.clicked.connect(partial(self.click_imp, 3))
        downLayout.addLayout(grid)
        downLayout.addWidget(ini)

        # Llenamos el layout
        outerLayout.addWidget(self.imagen3)
        outerLayout.addLayout(downLayout)
        return outerLayout

    def click_imp(self, num):
        global en
        filename, _ = QFileDialog.getOpenFileName(self,
                    'Buscar Video', '.', 'Formato (*.mp4)')

        if filename != '':
            capture = cv.VideoCapture(filename)
            while (capture.isOpened()):
                ret, frame = capture.read()

                if (ret == False):
                    break

                if (num == 1):
                    banda1 = frame[150:350, 45:180]
                    frame_gray = cv.cvtColor(banda1, cv.COLOR_BGR2GRAY)
                    h, w = frame_gray.shape
                    ret, frame_binary = cv.threshold(frame_gray, 150, 255, cv.THRESH_BINARY)
                    contours, hierarchy = cv.findContours(
                        frame_binary.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                    h,w = frame_gray.shape
                    img_contours = np.zeros((h,w,3), np.uint8)
                    for cnt in contours:
                        x, y, wc, hc = cv.boundingRect(cnt)
                        self.detec1(x, wc, hc, img_contours, cnt)
                        self.update_image(banda1, self.imagen1)
                    cv.waitKey(1)
                
                if (num == 2):
                    banda2 = frame[100:400,190:340]
                    banda2es = frame[140:250,195:325]
                    frame_gray = cv.cvtColor(banda2es, cv.COLOR_BGR2GRAY)
                    h, w = frame_gray.shape
                    ret, frame_binary = cv.threshold(frame_gray, 180, 255, cv.THRESH_BINARY)
                    contours, hierarchy = cv.findContours(
                        frame_binary.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                    h,w = frame_gray.shape
                    img_contours = np.zeros((h,w,3), np.uint8)
                    if (len(contours) != 2 and len(contours) != 3):
                        for cnt in contours:
                            x, y, wc, hc = cv.boundingRect(cnt)
                            self.detec2(x, wc, hc,img_contours, cnt)
                        cv.waitKey(1)
                    self.update_image(banda2es, self.imagen2)
                
                if (num == 3):
                    banda3 = frame[100:400,350:480]
                    banda3es = frame[100:200,340:470]
                    frame_gray = cv.cvtColor(banda3es, cv.COLOR_BGR2GRAY)
                    h, w = frame_gray.shape
                    ret, frame_binary = cv.threshold(frame_gray, 120, 255, cv.THRESH_BINARY)
                    contours, hierarchy = cv.findContours(
                        frame_binary.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                    h,w = frame_gray.shape
                    img_contours = np.zeros((h,w,3), np.uint8)
                    if (len(contours) != 2):
                        #print(len(contours))
                        for cnt in contours:
                            x, y, wc, hc = cv.boundingRect(cnt)
                            self.detec3(x, wc, hc, img_contours, cnt)
                            self.update_image(banda3es, self.imagen3)
                        cv.waitKey(1)


    def update_image(self, cv_img, wlabel):
        ##
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
        wlabel.setPixmap(QPixmap.fromImage(p))
    
    def detec1(self,x, wc, hc, img_contours, cnt):
        global conta,conta2,conta3
        area = wc*hc
        en1 = 1
        en2 = 1
        en3 = 1
        if (14000<area and area<14200 and en1 == 1):
            en1 = 0
            #cv.drawContours(img_contours, cnt, -1, (255,0,0), 2)
            #cv.imshow('Contornos',img_contours)
            conta = conta + 1
            self.pbox.setText('Plastic Box:'+str(conta))

        # if(3000<area and area<3100):
        #     cv.drawContours(img_contours, cnt, -1, (255,0,0), 2)
        #     cv.imshow('Contornos',img_contours)
        #     conta2 = conta2 + 1
        #     self.bpal.setText('Big Pallete:'+str(conta2))

        if (area > 1400 and area < 2000 and area != 1800):
            en1 = 1
            print(area)
            cv.drawContours(img_contours, cnt, -1, (255,0,0), 2)
            cv.imshow('Contornos',img_contours)
            conta3 = conta3 + 1
            self.spal.setText('Small Pallete:'+str(conta3))
    
    def detec2(self,x, wc, hc, img_contours, cnt):
        global conta4,conta5,conta6,conta7,conta8
        ras1 = wc/hc
        ras2 = hc/wc
        if (ras1 > 1 and ras1 < 1.1):
            print(ras1)
            cv.drawContours(img_contours, cnt, -1, (255,0,0), 2)
            cv.imshow('Contornos',img_contours)
            conta4 = conta4 + 1
            self.sbox.setText('S-Box:'+str(conta4))

        # if(10000<area and area<15000):
        #     conta5 = conta5 + 1
        #     self.mbox.setText('M-Box:'+str(conta5))

        # if(3100<area and area<3300):
        #     conta6 = conta6 + 1
        #     self.lbox.setText('L-Box:'+str(conta6))
    
    def detec3(self,x, wc, hc, img_contours, cnt):
        global conta9,conta10,conta11,conta12,conta13,conta14,en
        ras = float(wc/hc)
        if (ras>0.5 and ras<1.8 and ras != 1 ):
            #print(ras)
            cv.drawContours(img_contours, cnt, -1, (255,0,0), 2)
            cv.imshow('Contornos',img_contours)
            if (x < 30):
                en = 0
                conta9 = conta9 + 1
                self.ub1.setText('Izquierda: '+str(conta9))
            if (x<60 and x>30):
                en = 0
                conta10 = conta10 + 1
                self.ub2.setText('Centro: '+str(conta10))
            if (x>60):
                en = 0
                conta11 = conta11 + 1
                self.ub3.setText('Derecha: '+str(conta11))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())