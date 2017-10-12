'''
Created on Mar 24, 2017

@author: Jonathan.Cobb
'''
import os
from flask import Flask, render_template, request,make_response
import sys
from Utils import Utils
from Sql import Sql
import qbapi.qbapi as qb
from flask.helpers import send_file
from stjohns_calculator import stjohnsdict
from werkzeug import secure_filename
from mimetypes import MimeTypes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './stjohns'
mydir = os.path.dirname(__file__)
util = Utils()

@app.route('/')
def main():
    return render_template('Utils.html')

@app.route('/SplitPdf', methods=['GET','POST'])
def SplitPdf():
    tempf = './temp'
    file_to_split = request.files['splitpdf']
    if file_to_split is None:
        return render_template('Utils.html')
    batchf = os.path.join(mydir,'batchfiles/pdfSplit.bat')
    
    oldfilename = file_to_split.filename.replace('/','_').replace(' ','_')
    filename = os.path.join(tempf,str(oldfilename))
    file_to_split.save(secure_filename(file_to_split.filename))
    
    
    os.rename(os.path.join(mydir,str(oldfilename)), filename)
    command = batchf +" "+filename
    filelist = []
    os.system(command)
    os.remove(filename)
    for files in os.listdir(tempf):
        filelist.append(os.path.join(os.path.join(mydir,'temp'),files))
    return render_template('FileList.html',filelist=filelist)
    
@app.route('/home')
def home():
    for files in os.listdir('./temp'):
        os.remove('./temp/'+files)   
    return render_template('Utils.html')
    
@app.route('/StJohns', methods=['GET','POST'])
def Stjohns():
    county = request.form['county']
    folderpath = './'+county
    seeklist = request.form['totals'].split(',')
    seeklist = [float(i) for i in seeklist]
    if county is None or seeklist is None:
        return render_template('Utils.html')
    for inputfolder in request.files.getlist('folder'):
        inputfolder.save(secure_filename(inputfolder.filename).replace('_','/'))
    util.stjohnsPdf(folderpath,county)
    filelist = stjohnsdict(folderpath, seeklist,'temp',county)
    for files in os.listdir(folderpath):
        os.remove(os.path.join(folderpath,files))
    os.remove('./'+county+'.txt')
    return render_template('FileList.html',filelist=filelist)

@app.route('/attach/<filename>')
def attach(filename=None):
    return send_file(filename, mimetype='application/txt',as_attachment=True)
    
@app.route('/pdfView', methods=['GET','POST'])
def pdfView():
    depid = request.form['depid']
    #get deposit id
    fields = "8"
    token ='cxeyvydbvik5y3523fepbiue8q2'
    tid = 'bk2reib52'
    qstringofrqb="{3.EX.'"+depid+"'}"
    dep_rec_id = qb.query_table(token,tid,qstringofrqb,fields).old_fig_deposits_record_id[0]
    docquery = util.readFile(mydir,'sqlFiles/docvbin.sql').replace('(REPLACE ID)',dep_rec_id)
    docvbin = sql.findOne(docquery)
    if docvbin is None:
        txtquery = util.readFile(mydir,'sqlFiles/rocrv.sql').replace('(REPLACE ID)',dep_rec_id)
        ocr_text = sql.findOne(txtquery)[0]
        util.writeFile(mydir, depid+'.txt', ocr_text) 
        return send_file(os.path.join(mydir,depid+'.txt'), mimetype='application/txt', as_attachment=True)
    response = make_response(bytearray(docvbin[0]))
    if '.pdf' in docvbin[1]:
        response.mimetype = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename='+depid+".pdf"
    elif '.csv' in docvbin[1]:
        response.mimetype = 'application/csv'
        response.headers['Content-Disposition'] = 'attachment; filename='+depid+".csv"
    elif '.txt' in docvbin[1]:
        if str(type(docvbin[0])) == "<type 'buffer'>" and 'PDF' in str(docvbin[0]):
            response.mimetype = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename='+depid+".pdf"
        else:
            response.mimetype = 'application/txt'
            response.headers['Content-Disposition'] = 'attachment; filename='+depid+".txt"
    return response 

if __name__=="__main__":
    args = sys.argv[1:]
    argMap = util.getArgPairs(args, '=')
    hostname = argMap.get("url")
    username = argMap.get("uid")
    password = argMap.get("password")
    db = argMap.get("db")
    sql = Sql(hostname, username, password, db)
    sys.argv = ['username=bperlman@figadvisors.com','password=figtree77*']
    qb.authenticate_from_args()
    app.run( port=5300, debug=False)