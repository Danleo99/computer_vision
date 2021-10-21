import numpy as np
import xlrd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

book_excel = xlrd.open_workbook("DataNumsPairs.xlsx")


def load_xlsx(book):
    sh = book.sheet_by_index(0)
    x = np.zeros((sh.nrows, sh.ncols-1))
    y = []

    for i in range(0, sh.nrows):
        for j in range(0, sh.ncols-1):
            x[i, j] = sh.cell_value(rowx=i, colx=j+1)
        if(sh.cell_value(rowx=i, colx=0) == '0'):
            y.append(0)
        if(sh.cell_value(rowx=i, colx=0) == '2'):
            y.append(1)
        if(sh.cell_value(rowx=i, colx=0) == '4'):
            y.append(2)
        if(sh.cell_value(rowx=i, colx=0) == '6'):
            y.append(3)
        if(sh.cell_value(rowx=i, colx=0) == '8'):
            y.append(4)

    y = np.array(y, np.float32)
    return x, y


if __name__ == '__main__':
    X, Y = load_xlsx(book_excel)
    print(len(X), len(Y))

    model_ss = StandardScaler()
    X_SS = model_ss.fit_transform(X)

    for i in range(0, 10):
        sample_train, sample_test, response_train, response_test = train_test_split(
            X_SS, Y, test_size=0.3)

        model_mlp = MLPClassifier(
            activation='relu', hidden_layer_sizes=(50,), max_iter=1000, tol=0.0001)

        model_mlp.fit(sample_train, response_train)

        response_predict = model_mlp.predict(sample_test)
        accuracy = accuracy_score(response_test, response_predict)
        print(accuracy)
    
    joblib.dump(model_mlp, 'model_mlp.pkl')
    joblib.dump(model_ss, 'model_ss.pkl')
    
