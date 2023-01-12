import pandas as pd
def active(func):
    #CsvReader('settings/activeFunctions.csv').read().get_df()
    dfAct =pd.read_csv('settings/activeFunctions.csv') #this returns a dataframe
    def wrapper(*args):
        #self = args[0]  # in a Python decorator, args[0] corresponds to "self"
        #dfAct = self.dfAct
        funcName = func.__name__
        #filtering rows of the data
        funcrow = dfAct[dfAct['Function'] == funcName]  # if the function exists, funcrow has only 1 row

        if (funcrow.shape[0] == 1) and (funcrow.iloc[0]['Active'] == True):
            return func(*args)
        else:
            raise Exception("The function is not active or it does not exist")

    return wrapper