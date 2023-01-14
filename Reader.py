from Dataset import *
from abc import ABC, abstractmethod
import pandas as pd


# abstract class for reading the file
class DatasetReader(ABC):


    @abstractmethod
    def read(self): #abstract reading method
        pass


# implementation of the reader from gff3 files to pandas dataframes returning a Dataset
class Gff3Reader(DatasetReader): #subclass of the abstract reading class
    def __init__(self, filename): # receives a file as input
        self.filename = filename
    def read(self):
        df = pd.read_csv(self.filename, delimiter="\t", comment="#",names=["seqID", "source", "type", "start", "end", "score", "strand", "phase", "attributes"], na_values='.') #with na_values we are substituting every '.' in the dataframe with NaN
        return Dataset(df)

'''
class CsvReader(DatasetReader):
    def read(self):
        df = pd.read_csv(self.filename)
        return df
        '''

#we though about implementing the reader also for the active operations .csv file
#we could not use it in the decorator because we get a circular import
#Decorator imports Reader which imports Dataset which imports the Reader again (this is the circle that generates)

#we also tried to have the Csvreader retrun a dataframe instead of a Dataset but the circle generates anyway