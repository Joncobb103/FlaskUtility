import random
from Utils import Utils
import os
import sys
mydir = os.path.dirname(__file__)

util = Utils()

def knapsack(addem,curlist,seek):
    total = 0
    for i in addem:
        curlist.append(i)
        total+=float(i)
        if total == seek:
            print str(total)+ ' == '+ str(seek) +'\nList: '+str(curlist)
            return True
        elif total > seek:
            return False

def stjohnsdict(inputfolder,seeklist,outfolder,county):
    content = util.readLines(mydir, county+".txt")
    totdict = dict()
    addem = list()
    fwcontent = str()
    for line in content:
        if "@" in line:
            line_split = line.split("@")
            totdict[line_split[0]] = line_split[1]
            addem.append(line_split[0])
    curlist = list()
    random.shuffle(addem)
    filelist =[]
    
    for seek in seeklist:
        curlist = []
        statustot = False
        statustot = knapsack(addem,curlist,seek)
        
        while statustot == False:
            curlist = []
            random.shuffle(addem)
            statustot = knapsack(addem,curlist,seek)
        
        for tot in curlist:
            if tot in addem:
                addem.remove(tot)
        
        fwcontent = ""
        for line in curlist:
            fwcontent += totdict.get(line) + "\n"
        filepath = outfolder+"\\"+county+str(seek)+".txt"
        filelist.append(os.path.join(mydir,filepath))
        util.writeFile(mydir, filepath, fwcontent)
        fwcontent = ""
        for line in addem:
            fwcontent += line + "@" +totdict.get(line) + "\n"
        filepath = county+".txt"
#         print fwcontent
        util.writeFile(mydir, filepath, fwcontent)
    return filelist


# other = [42494.87,46907.22]
# argsm = sys.argv[1:]
# argMap = Utils().getArgPairs(argsm, "=")
# inputfolder = argMap.get('folder')
# util.stjohnsPdf(inputfolder)
# 
# remaining = stjohnsdict(inputfolder, other) 
# print remaining

#[1639.21, 1121.28, 1426.2, 900.38, 1340.41, 1695.37, 9081.12, 7344.09, 630.75, 2893.97, 3265.89, 312.53]