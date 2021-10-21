import numpy as np
import xlrd

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split #Coja cierta cantidad de muestras para entrenar y testear
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold

import joblib  


#Abro el libro desde el cual voy a leer
book_excel= xlrd.open_workbook("DataNumsTodos.xlsx")

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

        #Relleno el vector y, y le digo que si el valor es 0 y entiende que es la clase 0
        if(sh.cell_value(rowx=i,colx=0) == '0'): #Lleva las comillas porque es un string
            y.append (0)
        
        #Relleno el vector y, y le digo que si el valor es 2 y entiende que es la clase 1
        if(sh.cell_value(rowx=i,colx=0) == '1'): #Lleva las comillas porque es un string
            y.append (1)

        #Relleno el vector y, y le digo que si el valor es 4 y entiende que es la clase 2
        if(sh.cell_value(rowx=i,colx=0) == '2'): #Lleva las comillas porque es un string
            y.append (2)

        #Relleno el vector y, y le digo que si el valor es 6 y entiende que es la clase 3
        if(sh.cell_value(rowx=i,colx=0) == '3'): #Lleva las comillas porque es un string
            y.append (3)
        
        #Relleno el vector y, y le digo que si el valor es 8 y entiende que es la clase 4
        if(sh.cell_value(rowx=i,colx=0) == '4'): #Lleva las comillas porque es un string
            y.append (4)
        
        if(sh.cell_value(rowx=i,colx=0) == '5'): #Lleva las comillas porque es un string
            y.append (5)
        
        #Relleno el vector y, y le digo que si el valor es 2 y entiende que es la clase 1
        if(sh.cell_value(rowx=i,colx=0) == '6'): #Lleva las comillas porque es un string
            y.append (6)

        #Relleno el vector y, y le digo que si el valor es 4 y entiende que es la clase 2
        if(sh.cell_value(rowx=i,colx=0) == '7'): #Lleva las comillas porque es un string
            y.append (7)

        #Relleno el vector y, y le digo que si el valor es 6 y entiende que es la clase 3
        if(sh.cell_value(rowx=i,colx=0) == '8'): #Lleva las comillas porque es un string
            y.append (8)
        
        #Relleno el vector y, y le digo que si el valor es 8 y entiende que es la clase 4
        if(sh.cell_value(rowx=i,colx=0) == '9'): #Lleva las comillas porque es un string
            y.append (9)
    
    #Llenamos y como un array de las clases que encontramos
    y = np.array(y, np.float32) #Las maquinas trabajan con floats

    return x,y

if __name__=='__main__':
    #X, Y toman los valores de x, y
    X,Y = load_xlsx(book_excel)
    
    
    sel = VarianceThreshold(threshold=(.6 * (1 - .6)))
    #X_VT = sel.fit_transform(X)


    #Normalización
    model_ssc = StandardScaler()
    X_SS = model_ssc.fit_transform(X)
    #print(X_SS)

    modelslist = [0]*10
    accuracy = [0]*10
    for i in range(0,10):
        #Separo datos en entrenamiento y testeo
        #Separa las muestras X, Y en sample y response. El 70% es train y el 30% es test
        sample_train, sample_test, response_train, response_test = train_test_split(X_SS,Y,test_size = 0.3)
        
        #Características del modelo
        model_mlpc = MLPClassifier(activation = "relu", hidden_layer_sizes = (50,), max_iter= 500, tol =0.0001)
        model_mlpc.fit(sample_train, response_train)
        modelslist[i] = model_mlpc
        response_predict = model_mlpc.predict(sample_test)
        accuracy[i] = accuracy_score(response_test, response_predict)
        print(accuracy[i])
        #print(modelslist[i])
    
    util = accuracy.index(max(accuracy))
    print('Se guardo el modelo '+ str(util + 1 ))
        

joblib.dump(model_ssc,'model_ssc.pkl')
joblib.dump(modelslist[util],'model_mlpc.pkl')

#Guardo el modelo (Todo lo que tenga .fit)


        