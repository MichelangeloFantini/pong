import torch
import torch.nn as nn
from processing import DataFrame
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScalar


class DataLoader():
    def __init__():
        data = DataFrame("data.pkl")
        data.decode_data(save_data=False)
        data.classify_actions()
        Final = data.assemble_train_data()
        Final = data.standardize(Final)
        print(Final)
        X = data.iloc[1:5]
        y = data.iloc[6]
        return X, y

class Net(nn.Module):
    # Constructor
    def __init__(self, D_in):
        super(Net, self).__init__()
        #self.drop = nn.Dropout(p=p)
        self.linear1 = nn.Linear(D_in, 4)
        self.linear2 = nn.Linear(4, 1)
    def forward(self,x):
        x = torch.relu(x.linear1(x))
        x = torch.sigmoid(x.linear2(x))
        return x
        



def main():
    X,y = DataLoader()
    print(X)
    model = Net()
    n_samples, n_features = X.shape
    X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size= 0.2)

    sc = StandardScalar() # all the features will have zero mean and unit variance
    X_train = sc.fit_transfor(X_train)
    y_train = sc.fit_transfor(y_train)

    X_train = torch.from_numpy(X_train.astype(np.float32))
    # do this for all of them to make data into tensor
    y_train = y_train.view(y_train.shape[0],1)
    y_test = y_test.view(y_test.shape[0],1)

if __name__ == "__main__":
    main()