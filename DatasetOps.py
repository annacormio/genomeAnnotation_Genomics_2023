from Dataset import *
import pandas as pd

def active(func):
    def wrapper(*args):
        self = args[0]  # in a Python decorator, args[0] corresponds to "self"
        dfAct = self.dfAct
        funcName = func.__name__
        #filtering rows of the data
        funcrow = dfAct[dfAct['Function'] == funcName]  # if the function exists, funcrow has only 1 row

        if (funcrow.shape[0] == 1) and (funcrow.iloc[0]['Active'] == True):
            return func(self)
        else:
            raise Exception("The function is not active or it does not exist")

    return wrapper

#cannot import dataset reader cuz we would have a circular calling of classes
class DatasetOps:
    def __init__(self, ds:Dataset, dsAct):
        self.ds = ds
        self.dsAct = dsAct #this can be

    @active
    def basicInfo(self):
        # lo metto così poi se decidiamo di cambiare sticaxxi
        return Dataset(pd.DataFrame(data=self.ds.df.dtypes, columns=['dtype']))

    def __uniqueList(self, column):
        dfUnique = self.ds.df[column].unique()
        return pd.DataFrame(data=dfUnique, columns=[column])

    @active
    def uniqueID(self):
        return Dataset(self.__uniqueList(column='seqID'))

    @active
    def uniqueType(self):
        return Dataset(self.__uniqueList(column='type').sort_values(by='type', ignore_index=True))

    def __uniqueCount(self, column):
        return self.ds.df.groupby(column, dropna=False).size().sort_values(ascending=False)

    @active
    def countSource(self):
        return Dataset(self.__uniqueCount(column='source'))

    @active
    def countType(self):
        return Dataset(self.__uniqueCount(column='type'))

    @active
    def entireChromosome(self):
        # fattibile anche con groupby + get_group , la drop elimina la colonna source
        return Dataset(self.ds.df[self.ds.df['source'] == 'GRCh38'].drop(columns=['source']))

    @active
    def unassembledSequence(self):
        entire = self.entireChromosome().df
        unassembled = entire[entire['type'] == 'supercontig']

        fraction = str(unassembled.shape[0]) + "/" + str(entire.shape[0])
        perc = round(float(unassembled.shape[0]) * 100 / float(entire.shape[0]), 2)

        values = [fraction, perc]
        return Dataset(pd.DataFrame([values], columns=["fraction", "percentage %"]))

    @active
    def only_ensembl_havana(self):
        return Dataset(self.ds.df[(self.ds.df['source'] == 'ensembl') |
                               (self.ds.df['source'] == 'havana') |
                               (self.ds.df['source'] == 'ensembl_havana')])

    @active
    def entries_ensembl_havana(self):
        filtered_ds = self.only_ensembl_havana()
        return DatasetOps(filtered_ds, self.dsAct).countType()

    @active
    def ensembl_havana_genes(self):
        filtered_df = self.only_ensembl_havana().df
        genes = filtered_df[(filtered_df['type'] == 'gene')]
        geneNames = []

        for index, row in genes.iterrows():
            attString = row['attributes']  # we select the attributes of a row
            attList = attString.split(";")  # we devide the attributes by ";"

            # we create an attribute dictionary for code readability, populating it one attr. by one
            attDict = {}
            for i in attList:
                (key, value) = i.split("=")
                attDict[key] = value

            geneNames.append(attDict['Name'])

        # we convert the list to set to delete duplicates
        return Dataset(pd.DataFrame(set(geneNames), columns=['gene_name']))
