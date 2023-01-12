from Decorator import *
import pandas as pd
class Dataset:
    def __init__(self, pd_dataframe_read): #the Dataset is built on a pandas data frame
        self.__df = pd_dataframe_read #private attribute

    # @active decorator is called over each function
    def get_df(self): #method that retrieves the private dataframe attribute
        return self.__df
    #
    @active
    def basicInfo(self): #this method returns a Dataset with the column names and the data type they contain
        return Dataset(pd.DataFrame(data=self.get_df().dtypes, columns=['dtype']))

    def __uniqueList(self, column):#private method that given the column label returns the unique values of it
        dfUnique = self.get_df()[column].unique()
        return pd.DataFrame(data=dfUnique, columns=[column])
    @active
    def uniqueID(self): #return unique values of column seqID
        return Dataset(self.__uniqueList(column='seqID'))

    @active
    def uniqueType(self): #return unique values of column Type
        return Dataset(self.__uniqueList(column='type').sort_values(by='type', ignore_index=True))

    def __uniqueCount(self, column): #private method that given the column label returns the count of each one of its values
        return self.get_df().groupby(column, dropna=False).size().sort_values(ascending=False)

    @active
    def countSource(self): #return count of Source column
        return Dataset(self.__uniqueCount(column='source'))

    @active
    def countType(self): #return count of Type column
        return Dataset(self.__uniqueCount(column='type'))

    @active
    def entireChromosome(self): #returns a new dataframe selecting from the column source only the lines having GRCh38 as source
        return Dataset(self.get_df()[self.get_df()['source'] == 'GRCh38'].drop(columns=['source']))
        # we drop the source column from the dataframe because it will provide only GRCh38 sources since that was the filtering parameter

    @active
    def unassembledSequence(self): #returns the fraction and percentage of unassembled sequences over entire chromosomes set
        entire = self.entireChromosome().get_df() #retrieve the dataframe of only GRCh38 source
        unassembled = entire[entire['type'] == 'supercontig'] #select from these lines only the once of type supercontig
        fraction = str(unassembled.shape[0]) + "/" + str(entire.shape[0])#fraction
        perc = round(float(unassembled.shape[0]) * 100 / float(entire.shape[0]), 2) #rounded the percentage on 2 decimal
        values = [fraction, perc]
        return Dataset(pd.DataFrame([values], columns=["fraction", "percentage %"]))

    @active
    def only_ensembl_havana(self): #returns a new dataframe selecting only the lines having ensembl,havana and ensembl_havana as source
        return Dataset(self.get_df()[(self.get_df()['source'] == 'ensembl') |
                                     (self.get_df()['source'] == 'havana') |
                                     (self.get_df()['source'] == 'ensembl_havana')])

    @active
    def entries_ensembl_havana(self): #counts of the types only for ensembl,havana and ensembl_havana dataframe
        filtered_ds = self.only_ensembl_havana() #
        return Dataset(filtered_ds, self.dfAct).countType()

    @active
    def ensembl_havana_genes(self): #returns the name of the genes in the ensembl, havana and ensembl_havana dataframe
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
