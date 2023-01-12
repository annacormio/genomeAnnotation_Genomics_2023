from flask import Flask, render_template
from Reader import Gff3Reader
app = Flask("Gene annotation")

#Reading the Human genome annotation file
f = open('dataset/Homo_sapiens.GRCh38.85.gff3')
ds = Gff3Reader(f).read()  #read the file into a Dataset with our specific reader

#creating the DatasetOperation object with the ds and the dfAct just read
#dsOps = DatasetOps(ds, dfAct)

#homepage
@app.route('/')
def home():
    return render_template('active_operations.html')  # function used to import a html file into the py program without having to write in ptython

#get basic info
@app.route('/basicInfo')  # when on the web the user uses that / the function underneath is executed
def a():
    basic = ds.basicInfo()
    return f'''{basic.get_df().to_html()}'''

#list of unique ID
@app.route('/uniqueID')  # when on the web the user uses that / the function underneath is executed
def b():
    id = ds.uniqueID().get_df().to_html()
    return f'''{id}'''


@app.route('/uniqueType')  # when on the web the user uses that / the function underneath is executed
def c():
    type = ds.uniqueType().get_df().to_html()
    return f'''{type}'''



@app.route('/countSource')  # when on the web the user uses that / the function underneath is executed
def d():
    countS = ds.countSource().get_df().to_frame(name='count').to_html()
    return f'''{countS}'''



@app.route('/countType')  # when on the web the user uses that / the function underneath is executed
def e():
    countT = ds.countType().get_df().to_frame(name='count').to_html()
    return f'''{countT}'''



@app.route('/chromosome')  # when on the web the user uses that / the function underneath is executed
def f():
    chrom = ds.entireChromosome().get_df().to_html()
    return f'''{chrom}'''



@app.route('/unassembledsq')  # when on the web the user uses that / the function underneath is executed
def g():
    unassembled = ds.unassembledSequence().get_df().to_html()
    return f'''{unassembled}'''



@app.route('/onlyhavensbl')  # when on the web the user uses that / the function underneath is executed
def h():
    ens_hav_df = ds.only_ensembl_havana().get_df().to_html()
    return f'''{ens_hav_df}'''


@app.route('/counthavensbl')  # when on the web the user uses that / the function underneath is executed
def i():
    ens_hav_count = ds.entries_ensembl_havana().get_df().to_html()
    return f'''{ens_hav_count}'''


@app.route('/havensblGeneNames')  # when on the web the user uses that / the function underneath is executed
def l():
    genes = ds.ensembl_havana_genes().get_df().to_html()
    return f'''{genes}'''



if __name__ == "__main__":
    app.run(port=80)  # we want to have our application available online, port 80 is the default for http
