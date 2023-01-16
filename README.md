# genomeAnnotation_Genomics_2023

Genome annotation project for the Advanced Programming exam of the Genomics UniBo course, a.y. 2022/2023 - January 2023 session. 

Contributors: Chiozza Alice, Cormio Anna, De Angelis Simone, Rossi Marzia.

## Notes on the gff3 file on the human genome
The size of the gff3 file 'Homo_sapiens.GRCh38.85.gff3' is too big to be uploaded on GitHub, even in its zipped form (see <a href = 'https://github.com/annacormio/genomeAnnotation_Genomics_2023/blob/master/.gitignore' target = '_blank'> .gitignore</a>). Hence, we provide the following <a href='https://drive.google.com/file/d/1P4nYtl_SYNegCbWsoR-syltB84WOyaOp/view' target = '_blank'> link</a> from which the user can download the file.

* The file must be saved <i>exactly</i> as Homo_sapiens.GRCh38.85.gff3, or the code will not work. While we recognise this lack of generalisation, the specification of the project requested to design a program specific for reading the data cointained in the aforementioned gff3 document.
* The Homo_sapiens.GRCh38.85.gff3 file must be saved in the <a href = 'https://github.com/annacormio/genomeAnnotation_Genomics_2023/tree/master/dataset' target="__blank"> dataset</a> folder.

## Documentation

> <b> Note: The following information is the same offered at the Project Specification page on the browser user interface. </b>
 
Following the project specifications, we implemented the abstract interface <b>DatasetReader</b>, which presents the abstract method <i><b>read()</i></b>, overridden by the <i><b>read()</i></b> method of the <b>Gff3Reader</b>, the DatasetReader subclass. 

Gff3Reader is thus the realisation of the DatasetReader abstract interface; it is a concrete class that accepts a tabular file of format gff3 as an input and returns a Dataset object. We made sure that the class Gff3Reader was specific for the gff3 format by requesting that the fiel directory ended with '.gff3'. We analysed the file directory by splitting the whole using ‘.’ as delimiter, considering that the specification of the file type is contained in the last string, <i>e.g.</i> 

* ‘Auto.tsv’ ->  last string = file type = ‘tsv’ -> raises exception
* ‘Homo_sapiens.GRCh38.85.gff3’ -> last string = file type = ‘gff3’ -> works

The Dataset class is built around a Pandas Dataframe and can perform a list of active operations on that, which are listed as its public methods; all of those operations return a Dataset object. 

The only two private methods found in the Dataset class are: 
*	<b><i>__uniqueList(column)</b></i> – given a column label, it returns the unique values in it in the form of a Pandas DataFrame; 
    implemented to exploit reusability of code, as it is utilised by both <i><b>uniqueID()</i></b> and <i><b>uniqueType()</i></b>. 
* <b><i>__uniqueCount(column)</b></i> – given a column label, it returns the count of each of its values. Returns a Pandas DataFrame.
    As above, implemented to avoid repetition of code; it is utilised by <i><b>countSource()</b></i> and <i><b>countType()</i></b>.

As for the other methods found, which return all a Dataset object:

*	<b><i>getDf()</b></i> – retrieves the private attribute <i><b>__self.df</i></b> (type Pandas DataFrame);
*	<b><i>basicInfo()</b></i> – returns a Dataset object which provides us the column names and the type of the data contained in each of them; i.e. it can be used to retrieve the basic information on the Dataset obtained from the GFF3 file reading;
*	<b><i>uniqueID()</b></i> – returns unique values of column seqID (no duplicates);
*	<b><i>uniqueType()</b></i> – returns a Dataset object which informs us on the list of unique type of operations available in the dataset;
*	<b><i>countSource()</b></i> – returns count of Source column – for each source, how many entries do we have of it?
*	<b><i>countType()</b></i> – returns count of Type column – for each type, how many entries do we have? 
*	<b><i>entireChromosome()</b></i> – filters the column source to identify only entire chromosomes rows – i.e. only rows with source GRCh38 are selected and returned as a new dataset object;
*	<b>unassembledSequence()</b> – returns fraction and percentage of the unassembled sequences over the dataset provided by entireChromosome(), retrieving first the dataset obtained by ‘<b><i>entireChromosome()</b></i>’ method and then selecting only the entries of type ‘superconting’; eventually, it performs the fraction of the unassembled over the total entries to obtain the ratio, which is expressed also as percentage;
*	<b><i>onlyEnsemblHavana()</b></i> – returns a new dataset with only entries from sources ensembl, havana and ensembl_havana;
*	<b><i>entriesEnsemblHavana()</b></i> – counts the number of entries for each unique type found in the <i><b>onlyEnsemblHavana()</b></i> Dataset;
*	<b><i>ensemblHavanaGenes()</b></i> – returns the name of the genes present in the dataset obtained by <i><b>onlyEnsemblHavana()</b></i>.

The decorator implemented in our program read a .csv file containing the name of a function and if it is active or not (True or False). If it is not active, when the user tries to execute the operation in the web interface it gives us an Internal Server error while if the operation is active, we see the returning Dataset printed in a table.

>A note on <b>active operations</b> and the <b>decorator</b> that manages them: our choice of implementation was to use a csv file to compile the list of active >operation, and a function decorator to manage them. This meant that our UML class diagram could not figure nor the registry of active operation, nor the decorator, >albeit they both interact with the class Dataset, since it must check for an operation to be active before performing them. For coherence, and as we found it to be >rather disorienting, we also did not add the collaboration to the CRC cards.

The software functions through the execution of the main module implemented with Flask. There we read the .gff3 file using the Gff3Reader. Using the link we visualize an hompegage that contains two links: 

1. the project documentation with CRC cards and UML 
2. the active operations to perform on the Dataset. 
-> The link to the operations contains a list of the operations having each one a link that leads to the printing of the resulting table in a new tab. 
The web implementation is written in .html files that are then easily integrated with Flask using ‘render_template’.

The decorator implemented in our program reads a .csv file containing the name of a function and if it is active or not (True or False). 
* If the operation is not active, when the user tries to execute it in the web interface it gives an Internal Server error 
* If the operation is active, the user sees the returning Dataset printed in a table.


The software functions through the execution of the main module implemented with Flask. There we read the .gff3 file using the Gff3Reader. Using the link the user visualizes an hompegage that contains two links: 
* one for the <b>project documentation</b> with CRC cards and UML; 
* one for the <b>operations</b> to perform on the Dataset: opens a list the operations, each one with a link that opens in a new tab the table returned by the operation. 
    
The web implementation is written in .html files that are then easily integrated with Flask using ‘render_template’.
