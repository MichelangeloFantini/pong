import torch
import torch.nn as nn
from processing import DataFrame

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

if __name__ == "__main__":
    main()