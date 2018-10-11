'''
Created on Jul 21, 2018

@author: DawesC
'''
import pyodbc 
from datetime import datetime
from ConfigParser import ConfigParser

class TrailerRecord():
    record_type = ''
    record_total = ''
    amount_total = ''
    
    def __init__(self, rtype, records, amount):
        self.record_type = rtype
        self.record_total = records
        self.amount_total = amount
    
    
class PhoneUsageRecord():
    trans_id = None
    cust_id = None
    entry_by = 'SUN'
    service_type = '1'
    service_category = '1'
    service_sub_category = None
    service_description = None
    begin_date = None
    begin_time = None
    end_date = None
    end_time = None
    duration = '0'
    amount = None


def validateDateEntered():
    
    try:
        startdate = input('Enter StartDate\nUse the following format:\'YYYY-MM-DD\'(example:\'2018-06-01\'): ')
#        sdate = startdate.split('-')
#        print(str(sdate[0]))
        enddate = input('Enter EndDate\nUse the following format:\'YYYY-MM-DD\'(example: \'2018-06-30\'): ')
#        print(enddate)

        createPhoneUsageRecord(startdate, enddate)
        #runCDRBillingSummary(startdate, enddate)
            
    except NameError:
        print('Invalid Date entered.')
    
        
    
def createPhoneUsageRecord(startdate, enddate):
    
    ''' check to determine if string entered (startdate, enddate) is a valid date'''
    
    '''
    Open database cursor to execute and read records from database
    As you read through the records create a Phone Usage Record and write the record to a CSV (comma separated) formatted file.
    '''

    cfg = ConfigParser()
    cfg.read("NewWaveCDRProcessing.cfg")
    database = cfg.get('sqlserver', 'database')
    server = cfg.get('sqlserver', 'server')
    uid = cfg.get('sqlserver', 'user')
    pwd = cfg.get('sqlserver', 'password')

    
    dt = datetime.strftime(datetime.today(),'%Y%m%d%H%M%S')

    conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};" "server=" + server + "; database="+ database +"; UID="+ uid + "; PWD="+ pwd +";")
    cursor = conn.cursor()
    cursor.execute('SELECT seqnum from dbo.FileSeq;')
    row = cursor.fetchall()
    int_inputArg = row[0][0]
    cursor.execute('UPDATE dbo.FileSeq set seqnum = seqnum + increment;')
    cursor.commit()
    
    seqNum ='{str_0:0>{str_1}}'.format(str_0=int_inputArg, str_1=5)
    phonerecord = open('PHONE'+'_'+ dt +'_'+ seqNum+'.dat', 'w')
    controlrecord0 = open('PHONE'+'_'+ dt +'_'+ seqNum+'.dat.done', 'w')

    vals = (startdate, enddate)

    cursor.execute("EXEC dbo.spGetBigRiverPhoneCharges @start_date = ?, @end_date = ?", vals)
    rows = cursor.fetchall()
    record_count = 0
    amount_total = 0
    for row in rows:
        pur = PhoneUsageRecord()
        pur.trans_id = row[0]
        pur.cust_id = row[1]
        pur.entry_by = row[2]
        pur.service_type = row[3]
        pur.service_category = row[4]
        pur.service_sub_category = row[5]
        pur.service_description = row[6]
        pur.begin_date = row[7]
        pur.begin_time = '00:00'
        pur.end_date = row[8]
        pur.end_time = '00:00'
        pur.duration = row[9]
        pur.amount = row[10]
        
        try:
            phonerecord.write(str(pur.trans_id) +','+ str(pur.cust_id) +','+ pur.entry_by + ','+ 
                          str(pur.service_type)+','+ str(pur.service_category)+','+ str(pur.service_sub_category) + 
                          ','+ pur.service_description + ','+ datetime.strftime(pur.begin_date, '%m/%d/%Y')+ ',' + 
                          pur.begin_time + ',' + datetime.strftime(pur.end_date, '%m/%d/%Y')+ ','+ pur.end_time +
                          ',' + str(pur.duration) + ',' + str(pur.amount) +'\n')
        except:
            phonerecord.close() 
        
        record_count+=1
        amount_total += pur.amount

    
    
    tr = TrailerRecord('T', str(record_count), str(amount_total))
    phonerecord.write(tr.record_type+','+ tr.record_total+','+ tr.amount_total+'\n')
    phonerecord.close()
    controlrecord0.close()
        


    cursor.execute('SELECT seqnum from dbo.FileSeq;')
    row = cursor.fetchall()
    int_inputArg = row[0][0]
    cursor.execute('UPDATE dbo.FileSeq set seqnum = seqnum + increment;')
    cursor.commit()
    
    seqNum ='{str_0:0>{str_1}}'.format(str_0=int_inputArg, str_1=5)
    phonerecord = open('PHONE'+'_'+ dt +'_'+ seqNum+'.dat', 'w')
    controlrecord1 = open('PHONE'+'_'+ dt +'_'+ seqNum+'.dat.done', 'w')
    vals = (startdate, enddate)

    cursor.execute("EXEC dbo.spGetMomentumPhoneCharges @start_date = ?, @end_date = ?", vals)
    rows = cursor.fetchall()
    record_count = 0
    amount_total = 0
    for row in rows:
        pur = PhoneUsageRecord()
        pur.trans_id = row[0]
        pur.cust_id = row[1]
        pur.entry_by = row[2]
        pur.service_type = row[3]
        pur.service_category = row[4]
        pur.service_sub_category = row[5]
        pur.service_description = row[6]
        pur.begin_date = row[7]
        pur.begin_time = '00:00'
        pur.end_date = row[8]
        pur.end_time = '00:00'
        pur.duration = row[9]
        pur.amount = row[10]
        
        try:
            phonerecord.write(str(pur.trans_id) +','+ str(pur.cust_id) +','+ pur.entry_by + ','+ 
                          str(pur.service_type)+','+ str(pur.service_category)+','+ str(pur.service_sub_category) + 
                          ','+ pur.service_description + ','+ datetime.strftime(pur.begin_date, '%m/%d/%Y')+ ',' + 
                          pur.begin_time + ',' + datetime.strftime(pur.end_date, '%m/%d/%Y')+ ','+ pur.end_time +
                          ',' + str(pur.duration) + ',' + str(pur.amount) +'\n')
        except:
            phonerecord.close() 
        
        record_count+=1
        amount_total += pur.amount

    
    
    tr = TrailerRecord('T', str(record_count), str(amount_total))
    phonerecord.write(tr.record_type+','+ tr.record_total+','+ tr.amount_total+'\n')
    phonerecord.close()
    controlrecord1.close()
    
    cursor.close()
    conn.close()


def runCDRBillingSummary(startdate, enddate):
    
    cfg = ConfigParser()
    cfg.read("NewWaveCDRProcessing.cfg")
    database = cfg.get('sqlserver', 'database')
    server = cfg.get('sqlserver', 'server')
    uid = cfg.get('sqlserver', 'user')
    pwd = cfg.get('sqlserver', 'password')
    conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};" "server="+ server + "; database=" + database +"; UID="+ uid + "; PWD="+ pwd + ";")
    vals = (startdate, enddate)
    cursor = conn.cursor()

    
    
    cursor.execute("EXEC dbo.spSumBigRiverCDR @start_date = ?, @end_date = ?", vals)
    if cursor.rowcount > 0: 
        createPhoneUsageRecord(startdate, enddate)
    else:
        print('No records to process for current period!')
    

    cursor.execute("EXEC dbo.spSumMomentumCDR @start_date = ?, @end_date = ?", vals)
        
    cursor.close()
    conn.close()
    
    
    
    
          
    
if __name__ == '__main__':        
    validateDateEntered()