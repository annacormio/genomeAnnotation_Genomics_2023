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
        df = pd.read_csv(self.filename, delimiter="\t", comment="#",names=["seqID", "source", "type", "start", "end", "score", "strand", "phase", "attributes"], na_values='.') #with na_values we are substituting every '.' in the dataframe with NaN
        return Dataset(df)

'''
class CsvReader(DatasetReader):
    def read(self):
        df = pd.read_csv(self.filename)
        return Dataset(df)
'''
