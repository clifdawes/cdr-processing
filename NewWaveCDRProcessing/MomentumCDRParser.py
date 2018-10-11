'''
Created on June 24, 2018

@author: Clif Dawes
'''
import pyodbc 
import logging
from logging.handlers import RotatingFileHandler
from fileLayout import MomemtumFileLayout
import ConfigParser
from CDRParcer import CDRParser
import os
import sys
from datetime import datetime


log = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s| %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
rotatingHandler = RotatingFileHandler('momentumcdr.log', backupCount=5, maxBytes=1500*1024)
rotatingHandler.setFormatter(formatter)
rotatingHandler.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler(sys.stdout)
log.addHandler(consoleHandler)
log.addHandler(rotatingHandler)
log.setLevel(logging.INFO)

class MomentumCDRParser(CDRParser):
    
    def __init__(self, filename, delimiter, headerRow):
        CDRParser.__init__(self, filename, delimiter, headerRow)

    def saveCDRtoDB(self, data):
        
        conn = pyodbc.connect(self._driver + "server="+ self._dbServer+"; database="+ self._database+"; UID="+ self._UID + "; PWD="+ self._PWD +";")
        #conn = pyodbc.connect(self._driver + "server="+ self._dbServer+"; database="+ self._database+"; trusted_connection=yes")
        cursor = conn.cursor()
        result = []
        insert_date = datetime.strftime(datetime.now(), '%Y%m%d %H:%M:%S')
        log.info('Processing '+ self.filename + '............')
        rownum = 0
        for rs in data:
            layoutParams = [rs[0],rs[1],rs[2],rs[3],rs[4],rs[5],rs[6],rs[7],rs[8],rs[9],rs[10],rs[11],rs[12],rs[13],rs[14],rs[15],rs[16].rstrip('\n'),insert_date]
            rownum +=1

            if len(rs[6]) > 40:
                log.error('Input Processing Error: '+ str(layoutParams)+'\n')
            else:
                mlayout = MomemtumFileLayout(layoutParams)
                result.append(mlayout.toList())
                
             
        baseSQL = ("Insert into dbo.MomentumCDR(subscriber_id, client_subscriber_no,"
                    " system_id, service_provider, call_date, call_time, ani, dest_Number,"
                    " duration_sec, cash_balance_used, minute_bal_used, plan_code, call_billing_type,"
                    " call_direction, call_city, call_state, call_country, insert_date)" 
                    " Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")


        try:
            log.info('Inserting '+ str(rownum) +' rows into database '+ self._database)
            cursor.executemany(baseSQL, result)
        except:
            log.info('Unable to upload data for '+ self.filename)
            
        conn.commit()
        print('Completed database insert!')
        cursor.close()
        #inputFile.close()
        conn.close()
        #==========================================================================
        #Rename the just processed file to indicate the file has been processed.
        os.rename(self.filename, os.path.splitext(self.filename)[0]+'.done')
        log.info('Processing completed for ' + self.filename +'!')
        log.info('=====================================================================================================')
        

def startProcess(cdrlist):
    log.info('Starting Momentum CDR files processing...')
    for cdrFile in cdrlist:    
        mParcer = MomentumCDRParser(cdrFile, '\t', True)
        mParcer.parse()



def checkForCDRFiles():
    config = ConfigParser.ConfigParser()
    config.read('NewWaveCDRProcessing.cfg')
    momentum_dir = config.get('filelocation', 'momentum_dir')

    moFilesToProcess = []
    
    mfiles = os.listdir(momentum_dir)

    for m_cdrs in mfiles:
        if os.path.splitext(m_cdrs)[1] == '.txt':
            moFilesToProcess.append(momentum_dir+m_cdrs)
    
    if len(moFilesToProcess) > 0: 
        startProcess(moFilesToProcess)
        log.info('Finished processing Momentum CDR files!')
        log.info('=====================================================================================================\n\n')
    else:
        log.info('No Momentum CDR files to process!')
        log.info('=====================================================================================================\n\n')



if __name__ == '__main__':
    checkForCDRFiles()

