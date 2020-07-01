from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from zeep import Client
import xmltodict, json
from .models import Stock
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime, timedelta

class QatarExchange:
    __username = 'widam'
    __password = 'wid@2019#'
    __marketType = '510'
    __instrument = 'A'
    client = ''
    __wsdl = "https://www.qe.com.qa/Process/WSInterfaces/intf-ExchangeStats.serviceagent?wsdl"
    __endpoint = "https://www.qe.com.qa/Process/WSInterfaces/intfExchangeStatsEnquiry-service.serviceagent/intf-ExchangeStatsEp"
    
    def __init__(self):
        self.connectToServer();
    def connectToServer(self):
        self.client = Client(wsdl=self.__wsdl)
        self.client.service._binding_options["address"] = self.__endpoint
        print("To server connected")
        return True
    def toJson(self,data):
        o = xmltodict.parse(data['OPRESULT'])
        c = json.loads(json.dumps(o))
        main = c['ns0:BAG']['ns0:INSTRUMENT']
        data = {
            'SYM':main['ns0:SYM'],
            'PCL':float(main['ns0:PCL']),
            'OPN':float(main['ns0:OFR']),
            'OFR':float(main['ns0:OFR']),
            'OFRVOL':float(main['ns0:OFRVOL']),
            'BID':float(main['ns0:BID']),
            'BIDVOL':float(main['ns0:BIDVOL']),
            'CUR':float(main['ns0:CUR']),
            'TRND':main['ns0:TRND'],
            'VOL':float(main['ns0:VOL']),
            'VAL':float(main['ns0:VAL']),
            'HIGH':float(main['ns0:HIGH']),
            'LOW':float(main['ns0:LOW']),
            'NCHN':float(main['ns0:NCHN']),
            'W52H':float(main['ns0:W52H']),
            'W52L':float(main['ns0:W52L']),
            'MCAP':float(main['ns0:MCAP']),
            'STATTIME':main['ns0:STATTIME'],
        }
        Stock.objects.create(BID=data['BID'],BIDVOL=data['BIDVOL'],CUR=data['CUR'],HIGH=data['HIGH'],LOW=data['LOW'],MCAP=data['MCAP'],TRND=data['TRND'])
        return data
    def getCurrentData(self):
        if(self.client == ''):
            self.connectToServer()
        # response =  self.client.service.OpInstruments(self.__username,self.__password,self.__instrument,self.__marketType)
        data = self.client.service.OpInstruments(self.__username,self.__password,self.__marketType,self.__instrument)
        return self.toJson(data)


main = QatarExchange()
def getData(request):
    response = main.getCurrentData()
    return JsonResponse(response,safe=False)

def one_hour(request):

    this_hour = datetime.now(tz=timezone.utc).replace(minute=0, second=0, microsecond=0)
    one_hour_later = this_hour + timedelta(hours=1)
    results = Stock.objects.filter(created_on__lt=(this_hour, one_hour_later))
    print(results)
    return JsonResponse("ok",safe=False)

def index(request):
    return render(request, 'index2.html')



