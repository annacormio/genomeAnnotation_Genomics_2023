import pandas as pd
#implementing the decorator
def active(func):
    #read the .csv file containing the functions activity or not
    dfAct =pd.read_csv('settings/activeFunctions.csv') #returns a dataframe
    def wrapper(*args):
        funcName = func.__name__ #get just the name of the function
        #filtering rows of the data
        funcrow = dfAct[dfAct['Function'] == funcName]
        # if the function exists, funcrow has only 1 row
        if (funcrow.shape[0] == 1) and (funcrow.iloc[0]['Active'] == True):# here I check that it actually is just a row and that the 'Active' status is True
            return func(*args) #if condition is satisfied I execute the function
        else:
            raise Exception("The function is not active or it does not exist")


    return wrapper


#da togliere alla consegna---->

# self = args[0]  # in a Python decorator, args[0] corresponds to "self"
# dfAct = self.dfAct