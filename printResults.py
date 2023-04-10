import sys, getopt, os
import csv
from datetime import datetime
import matplotlib  
matplotlib.use('TkAgg')   
import matplotlib.pyplot as plt 

import base64
from io import BytesIO
import re
import shutil

def printResults(folderName):
    with open(inputFile, "r") as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        
        #print('HEADERS')
        #print(headers)
        #print(len(headers))
        data = {}
        for title in headers:
            data[title] = []
        for row in csv_reader:
            for i, title in enumerate(headers):
                data[title].append(row[i])
        #print(data)

    for i in range(len(data["INIT_EXEC_TIME"])):
        currentTimestamp = datetime.fromtimestamp(int(data["INIT_EXEC_TIME"][i])/1000)
        data["INIT_EXEC_TIME"][i] = currentTimestamp.strftime("%H:%M:%S")
    for i in range(len(data["TOTAL_TIME"])):
        data["TOTAL_TIME"][i] = float(data["TOTAL_TIME"][i])

    '''fig, ax = plt.subplots()
    ax.plot(data["INIT_EXEC_TIME"], data["TOTAL_TIME"])
    fig.autofmt_xdate()
    #plt.savefig(outputFile)
    plt.show()'''
    #fig = plt.figure()
    fig, ax = plt.subplots()
    ax.plot(data["INIT_EXEC_TIME"], data["TOTAL_TIME"])
    fig.autofmt_xdate()
    #plot sth

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html = 'Some html head' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + 'Some more html'

    with open('test.html','w') as f:
        f.write(html)

def readFile(inputFile):
    headers = []
    data = {}
    with open(inputFile, "r") as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        
        #print('HEADERS')
        #print(headers)
        #print(len(headers))
        for title in headers:
            data[title] = []
        for row in csv_reader:
            for i, title in enumerate(headers):
                data[title].append(row[i])
        #print(data)
    return headers, data

def getResultsByAgreement(folderName, experimentNumber):
    agreements = {}
    excludes = '|'.join(['.DS_Store', '\w*_havest.csv','\w*joined.csv'])
    for root, dirs, files in os.walk(folderName):
        dirs[:] = [d for d in dirs if not re.match(excludes, d)]
        files = [f for f in files if not re.match(excludes, f)]
        for file in files:
            #print(root)
            #print(file)
            if "_harvest" not in file and "_joined" not in file and "html" not in file:
                #print(file)
                agreementId = root.split('/')[-1:][0]
                
                pathFile = os.path.join(root, file)
                headers, data = readFile(pathFile)
                agreements[agreementId] = {
                    'headerFile' : headers,
                    'dataFile' : data
                }
    #print(agreements)
    return agreements

def joinResults(agreements):
    #print(agreements)
    totalESC = len(agreements)
    #print(totalESC)
    result = {}
    for agreementId in agreements:
        escNumber = agreementId.split('oti_gc_ans')[1]
        #print(escNumber)
        dataFile = agreements[agreementId]['dataFile']
        for i in range(len(dataFile['INIT_EXEC_TIME'])):
            timeStamp = dataFile['INIT_EXEC_TIME'][i]
            currentTimestamp = []
            if timeStamp in result:
                currentTimestamp = result[timeStamp]
            newData = {
                'escNumber' : int(escNumber),
                'agreementId' : agreementId,
                'totalTime' : float(dataFile['TOTAL_TIME'][i]),
                'analysisTime' : float(dataFile['ANALYSIS_TIME'][i]),
                'timeData' : float(dataFile['TIME_DATA'][i]),
                'frequencyData' : float(dataFile['FREQUENCY_DATA'][i])
            }
            currentTimestamp.append(newData)
            result[timeStamp] = currentTimestamp
    #print(result)
    return totalESC, result

def generateCSVJoined(totalNumberESC, agreementsJoined, savePath):
    header = ['TIMESTAMP']
    for i in range(totalNumberESC):
        escHeader = 'ESC_{0}_TotalTime,ESC_{0}_AnalysisTime,ESC_{0}_TimeData,ESC_{0}_FrequencyData'.format(i+1)
        header.extend(escHeader.split(','))
    #print('Header joined')
    #print(header)
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%dT%H-%M-%S")
    fileResultPath = savePath+now_str+'_joined.csv'
    with open(fileResultPath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for timeStamp in agreementsJoined:
            row = []
            dataTS = agreementsJoined[timeStamp]
            if totalNumberESC == len(dataTS):
                for agreement in dataTS:
                    row.append(agreement['totalTime'])
                    row.append(agreement['analysisTime'])
                    row.append(agreement['timeData'])
                    row.append(agreement['frequencyData'])
            else:
                existESC = []
                existingAgreement = {}
                for agreement in dataTS:
                    escNumber = agreement['escNumber']
                    existESC.append(escNumber)
                    agreementData = []
                    agreementData.append(agreement['totalTime'])
                    agreementData.append(agreement['analysisTime'])
                    agreementData.append(agreement['timeData'])
                    agreementData.append(agreement['frequencyData'])
                    existingAgreement[escNumber] = agreementData
                for i in range(totalNumberESC):
                    if i+1 in existESC:
                        row.extend(existingAgreement[i+1])
                    else:
                        row.extend([None,None,None,None])
            row.insert(0,timeStamp)
            writer.writerow(row)
    return fileResultPath

def generateAgreementGraphic(agreementId, agreement):
    data = agreement['dataFile']
    for i in range(len(data["INIT_EXEC_TIME"])):
        currentTimestamp = datetime.fromtimestamp(int(data["INIT_EXEC_TIME"][i])/1000)
        data["INIT_EXEC_TIME"][i] = currentTimestamp.strftime("%H:%M:%S")
    for i in range(len(data["TOTAL_TIME"])):
        data["TOTAL_TIME"][i] = float(data["TOTAL_TIME"][i])

    '''fig, ax = plt.subplots()
    ax.plot(data["INIT_EXEC_TIME"], data["TOTAL_TIME"])
    fig.autofmt_xdate()
    #plt.savefig(outputFile)
    plt.show()'''
    #fig = plt.figure()
    fig, ax = plt.subplots()
    ax.plot(data["INIT_EXEC_TIME"], data["TOTAL_TIME"])
    ax.title.set_text(agreementId)
    fig.autofmt_xdate()
    #plot sth

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return encoded

def addAgreementGraphics(agreementsBase64Code, file):
    elements = []
    for agreementId in agreementsBase64Code:
        base64graphic = agreementsBase64Code[agreementId]
        graphicElement = "<div class=\"col-4\"><img class=\"img-fluid\" src=\"data:image/png;base64,{0}\"></div><!--AgreementsChart-->".format(base64graphic)
        #graphicElement = "<div class=\"col {0}\">".format(agreementId,base64graphic)
        elements.append(graphicElement)
    
    readFile = open(file, "r")
    data = readFile.read()
    data = data.replace('<!--AgreementsChart-->', '<br/>'.join(elements))
    writeFile = open(file, "w")
    writeFile.write(data)

    '''for agreementId in agreementsBase64Code:
        base64graphic = agreementsBase64Code[agreementId]
        with open(file,'rw') as f:
            for line in f:
                graphicElement = "<div class=\"col\"><img src=\"data:image/png;base64,{1}\"></div><!--AgreementsChart-->".format(agreementId,base64graphic)
                f.write(line.replace('<!--AgreementsChart-->', graphicElement))
                f.close()'''
    
    
    '''
    #html = 'Some html head' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + 'Some more html'
    #input file
    fin = open(file, "rt")
    #output file to write the result to
    fout = open(file, "w")
    #with open(file,'w') as f:
    for line in fin:
        #read replace the string and write to output file
        graphicElement = "<div class=\"col {0}\"><img src=\"data:image/png;base64,{1}\"></div><!--AgreementsChart-->".format(agreementId,base64graphic)
        fout.write(line.replace('<!--AgreementsChart-->', graphicElement))
        #f.write(html)'''


def main(argv):
    inputfolder = ''
    experimentNumber = ''
    opts, args = getopt.getopt(argv,"h:e:",["expnum="])
    for opt, arg in opts:
        if opt == '-h':
            print ('printResults.py -e <experiment number>')
            sys.exit()
        elif opt in ("-e", "--expnum"):
            experimentNumber = arg
    pathFolder = "experiments/experiments_results/{0}/".format(experimentNumber)
    print('Experiment number: {0}\nPath folder: {1}'.format(experimentNumber, pathFolder))

    # Dictionary. Key: agreement id; Value: {dataFile, headerFile}
    agreements = getResultsByAgreement(pathFolder, experimentNumber)
    # Join all agreements results by timestamp
    totalNumberESC, agreementsJoined = joinResults(agreements)
    # Create csv file with joined agreements
    joinedFilePath = generateCSVJoined(totalNumberESC, agreementsJoined, pathFolder)
    print('Agreements results joined in: {}'.format(joinedFilePath))

    graphicPath = pathFolder + 'graphicResult.html'
    shutil.copyfile('graphicResultTemplate.html', graphicPath)

    agreementGraphic = {}
    for agreementId in agreements:
        base64graphic = generateAgreementGraphic(agreementId, agreements[agreementId])
        agreementGraphic[agreementId] = base64graphic
    addAgreementGraphics(agreementGraphic,graphicPath)


    '''fig, ax = plt.subplots()
    testX = ['A', 'B', 'C', 'A', 'D']
    testY = [30, 20, 50, 100,10]
    ax.plot(testX, testY)
    fig.autofmt_xdate()
    #plt.savefig(outputFile)
    plt.show()'''

if __name__ == "__main__":
   main(sys.argv[1:])
