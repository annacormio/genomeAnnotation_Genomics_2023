from Dataset import *
from abc import ABC, abstractmethod
import pandas as pd

'''
#from Dataset import *
filename = 'Homo_sapiens.GRCh38.85.gff3'
df = pd.read_csv(file,delimiter="\t",comment="#",names=["seqID","source","type","start","end","score","strand","phase","attributes"], na_values='.' )
'''


# abstract class for reading the file
class DatasetReader(ABC):
    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def read(self):
        pass


# implementation of the reader from gff3 files to pandas dataframes
class Gff3Reader(DatasetReader):
    def read(self):
        df = pd.read_csv(self.filename, delimiter="\t", comment="#",
                         names=["seqID", "source", "type", "start", "end", "score", "strand", "phase", "attributes"],
                         na_values='.')
        return Dataset(df)


class CsvReader(DatasetReader):
    def read(self):
        df = pd.read_csv(self.filename)
        return Dataset(df)
