'''
Created on Mar 24, 2017

@author: Jonathan.Cobb
'''
import os
import logging

class Utils:
    
    def readFile(self, mydir,filepath):
        fd = open(os.path.join(mydir,filepath),'r')
        content = fd.read()
        fd.close()
        return content
    
    def writeFile(self, mydir,filepath,content):
        newfile = os.path.join(mydir,filepath)
        fd = open(newfile,'w')
        fd.write(content)
        fd.close()
        return newfile
    
    def readLines(self,mydir,filepath):
        fd = open(os.path.join(mydir,filepath),'r')
        content = fd.read()
        contentlist = content.split('\n')
        return contentlist
    
    def getArgPairs(self, args,separator):
        ret = dict()
        for pairs in args:
            argPair = pairs.split(separator)
            if len(argPair) > 1:
                ret[argPair[0]] = argPair[1]
        return ret

    
    def logClass(self, name,logpath):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s: %(Levelname)-8s %(message)s',
            datefmt = '%m-%d-%y %H:%M',filename=logpath, filemode='w')  
        log = logging.getLogger(name)
        return log
        
    def stjohnsPdf(self,inputfolder,county):
        mydir = os.path.dirname(__file__)
        batchf = os.path.join(mydir,'batchfiles/stjohns.bat')
        command = batchf+" "+str(inputfolder)+" "+county
        os.system(command)
        