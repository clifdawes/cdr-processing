'''
Created on June 24, 2018

@author: DawesC
'''

import pyodbc 
from fileLayout import BigRiverFileLayout
import ConfigParser
from CDRParcer import CDRParser
import os
import logging
from logging.handlers import RotatingFileHandler
import sys
from datetime import datetime

log = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s| %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
rotatingHandler = RotatingFileHandler('bigrivercdr.log', maxBytes=1500*1024, backupCount=5 )
rotatingHandler.setFormatter(formatter)
consoleHandler = logging.StreamHandler(sys.stdout)
log.addHandler(consoleHandler)
log.addHandler(rotatingHandler)
log.setLevel(logging.INFO)

class BigRiverParser(CDRParser):

    def __init__(self, filename, delimiter, headerRow):
        CDRParser.__init__(self, filename, delimiter, headerRow)
        
        
    def saveCDRtoDB(self, data):
        
        conn = pyodbc.connect(self._driver + "server="+ self._dbServer+"; database="+ self._database+"; UID="+ self._UID + "; PWD="+ self._PWD +";")
        #conn = pyodbc.connect(self._driver + "server="+ self._dbServer+"; database="+ self._database+"; trusted_connection=yes")
        cursor = conn.cursor()
        insert_date = datetime.strftime(datetime.now(), '%Y%m%d %H:%M:%S')
        result = []
        rownum = 0

        log.info('Processing '+ self.filename + '............')

        for rs in data:
            layoutParams = [rs[0],rs[1],rs[2],rs[3],rs[4],rs[5],rs[6],rs[7],rs[8],rs[9],rs[10],rs[11],rs[12],rs[13],rs[14],rs[15],rs[16].rstrip('\n'),insert_date]
            rownum +=1

            if len(rs[0]) > 40:
                log.error('Input Processing Error: '+ str(layoutParams)+'\n')
            else:
                mlayout = BigRiverFileLayout(layoutParams)
                result.append(mlayout.toList())
             
               
            
        baseSQL = ("Insert into dbo.BigRiverCDR(subscriber_id, call_date, call_time, called_from, called_to,"
                   " call_city, call_state, duration, amount, state_tax, federal_tax, usf, usage_description,"
                   " rated_date, account_code, toll_free_number, country_code, insert_date)" 
                   " Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

        log.info('Inserting '+str(rownum)+' rows into database '+ self._database)
        cursor.executemany(baseSQL, result)
        conn.commit()
        print('Completed database insert!')
        cursor.close()
        conn.close()
        
        #==========================================================================
        #Rename the just processed file to indicate the file has been processed.
        os.rename(self.filename, os.path.splitext(self.filename)[0]+'.DONE')
        
        log.info('Processing completed for ' + self.filename +'!')
        log.info('=====================================================================================================')


def startProcess(cdrlist):
    log.info('Starting Big River CDR file processing....' )
    for cdrFile in cdrlist:
        bParcer = BigRiverParser(cdrFile,',', False)
        bParcer.parse()


def checkForCDRFiles():
    config = ConfigParser.ConfigParser()
    config.read('NewWaveCDRProcessing.cfg')
    bigriver_dir = config.get('filelocation', 'bigriver_dir')

    brFilesToProcess = []
    bfiles = os.listdir(bigriver_dir)

    
    for b_cdrs in bfiles:
        if os.path.splitext(b_cdrs)[1] == '.CSV':
            brFilesToProcess.append(bigriver_dir+b_cdrs)
    
    
    if len(brFilesToProcess) > 0: 
        startProcess(brFilesToProcess)
        log.info("Finished processing Big River CDR files!")
        log.info('=====================================================================================================\n\n')
    else:
        log.info('No Big River CDR files to process!')
        log.info('=====================================================================================================\n')
    
if __name__ == '__main__':
    checkForCDRFiles()

