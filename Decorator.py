import pandas as pd

def active(func):
    '''
    Decorator that reads the .csv file containing information on the functions' activities
    '''
    dfAct =pd.read_csv('settings/activeFunctions.csv') #returns a dataframe
    def wrapper(*args):
        '''
        If the function is active, the function is executed
        If the function is not active, an Exception is raised
        '''
        funcName = func.__name__ #get just the name of the function
        #filtering rows of the data
        funcrow = dfAct[dfAct['Function'] == funcName]
        # if the function exists, funcrow has only 1 row
        if (funcrow.shape[0] == 1) and (funcrow.iloc[0]['Active'] == True):# here I check that it actually is just a row and that the 'Active' status is True
            return func(*args) 
        else:
            raise Exception("The function is not active or it does not exist")


    return wrapper

