from Decorator import *
import pandas as pd


class Dataset:
    def __init__(self, pdDataframeRead):
        """
        Init function: the Dataset is built on a Pandas DataFrame
        """
        self.__df = pdDataframeRead  # private attribute
    
    def getDf(self):
        """
         Retrieves the private Pandas DataFrame attribute
        """

        return self.__df

    #@active decorator is called over each function 
    @active
    def basicInfo(self):  
        '''
        Returns a Dataset object with the column names and the data type they contain
        '''
        dfBasic = (self.getDf().dtypes.reset_index())
        return Dataset(dfBasic.rename(columns={"index": "column_name", 0: "data type"}))

    def __uniqueList(self, column):  
        '''
        Private method that given the column label returns a Pandas DataFrame with the column's unique values
        '''
        dfUnique = self.getDf()[column].unique()
        return pd.DataFrame(data=dfUnique, columns=[column])

    @active
    def uniqueID(self):  
        '''
        Returns a Dataset object with the unique values of the seqID column 
        '''
        return Dataset(self.__uniqueList(column='seqID'))

    @active
    def uniqueType(self):  
        '''
        Returns a Dataset object with the unique values of the Type column 
        '''
        return Dataset(self.__uniqueList(column='type').sort_values(by='type', ignore_index=True))

    def __uniqueCount(self,
                      column):  
        '''
        Private method that given the column label returns a Pandas DataFrame with the count of each one of its values
        '''
        uniqueDf = self.getDf().groupby(column, dropna=False).size().sort_values(
            ascending=False).reset_index()  # reset_index returns a DF with two columns
        return uniqueDf.rename(columns={0: "count"})

    @active
    def countSource(self):  
        '''
        Returns a Dataset object with the count of the Source column
        '''
        return Dataset(self.__uniqueCount(column='source'))

    @active
    def countType(self):  
        '''
        Returns a Dataset object with the count of the Type column
        '''
        return Dataset(self.__uniqueCount(column='type'))

    @active
    def entireChromosome(
            self):  
        '''
        Returns a Dataset object selecting from the column source only the rows having GRCh38 as source
        '''
        return Dataset(self.getDf()[self.getDf()['source'] == 'GRCh38'].drop(columns=['source']))
        # we drop the source column from the DataFrame because it will provide only GRCh38 sources since that was the filtering parameter

    @active
    def unassembledSequence(
            self):  
        '''
        Returns a Dataset object with the fraction and percentage of unassembled sequences over entire chromosomes set
        '''
        entire = self.entireChromosome().getDf()  # retrieves the Dataframe of only GRCh38 source
        unassembled = entire[
            entire['type'] == 'supercontig']  # selects from these rows only the ones of type supercontig
        fraction = str(unassembled.shape[0]) + "/" + str(entire.shape[0])  # fraction
        perc = round(float(unassembled.shape[0]) * 100 / float(entire.shape[0]),
                     2)  # percentage rounded on 2 decimal
        values = [fraction, perc]
        return Dataset(pd.DataFrame([values], columns=["fraction", "percentage %"]))

    @active
    def onlyEnsemblHavana(
            self):  
        '''
        Returns a Dataset object selecting only the rows having ensembl, havana and ensembl_havana as source
        '''
        return Dataset(self.getDf()[(self.getDf()['source'] == 'ensembl') |
                                    (self.getDf()['source'] == 'havana') |
                                    (self.getDf()['source'] == 'ensembl_havana')].reset_index())

    @active
    def entriesEnsemblHavana(self):  
        '''
        Returns a Dataset object with the count of the types of sequences in the ensembl, havana and ensembl_havana Dataset
        '''
        filteredDs = self.onlyEnsemblHavana()  
        return filteredDs.countType()

    @active
    def ensemblHavanaGenes(self):  
        '''
        Returns a Dataset object with the names of the genes in the ensembl, havana and ensembl_havana Dataset
        '''
        filteredDf = self.onlyEnsemblHavana().getDf()
        genes = filteredDf[(filteredDf['type'] == 'gene')]
        geneNames = []

        for index, row in genes.iterrows():
            attString = row['attributes']  # we select the attributes of a row
            attList = attString.split(";")  # we divide the attributes by ";"

            # we create an attribute dictionary for code readability, populating it one attribute by one
            attDict = {}
            for i in attList:
                (key, value) = i.split("=") # we divide the elements of the attList by "="
                attDict[key] = value # we add the elements in the dictionary

            geneNames.append(attDict['Name']) # we add the gene name in the genNames list 

        # we convert the geneName list to set to delete duplicates 
        # set does not allow duplicates so all genes names repeated, if there are any, are dropped
        return Dataset(pd.DataFrame(set(geneNames), columns=[
            'gene_name']))  
