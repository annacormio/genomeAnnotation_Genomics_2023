from Decorator import *
import pandas as pd

#defaultActiveFileName = 'settings/activeFunctions.csv'
#read the csv file containing active operations into a Dataframe with our specific reader implemented in the 'Reader.py' module

class Dataset:
    def __init__(self, pd_dataframe_read):
        self.df = pd_dataframe_read
        # each operation should be marked as active through a decorator

    '''def get_df(self):
        return self.df
        '''

    @active
    def basicInfo(self):
        # lo metto così poi se decidiamo di cambiare sticaxxi
        return Dataset(pd.DataFrame(data=self.get_df().dtypes, columns=['dtype']))

    def __uniqueList(self, column):
        dfUnique = self.get_df()[column].unique()
        return pd.DataFrame(data=dfUnique, columns=[column])

    @active
    def uniqueID(self):
        return Dataset(self.__uniqueList(column='seqID'))

    @active
    def uniqueType(self):
        return Dataset(self.__uniqueList(column='type').sort_values(by='type', ignore_index=True))

    def __uniqueCount(self, column):
        return self.get_df().groupby(column, dropna=False).size().sort_values(ascending=False)

    @active
    def countSource(self):
        return Dataset(self.__uniqueCount(column='source'))

    @active
    def countType(self):
        return Dataset(self.__uniqueCount(column='type'))

    @active
    def entireChromosome(self):
        # select from the column source only the lines having GRCh38 as source
        return Dataset(self.get_df()[self.get_df()['source'] == 'GRCh38'].drop(
            columns=['source']))  # we drop the source column from the dataframe
        # because it will provide only GRCh38 sources since that was the filtering parameter

    @active
    def unassembledSequence(self):
        entire = self.entireChromosome().get_df()
        unassembled = entire[entire['type'] == 'supercontig']

        fraction = str(unassembled.shape[0]) + "/" + str(entire.shape[0])
        perc = round(float(unassembled.shape[0]) * 100 / float(entire.shape[0]), 2)

        values = [fraction, perc]
        return Dataset(pd.DataFrame([values], columns=["fraction", "percentage %"]))

    @active
    def only_ensembl_havana(self):
        return Dataset(self.get_df()[(self.get_df()['source'] == 'ensembl') |
                                        (self.get_df()['source'] == 'havana') |
                                        (self.get_df()['source'] == 'ensembl_havana')])

    @active
    def entries_ensembl_havana(self):
        filtered_ds = self.only_ensembl_havana()
        return DatasetOps(filtered_ds, self.dfAct).countType()

    @active
    def ensembl_havana_genes(self):
        filtered_df = self.only_ensembl_havana().get_df()
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


