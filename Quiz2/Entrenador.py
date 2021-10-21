import numpy as np
import xlrd

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split #Coja cierta cantidad de muestras para entrenar y testear
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn import preprocessing

import joblib

#Abro el libro desde el cual voy a leer
book_excel= xlrd.open_workbook("Letras10.xlsx")

#Creamos una función
def load_xlsx(book):
    sh = book.sheet_by_index(0) #Le pasamos la hoja
    #De aquí sale la matriz de características
    x = np.zeros((sh.nrows,sh.ncols-1)) ##Le quito una columna, ahí está la clase
    y = []

    for i in range(0,sh.nrows):
        for j in range(0,sh.ncols-1):
            #Lleno el vector, desde la fila 1 y la columna 2
            x[i,j] = sh.cell_value(rowx=i,colx=j+1)
        
        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'T'): #Lleva las comillas porque es un string
            y.append(0)

        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'R'): #Lleva las comillas porque es un string
            y.append(1)

        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'A'): #Lleva las comillas porque es un string
            y.append(2)
        
        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'E'): #Lleva las comillas porque es un string
            y.append(3)

        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'S'): #Lleva las comillas porque es un string
            y.append(4)

        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'I'): #Lleva las comillas porque es un string
            y.append(5)

        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'G'): #Lleva las comillas porque es un string
            y.append(6)

        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'C'): #Lleva las comillas porque es un string
            y.append(7)

        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'D'): #Lleva las comillas porque es un string
            y.append(8)

        #Relleno el vector y
        if(sh.cell_value(rowx=i,colx=0) == 'Z'): #Lleva las comillas porque es un string
            y.append(9)

    #Llenamos y como un array de las clases que encontramos
    y = np.array(y, np.float32) #Las maquinas trabajan con floats

    return x,y

if __name__=='__main__':
    #X, Y toman los valores de x, y
    X,Y = load_xlsx(book_excel)

    #Normalización
    model_ssc = StandardScaler()
    X_SS = model_ssc.fit_transform(X)
    #print(X_SS)

    util = [0]*4
    utilacc = [0]*4
    a=0
    VecFunc = ['tanh',  'relu']
    VecLayer = [10, (10, 50)]
    for i in VecFunc:
        capas = 0
        for j in VecLayer:
            modelslist = [0]*10
            accuracy = [0]*10
            capas = capas + 1
            print('Realizando modelo MLP con funcion ' + i + ' y ' + str(capas) + ' capas ocultas de ' + str(j) + ' neuronas')
            for k in range(0,5):
                #Separo datos en entrenamiento y testeo
                #Separa las muestras X, Y en sample y response. El 70% es train y el 30% es test
                sample_train, sample_test, response_train, response_test = train_test_split(X_SS,Y,test_size = 0.3)
                
                #Características del modelo
                model_mlpc = MLPClassifier(activation = i, hidden_layer_sizes = (j), max_iter= 5000, tol = 0.0001)
                model_mlpc.fit(sample_train, response_train)
                modelslist[k] = model_mlpc
                response_predict = model_mlpc.predict(sample_test)
                accuracy[k] = accuracy_score(response_test, response_predict)
                #print(i+" "+str(j)+" "+str(accuracy[k]))
                #print(modelslist[i])
    
            utilpos = accuracy.index(max(accuracy))
            util[a] = modelslist[utilpos]
            utilacc[a] = accuracy[utilpos]
            a = a+1
            print('Precision del ' + str(int(accuracy[utilpos]*100))+ '%')

    utilpos2 = utilacc.index(max(utilacc))
    print('Se guardo el modelo '+ str(util[utilpos2]) + ' con precision del ' + str(int(utilacc[utilpos2]*100)) + '%')


    joblib.dump(model_ssc,'model_ssc.pkl')
    joblib.dump(util[utilpos2],'model_mlpc.pkl')