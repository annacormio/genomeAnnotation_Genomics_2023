from flask import Flask, render_template, request
from DatasetOps import *
from Reader import *
# Active Functions filename
defaultActiveFileName = 'settings/activeFunctions.csv'
myfile = '../dataset/Homo_sapiens.GRCh38.85.gff3'

app = Flask("Gene annotation")
filenames = []
dsOps = []


# create web homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')  # function used to import a html file into the py program without having to write in ptython


# getting the file
'''
@app.route('/activeoperations', methods = ['GET', 'POST'])
def activeop():

    if request.method == 'POST':
        f = request.form['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Reading the files
        ds = Gff3Reader(f).read()
        dfAct = CsvReader(defaultActiveFileName).read().df


        dsOps = DatasetOps(ds, dfAct)

    return render_template('active_operations.html',file=f)
'''


# create other pages for operation display
@app.route("/", methods=['GET', 'POST'])
def index():
    dfAct = CsvReader(defaultActiveFileName).read().df
    if request.method == 'POST':
        # dsSelected = Gff3Reader(request.form.get("gff3")).read()
        if 'dsFile' in request.files:  # if a file is inserted
            f = request.files['dsFile']  # I request the file
            # f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            # Reading the files with my reader
            ds = Gff3Reader(f).read()
            dsOps = DatasetOps(ds, dfAct)
            return render_template('active_operations.html')
        elif request.form['submit']=='basicInfo':
            return dsOps.basicInfo()
    '''
        if request.form['submit'] == 'uniqueID':
                dsOps.uniqueID()
        if request.form['submit']=='uniqueType':
            dsOps.uniqueType()
        if request.form['submit']=='countSource':
            dsOps.countSource()
        if request.form['submit']=='countType':
            dsOps.countType()
        if request.form['submit']=='entireChrom':
            dsOps.entireChromosome()
        if request.form['submit']=='unassembledSeq':
            dsOps.unassembledSequence()
        if request.form['submit']=='onlyEnsmblHav':
            dsOps.only_ensembl_havana()
        if request.form['submit']=='countEnsmblHav':
            dsOps.entries_ensembl_havana()
        if request.form['submit']=='geneEnsmblHav':
            dsOps.ensembl_havana_genes()

        # elif #se viene da pulsante unique Id :
        # dfOps.uniqueid
        
        else:  # if no file is uploaded
            print('hello')
            f = myfile  # it takes the human genome annotation file as defualt
            ds = Gff3Reader(f).read()
            dfAct = CsvReader(defaultActiveFileName).read().df
            dsOps = DatasetOps(ds, dfAct)
            return render_template('active_operations.html')
'''

if __name__ == "__main__":
    app.run(port=80)  # we want to have our application available online, port 80 is the default for http

'''
@app.route('/basicinfo')  # when on the web the user uses that / the function underneath is executed
def a():
    return


@app.route('/listID')  # when on the web the user uses that / the function underneath is executed
def b():
    return 'This is the page in which i display the list of IDs'


@app.route('/optypes')  # when on the web the user uses that / the function underneath is executed
def c():
    return 'This is the page in which i display the list of operation types'


@app.route('/countft')  # when on the web the user uses that / the function underneath is executed
def d():
    return 'This is the page in which i display the count of features from one source'


@app.route('/entries')  # when on the web the user uses that / the function underneath is executed
def e():
    return 'This is the page in which i display the number of entries for the operations'


@app.route('/chromosome')  # when on the web the user uses that / the function underneath is executed
def f():
    return 'This is the page in which i display only informations about entire chrosomes'


@app.route('/unassembledsq')  # when on the web the user uses that / the function underneath is executed
def g():
    return 'This is the page in which i display the fraction of unassembled seuqences'


@app.route('/onlyhavensbentries')  # when on the web the user uses that / the function underneath is executed
def h():
    return 'This is the page in which i display only entries from source ensembl , havana andensembl_havana'


@app.route('/counthavensblentries')  # when on the web the user uses that / the function underneath is executed
def i():
    return 'This is the page in which i display the count of entries for each type of operation for the dataset containing only entries from source ensembl , havana and ensembl_havana'


@app.route('/havensblgenenames')  # when on the web the user uses that / the function underneath is executed
def l():
    return 'This is the page in which i display the gene names from the dataset containing containing only entries from source ensembl ,havana and ensembl_havana'



'''
# --------------------------------------------------------------------------------------------------
# Dataset filenames (folder "/dataset")
'''
    import glob, os

    os.chdir("dataset/")
    for file in glob.glob("*.gff3"):
        filenames.append(file)

    print(filenames)
    # Active Functions filename
    activeFileName = '../settings/activeFunctions.csv'

    # Reading the files
    dfAct = CsvReader(activeFileName).read().df
    
    # dsOps = DatasetOps(ds, dsAct)
    
'''
'''
    < p > select
    here
    your.gff3
    file
    from the dropdown

DROPDOWN BOX
    < form
    method = "post"
    action = "/select" >
    < select
    name = "gff3"
    id = "gff3" >
    { %
    for fn in filenames %}
    < option > {{fn}} < / option >
{ % endfor %}
< / select >

< / form >

< / p >
BUTTON FOR LOADING
<form method="post" action="/">
                <input type="submit" value="loadDSButton" name="loadDS"/>
            </form>
'''
