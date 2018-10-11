'''
Created on Jul 17, 2018

@author: DAWESC
'''
import ConfigParser
from ftplib import FTP
import pysftp
import paramiko
import re
import os
from datetime import datetime
from datetime import timedelta

import BigRiverCDRParser

#==================================================================
#FTP download from BigRiver Communications
def downloadCDRS():
    
    config = ConfigParser.ConfigParser()
    config.read('NewWaveCDRProcessing.cfg')
    bigriver_ftp_host = config.get('filelocation', 'bigriver_ftp_host')
    bigriver_ftp_user = config.get('filelocation', 'bigriver_ftp_user')
    bigriver_ftp_password= config.get('filelocation', 'bigriver_ftp_password')
    tdelta = timedelta(days=-60)
    
    yearmonth = datetime.strftime(datetime.today()+tdelta,'%Y%m')

    pattern = re.compile(r'NEWWAVECDR'+yearmonth+'\d{2}.CSV')
    
    
    ftps = FTP(bigriver_ftp_host)
    ftps.login(bigriver_ftp_user, bigriver_ftp_password)
    cdrs = ftps.nlst()
    
    for cdr in cdrs:
        match = pattern.match(cdr)
        if match:
            localfile = os.path.join(r"c:\\Call Detail Records\\Big River\\August 2018\\",cdr)
            lf = open(localfile,"wb")
            ftps.retrbinary("RETR " + cdr, lf.write, 8*1024)
            lf.close()
            print(match.group())
        
    ftps.quit()
    BigRiverCDRParser.checkForCDRFiles()

def downloadCDRSSecure():
    config = ConfigParser.ConfigParser()
    config.read('NewWaveCDRProcessing.cfg')
    momentum_ftp_host = config.get('filelocation', 'momentum_ftp_host')
    momentum_ftp_user = config.get('filelocation', 'momentum_ftp_user')
    momentum_ftp_password= config.get('filelocation', 'momentum_ftp_password')

    cnotps = pysftp.CnOpts()
    cnotps.hostkeys = None
    with pysftp.Connection(host=momentum_ftp_host, username=momentum_ftp_user, password=momentum_ftp_password, cnotps=cnotps):
    
        data = pysftp.Connection.listdir()
    
        for i in data:
            print(i)

    
if __name__ == '__main__':
    downloadCDRS()
    #BigRiverCDRParser.checkForCDRFiles()
