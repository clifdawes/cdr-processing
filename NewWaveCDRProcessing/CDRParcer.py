'''
Created on June 12, 2018

@author: DAWESC
'''
import ConfigParser


class CDRParser:
    rows = []
    _dbServer = None
    _database = None
    _UID = None
    _PWD = None
    _driver = None
    
    
    def __init__(self, filename, delimiter, headerRow):
        self.filename = filename
        self.delimiter = delimiter
        self.headerRow = headerRow
        cfg = ConfigParser.ConfigParser()
        cfg.read("NewWaveCDRProcessing.cfg")
        self._driver = cfg.get('sqlserver', 'driver')
        self._database = cfg.get('sqlserver', 'database')
        self._dbServer = cfg.get('sqlserver', 'server')
        self._UID = cfg.get('sqlserver', 'user')
        self._PWD = cfg.get('sqlserver', 'password')
        
    def parse(self):
        cdrFile = open(self.filename, 'r')
        del self.rows[:]
        #===============================================================
        # call to readline() method in order to skip header row.
        if self.headerRow:cdrFile.readline()  
        #===============================================
        for line in cdrFile:
            cdr = line.split(self.delimiter)
            self.rows.append(cdr)
        
        cdrFile.close()
        self.saveCDRtoDB(self.rows)


    def saveCDRtoDB(self, data):
        print(self.filename)
        print(data)
        

                
def createPhoneList():
    lineFile = open("c:\ICOMS Billing Migration\line_file.csv", 'r')
    l =[]
    lineFile.readline()
    for line in lineFile:
        phone = line.split('|')
        l.append(phone[4].strip('\n'))
    lineFile.close()
    
    phonenum = '2179429157'
    if phonenum in l:
        print('phone number: '+ phonenum + ' found!')
    
if __name__ == '__main__':
    createPhoneList()
    