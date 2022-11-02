#Computer controlled pad is on the left
import pandas as pd
import numpy as np
class DataFrame():
    def __init__(self,dataframe_address):
        #"data.pkl"
        self.data = pd.read_pickle(dataframe_address)

    def decode_data(self,save_data=True):
#df.to_csv("data.csv")
        prev= self.data["ball"][0][0]
        l=[np.nan]
        lx= [np.nan]
        ly = [np.nan]
        for x in self.data["ball"][1:]:
            #determine if ball is moving left or right
            lx.append(x[0])
            ly.append(x[1])
            if x == (212.5, 132.5):
                l.append(np.nan)
            elif x[0] > prev:
                l.append(True)
            else:
                l.append(False)
            prev = x[0]
        self.data["ball moving to right"] = l
        self.data["ball x"] = lx
        self.data["ball y"] = ly


        for i in range(0,self.data.shape[0]):
            #store only y coord of the pad, as it is not moving on x axis
            self.data["my pad"][i]= self.data["my pad"][i][1]
            self.data["comp pad"][i]= self.data["comp pad"][i][1]


        l=[np.nan]
        prev= self.data["my pad"][0]

        for x in self.data["my pad"][1:]:
            #check determine if my_pad is moving up or down
            if x > prev:
                l.append("up")
            else:
                l.append("down")
            prev=x
        self.data["my dir"] = l

        l=[np.nan]
        prev= self.data["comp pad"][0]

        for x in self.data["comp pad"][1:]:
            #check if computer pad is going up or down
            if x > prev:
                l.append("up")
            else:
                l.append("down")
            prev=x
        self.data["comp dir"] = l
        self.data = self.data.dropna()
        self.data = self.data.reset_index()   
        #print(df)
        if save_data:
            self.data.to_csv("processed_data.csv")

#________________________________________________________
#NOW THE MORE COMPLICATED STUFF

#when is a good action
# -> when hit ball back 
# -> when score point 

#I want algo to learn from these two situations
#I will split the data into chunks of "good actions"

#1 when does player do good action?
# when ball is travelling right and then it switches direction...
#2 computer does good action also when there is change in direction (ball going to left now goes to right) without any point scored

#split data into chunks based on chnage in direction
    def classify_actions(self):
        L =[]
        prev_direction = not self.data['ball moving to right'][0]
        prev_score = self.data["score"][0]
        for ind in range(self.data.shape[0]): #for each row in the dataframe
            row=self.data.iloc[ind,:]
            if row['ball moving to right']!=prev_direction or prev_score != row["score"]:
                #create a new dataframe and append it to L
                exec(f"df_{ind}=pd.DataFrame([self.data.iloc[{ind},:]])")
                exec(f"L.append(df_{ind})")
                #exec(f"print(df_{row['index']} )")
            elif row['ball moving to right']==prev_direction:
                #pop the most current daframe and add elements to it
                temp = L.pop()
                new = pd.DataFrame([self.data.iloc[ind,:]])
                temp = pd.concat([temp,new])
                #print(temp)
                L.append(temp)


            prev_direction = row['ball moving to right']
            prev_score = row["score"]
        #print(len(L))
        for i in range(len(L)-1):
            df = L[i]
            #print(i)
            #print(L[i+1]["score"].values[0])
            if df["score"].values[0]!=L[i+1]["score"].values[0]:
                #if the score of the df is differet than the next one a goal was scored if last direction was right-> comp has scored, otherwise human scored
               
                if df["ball moving to right"].values[0]:
                #comp scored
                 #the last action from robot was especially good
                    df["score type"]= [0]*df.shape[0]
                    df = L[i-1]
                    df["score type"]= [1]*df.shape[0]
                else:
                    #human scored -> bad action from computer
                    df["score type"]= [0]*df.shape[0]
                    df = L[i-1]
                    df["score type"]= [2]*df.shape[0]
            else:
                df["score type"]= [0]*df.shape[0]      
        self.action_list = L             
#print(L)

#--------------------------------------------
#now is time to assemble a final data to train the neuro net

#if label is zero-> check the direction the ball is moving
#-> right (True) for now: don't do anything
#                for later: change my pad and comp pad
# 
#-> left (False) it means the robot hit the ball back -> learn from that

#if label is 1-> comp scored, keep everything as is
#if label is 2 -> i scored, don't learn from it

#IDEA for future. Give different scenarios different weights.
    def assemble_train_data(self):
        self.action_list = self.action_list[:len(self.action_list)-1]
        Final = self.action_list[0]
        for df in self.action_list[1:]: 
            if df["score type"].values[0]==0:
                if df["ball moving to right"].values[0]:
                    pass
                    # col_list = list(df)
                    # col_list[1], col_list[2] = col_list[2], col_list[1]
                    # col_list[6], col_list[7] = col_list[7], col_list[6]
                    # df.columns = col_list
                    # Final = pd.concat([Final,df],ignore_index=True)
                else:
                    Final = pd.concat([Final,df],ignore_index=True)
            elif df["score type"].values[0]==1:
                Final = pd.concat([Final,df],ignore_index=True)
            elif df["score type"].values[0]==2:
                pass
                # col_list = list(df)
                # col_list[1], col_list[2] = col_list[2], col_list[1]
                # col_list[6], col_list[7] = col_list[7], col_list[6]
                # df.columns = col_list
                # Final = pd.concat([Final,df],ignore_index=True)
            else:
                print("Error")
            #print(Final.shape)
        Final = Final.drop(['index', 'score','ball moving to right','score type','comp dir',"ball"],axis=1)
        return Final

    def standardize(self,final):
        final["my pad"] = final["my pad"]/280
        final["comp pad"] = final["comp pad"]/280
        final["ball x"] = final["ball x"]/440
        final["ball y"] = final["ball y"]/280
        return final

        

def main():
    data = DataFrame("data.pkl")
    data.decode_data(save_data=False)
    data.classify_actions()
    Final = data.assemble_train_data()
    Final = data.standardize(Final)
    Final.to_csv("finalized data.csv")
    print(Final)

if __name__ == "__main__":
    main()


