from flask import Flask, render_template
from Reader import Gff3Reader

app = Flask("Gene annotation")

# Reading the Human genome annotation file
f = 'dataset/Homo_sapiens.GRCh38.85.gff3'
ds = Gff3Reader(f).read()  # read the file into a Dataset with our specific reader


# homepage
@app.route('/')
def home():
    return render_template('homepage.html')  # referes to the homepage.html file
    #render_template by default retrieves the html file from the folder named 'templates'

#documentation
@app.route('/documentation') # / indicates the reference of the link
def doc():
    return render_template('documentation.html')

#active operations
@app.route('/active_op')
def operations():
    return render_template('active_operations.html')

# get basic info
@app.route('/basicInfo')  
def a():
    basic = ds.basicInfo().getDf().to_html()
    return basic


# list of unique ID
@app.route('/uniqueID')
def b():
    idUn = ds.uniqueID().getDf().to_html()
    return idUn


# list of unique Types
@app.route('/uniqueType')
def c():
    typeL = ds.uniqueType().getDf().to_html()
    return typeL


# count of sources
@app.route('/countSource')
def d():
    countS = ds.countSource().getDf().to_html()
    return countS


# count of types
@app.route('/countType')
def e():
    countT = ds.countType().getDf().to_html()
    return countT


# entire chromosomes only dataset
@app.route('/chromosome')
def f():
    chrom = ds.entireChromosome().getDf().to_html()
    return chrom


# fraction of unassembled sequences and chromosomes
@app.route('/unassembledsq')
def g():
    unassembled = ds.unassembledSequence().getDf().to_html()
    return unassembled


# dataset of ensembl, havana, ensembl_havana
@app.route('/onlyhavensbl')
def h():
    ensHavDf = ds.onlyEnsemblHavana().getDf().to_html()
    return ensHavDf


# count of ensembl, havana, ensembl_havana types
@app.route('/counthavensbl')
def i():
    ensHavCount = ds.entriesEnsemblHavana().getDf().to_html()
    return ensHavCount


# dataset of ensembl, havana, ensembl_havana gene Names
@app.route('/havensblGeneNames')  # when on the web the user uses that / the function underneath is executed
def l():
    genes = ds.ensemblHavanaGenes().getDf().to_html()
    return genes


if __name__ == "__main__":
    app.run(port=80)  # we want to have our application available online, port 80 is the default for http
