from Dataset import *
from abc import ABC, abstractmethod
import pandas as pd

class DatasetReader(ABC):
    '''
    Abstract interface 
    '''
    @abstractmethod
    def read(self): 
        '''
        Abstract reading method
        '''
        pass

class Gff3Reader(DatasetReader): 
    '''
    Subclass of the abstract reading class specific for Gff3 files
    '''
    def __init__(self, filename): 
        '''
        A reader reiceives a file as input  
        '''
        self.filename = filename
        
    def read(self):
        '''
        Overriding of the abstract method read(): given a Gff3 file, it returns a Dataset object
        '''
        splitName=self.filename.split('.') # split the name in a list by '.' as delimiter
        if 'gff3' != splitName[-1]:        # verify the file type by considering the last string, which should be gff3
            raise Exception('Sorry, the program requires a gff3 file.') # if not gff3, the reader will not work
        else: #the file is read
            df = pd.read_csv(self.filename, delimiter="\t", comment="#",names=["seqID", "source", "type", "start", "end", "score", "strand", "phase", "attributes"], na_values='.') #with na_values we are substituting every '.' in the dataframe with NaN
            return Dataset(df)

