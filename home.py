from flask import Flask, render_template, request
from DatasetOps import *
from Reader import *
app = Flask("Gene annotation")

# Active Functions filename
defaultActiveFileName = 'settings/activeFunctions.csv'
#read the csv file containing active operations into a Dataframe with our specific reader implemented in the 'Reader.py' module
dfAct = CsvReader(defaultActiveFileName).read().df
#Reading the Human genome annotation file
f = open('dataset/Homo_sapiens.GRCh38.85.gff3')
ds = Gff3Reader(f).read()  #read the file into a Dataset with our specific reader

#creating the DatasetOperation object with the ds and the dfAct just read
dsOps = DatasetOps(ds, dfAct)

#homepage
@app.route('/')
def home():
    return render_template('active_operations.html')  # function used to import a html file into the py program without having to write in ptython

#get basic info
@app.route('/basicInfo')  # when on the web the user uses that / the function underneath is executed
def a():
    basic = dsOps.basicInfo().df.to_html()
    return f'''{basic}'''

#list of unique ID
@app.route('/uniqueID')  # when on the web the user uses that / the function underneath is executed
def b():
    id = dsOps.uniqueID().df.to_html()
    return f'''{id}'''


@app.route('/uniqueType')  # when on the web the user uses that / the function underneath is executed
def c():
    type = dsOps.uniqueType().df.to_html()
    return f'''{type}'''



@app.route('/countSource')  # when on the web the user uses that / the function underneath is executed
def d():
    countS = dsOps.countSource().df.to_frame(name='count').to_html()
    return f'''{countS}'''



@app.route('/countType')  # when on the web the user uses that / the function underneath is executed
def e():
    countT = dsOps.countType().df.to_frame(name='count').to_html()
    return f'''{countT}'''



@app.route('/chromosome')  # when on the web the user uses that / the function underneath is executed
def f():
    chrom = dsOps.entireChromosome().df.to_html()
    return f'''{chrom}'''



@app.route('/unassembledsq')  # when on the web the user uses that / the function underneath is executed
def g():
    unassembled = dsOps.unassembledSequence().df.to_html()
    return f'''{unassembled}'''



@app.route('/onlyhavensbl')  # when on the web the user uses that / the function underneath is executed
def h():
    ens_hav_df = dsOps.only_ensembl_havana().df.to_html()
    return f'''{ens_hav_df}'''


@app.route('/counthavensbl')  # when on the web the user uses that / the function underneath is executed
def i():
    ens_hav_count = dsOps.entries_ensembl_havana().df.to_html()
    return f'''{ens_hav_count}'''


@app.route('/havensblGeneNames')  # when on the web the user uses that / the function underneath is executed
def l():
    genes = dsOps.ensembl_havana_genes().df.to_html()
    return f'''{genes}'''



if __name__ == "__main__":
    app.run(port=80)  # we want to have our application available online, port 80 is the default for http
