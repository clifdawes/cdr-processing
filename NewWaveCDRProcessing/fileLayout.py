'''
Created on Jun 21, 2018

@author: DawesC
'''
from datetime import datetime

class BigRiverFileLayout:

    subscriberID = None
    callDate = None
    callTime = None
    ANI = None
    callTo = None
    city = None
    state = None
    duration = None
    amount = None
    stateTax = None
    federalTax = None
    USF = None
    UsageDescription = None
    ratedDate = None
    accountCode = None
    tollFreeNumber = None
    countryCode = None
    insertdate = None


    def __init__(self, params):
        '''
        Constructor
        '''
        if len(params) != 0:
            self.subscriberID = params[0]
            dt = datetime.strptime(params[1], '%m%d%Y').date()
            self.callDate = dt.strftime('%Y-%m-%d')

            if (params[2][8:9]) == 'P':
                call_hour = int(params[2][0:2])
                if call_hour in range(1,12):
                    self.callTime = self.__convertTo24HourTime__(params[2])
                else:
                    self.callTime = params[2][0:8]
            else:
                self.callTime = params[2][0:8]
                    
            self.ANI = params[3]
            self.callTo = params[4]
            self.city = params[5]
            self.state = params[6]
            self.duration = params[7]
            self.amount = params[8]
            self.stateTax = params[9]
            self.federalTax = params[10]
            self.USF = params[11]
            self.UsageDescription = params[12]
            self.ratedDate = params[13]
            self.accountCode = params[14]
            self.tollFreeNumber = params[15]
            self.countryCode = params[16]
            self.insertdate = params[17]
        
        
    def __convertTo24HourTime__(self, val):
        call_hour = int(val[0:2])
        call_hour +=12
        call_minute = val[3:5]
        call_second = val[6:8]
        call_time = str(call_hour)+':'+call_minute+':'+call_second
        return call_time

    
    def layout(self):
        print(self.subscriberID, self.callDate, self.callTime, self.ANI, self.callTo, self.city, self.state, self.duration, self.amount, self.stateTax, self.federalTax,
              self.USF, self.UsageDescription, self.ratedDate, self.accountCode, self.tollFreeNumber, self.countryCode, self.insertdate)
        
    def toList(self):
        
        layoutList = (self.subscriberID, self.callDate, self.callTime, self.ANI, self.callTo, self.city, self.state, self.duration, self.amount, self.stateTax, self.federalTax,
              self.USF, self.UsageDescription, self.ratedDate, self.accountCode, self.tollFreeNumber, self.countryCode, self.insertdate)

        return layoutList
    
        
class MomemtumFileLayout:
    
    subscriber = None
    clientSubscriberNo = None
    systemID = None
    serviceProvider = None
    callDate = None
    callTime = None
    ANI = None
    telNo = None
    durationSeconds = None
    cashBalanceUsed = None
    minuteBalUsed = None
    planCode = None
    callBillingType = None
    callDirection = None
    callCity = None
    callState = None
    callCountry = None
    insertdate = None

    
    def __init__(self, params):
        if len(params) != 0:
            self.subscriber = params[0]
            self.clientSubscriberNo = params[1]
            self.systemID = params[2]
            self.serviceProvider = params[3]
            self.callDate = params[4]
            self.callTime = params[5]
            self.ANI = params[6].lstrip('1')
            self.telNo = params[7].lstrip('1')
            self.durationSeconds = params[8]
            self.cashBalanceUsed = params[9]
            self.minuteBalUsed = params[10]
            self.planCode = params[11]
            self.callBillingType = params[12]
            self.callDirection = params[13]
            self.callCity = params[14]
            self.callState = params[15]
            self.callCountry = params[16]
            self.insertdate = params[17]
            
    def layout(self):
        print(self.subscriber, self.clientSubscriberNo, self.systemID, self.serviceProvider, self.callDate,
              self.callTime, self.ANI, self.telNo, self.durationSeconds, self.cashBalanceUsed, self.minuteBalUsed,
              self.planCode, self.callBillingType, self.callDirection, self.callCity, self.callState, self.callCountry, self.insertdate)
        
    def toList(self):
        layoutList = (self.subscriber, self.clientSubscriberNo, self.systemID, self.serviceProvider, self.callDate,
              self.callTime, self.ANI, self.telNo, self.durationSeconds, self.cashBalanceUsed, self.minuteBalUsed,
              self.planCode, self.callBillingType, self.callDirection, self.callCity, self.callState, self.callCountry, self.insertdate)    
        
        return layoutList