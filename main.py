from flask import Flask, render_template
from Reader import Gff3Reader

app = Flask("Gene annotation")

#Reading the Human genome annotation file
f = open('dataset/Homo_sapiens.GRCh38.85.gff3')
ds = Gff3Reader(f).read()  #read the file into a Dataset with our specific reader
ds.entries_ensembl_havana()
#homepage
@app.route('/')
def home():
    return render_template('active_operations.html')  #referes to the active_operation.html file

#get basic info
@app.route('/basicInfo')  #/ indicates the reference of the link
def a():
    basic = ds.basicInfo()
    return f'''{basic.get_df().to_html()}'''

#list of unique ID
@app.route('/uniqueID')
def b():
    id = ds.uniqueID().get_df().to_html()
    return f'''{id}'''

#list of unique Types
@app.route('/uniqueType')
def c():
    type = ds.uniqueType().get_df().to_html()
    return f'''{type}'''

#count of sources
@app.route('/countSource')
def d():
    countS = ds.countSource().get_df().to_frame(name='count').to_html()
    return f'''{countS}'''

#count of types
@app.route('/countType')
def e():
    countT = ds.countType().get_df().to_frame(name='count').to_html()
    return f'''{countT}'''

#entire chromosomes only dataset
@app.route('/chromosome')
def f():
    chrom = ds.entireChromosome().get_df().to_html()
    return f'''{chrom}'''

#fraction of unassembled sequences and chromosomes
@app.route('/unassembledsq')
def g():
    unassembled = ds.unassembledSequence().get_df().to_html()
    return f'''{unassembled}'''

#dataset of ensembl, havana, ensembl_havana
@app.route('/onlyhavensbl')
def h():
    ens_hav_df = ds.only_ensembl_havana().get_df().to_html()
    return f'''{ens_hav_df}'''

#count of ensembl, havana, ensembl_havana types
@app.route('/counthavensbl')
def i():
    ens_hav_count = ds.entries_ensembl_havana().get_df().to_frame(name='count').to_html()
    return f'''{ens_hav_count}'''

#dataset of ensembl, havana, ensembl_havana gene Names
@app.route('/havensblGeneNames')  # when on the web the user uses that / the function underneath is executed
def l():
    genes = ds.ensembl_havana_genes().get_df().to_html()
    return f'''{genes}'''


if __name__ == "__main__":
    app.run(port=80)  # we want to have our application available online, port 80 is the default for http