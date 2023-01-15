from Dataset import *
from abc import ABC, abstractmethod
import pandas as pd


# abstract class for reading the file
class DatasetReader(ABC):
    '''def __init__(self, filename): #a reader in general receives a file as input
        self.filename = filename''' 
    # ^ lo abbiamo messo come commento per provare a rendere DatasetReader una abstract INTERFACE e non abstract class; lo reimplementiamo in Gff3Reader

    @abstractmethod
    def read(self): #abstract reading method
        pass


# implementation of the reader from gff3 files to pandas dataframes returning a Dataset
class Gff3Reader(DatasetReader): #subclass of the abstract reading class
    def __init__(self, filename): #a reader in general receives a file as input
        self.filename = filename
        
    def read(self):
        df = pd.read_csv(self.filename, delimiter="\t", comment="#",names=["seqID", "source", "type", "start", "end", "score", "strand", "phase", "attributes"], na_values='.') #with na_values we are substituting every '.' in the dataframe with NaN
        return Dataset(df)

'''
class CsvReader(DatasetReader):
    def read(self):
        df = pd.read_csv(self.filename)
        return Dataset(df)
'''
