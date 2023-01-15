import time

from flask import Flask, render_template
from Reader import Gff3Reader
import pandas as pd
import numpy as np

app = Flask("Gene annotation")

# Reading the Human genome annotation file
f = open('dataset/Homo_sapiens.GRCh38.85.gff3')
ds = Gff3Reader(f).read()  # read the file into a Dataset with our specific reader


def testExTime():
    """
    Tests execution times of all the active functions, plus the returned type and the size of the dataframe
    """
    dfAct = pd.read_csv('settings/activeFunctions.csv')  # returns a dataframe
    for index, row in dfAct.iterrows():
        try:
            funcName = row['Function']
            function = getattr(ds, funcName)
            start = time.time()
            ds2 = function()
            ds2Type = str(type(ds2))
            end = time.time()
            duration = end - start
            print("Test Execution Time --> ", funcName, "\t", ds2Type, "\t", duration, "\t", "(", ds2.getDf().shape[0], ",",
                  ds2.getDf().shape[1], ")")
        except Exception as e:
            print("Exception with: ", funcName)
            print(e)


def testAll():
    """
    Tests manually all the functions, with specific Unit tests
    """
    dfAct = pd.read_csv('settings/activeFunctions.csv')  # returns a dataframe
    for index, row in dfAct.iterrows():
        try:
            funcName = row['Function']
            function = getattr(ds, funcName)
            df = ds.getDf()
            df2 = function().getDf()

            if funcName == 'basicInfo':
                assert (df2.shape[0] == df.shape[1])
                assert (df2.shape[1] == 2)
            elif funcName == 'uniqueID':
                assert (df2.shape[1] == 1)
                assert (np.all(df2['seqID'].value_counts() == 1))
            elif funcName == 'uniqueType':
                assert (df2.shape[1] == 1)
                assert (np.all(df2['type'].value_counts() == 1))
            elif funcName == 'countSource':
                assert (df2.shape[1] == 2)
                assert (np.all(df2['source'].value_counts() == 1))
            elif funcName == 'countType':
                assert (df2.shape[1] == 2)
                assert (np.all(df2['type'].value_counts() == 1))
            elif funcName == 'entireChromosome':
                dfTemp = df
                dfTemp2 = df[df['source'] != "GRCh38"]
                assert (df2.shape[0] == dfTemp.shape[0] - dfTemp2.shape[0])
                assert (np.all(df2['type'].unique() in np.array(['chromosome', 'supercontig'])))
            elif funcName == 'unassembledSequence':
                df3 = ds.entireChromosome().getDf()
                typeCount = df3['type'].value_counts().reset_index()
                num_den = df2['fraction'][0].split("/")
                assert (int(num_den[1]) == int(typeCount['type'][0]) + int(typeCount['type'][1]))
                assert (typeCount.shape[0] == 2)  # two Types
            elif funcName == 'onlyEnsemblHavana':
                dfTemp = df
                dfTemp2 = df[
                    (df['source'] != "ensembl") & (df['source'] != "havana") & (df['source'] != "ensembl_havana")]
                assert (df2.shape[0] == dfTemp.shape[0] - dfTemp2.shape[0])
            elif funcName == 'entriesEnsemblHavana':
                assert (df2.shape[1] == 2)
                assert (np.all(df2['type'].value_counts() == 1))
            elif funcName == 'ensemblHavanaGenes':
                assert (df2.shape[1] == 1)
                assert (np.all(df2['gene_name'].value_counts() == 1))

            print(f'Testall --> {funcName}: OK')

        except Exception as e:
            print("Exception with: ", funcName)
            print(e)

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

help(testExTime)
testExTime()

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

help(testAll)
testAll()

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
