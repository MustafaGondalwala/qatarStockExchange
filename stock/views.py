from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from zeep import Client
import xmltodict, json
from .models import Stock
from django.utils.timezone import make_aware
from django.utils import timezone
from django.core import serializers
from datetime import datetime, timedelta
from django.db import connection


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
        from datetime import datetime, timedelta, timezone
        import time
        last_modified_string = round(int(round(time.time() * 1000)))
        Stock.objects.create(BID=data['BID'],BIDVOL=data['BIDVOL'],CUR=data['CUR'],HIGH=data['HIGH'],LOW=data['LOW'],MCAP=data['MCAP'],TRND=data['TRND'],last_modified_string=last_modified_string)
        return data
    def getCurrentData(self):
        if(self.client == ''):
            self.connectToServer()
        # response =  self.client.service.OpInstruments(self.__username,self.__password,self.__instrument,self.__marketType)
        data = self.client.service.OpInstruments(self.__username,self.__password,self.__marketType,self.__instrument)
        return self.toJson(data)

# main = QatarExchange()
def getData(request):
    main = QatarExchange()
    response = main.getCurrentData()
    return JsonResponse(response,safe=False)

def report(request):
    type = request.GET['type']
    hour_type = 0
    if(type == "1"):
        hour_type = 24
    elif(type == "2"):
        hour_type = 48
    elif(type == "3"):
        hour_type = 60
    elif(type == "15"):
        hour_type = 360
    elif(type == "30"):
        hour_type = 720
    elif(type == "60"):
        hour_type = 1440
    elif(type == "90"):
        hour_type = 2160
    elif(type == "182"):
        hour_type = 4368
    elif(type == "365"):
        hour_type = 8760

    from datetime import datetime, timedelta, timezone
    first_date = datetime.now().strftime('%Y-%m-%d')

    # print)

    last_hour_date_time = datetime.now() - timedelta(hours = hour_type)
    last_hour_date_time = last_hour_date_time.strftime('%Y-%m-%d')
    print(first_date,last_hour_date_time)
    data = Stock.objects.filter(created_on__range=(last_hour_date_time,first_date)).values().order_by('-created_on')
    return JsonResponse(list(data),safe=False)
def index(request):
    return render(request, 'index2.html')




def currentprice(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT AVG(last_modified_string) as last_modified_string,AVG(CUR) as CUR from stock_stock GROUP BY created_on")
        row = cursor.fetchall()
    return JsonResponse(row,safe=False)

def volume(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT ROUND(AVG(last_modified_string)) as last_modified_string,AVG(MCAP) as MCAP from stock_stock GROUP BY created_on")
        row = cursor.fetchall()
    return JsonResponse(row,safe=False)
def mainpage(request):
    return render(request, 'web.html')


main = QatarExchange()
def top10(request):
    top10Data = Stock.objects.all()[:10].values()
    response = main.getCurrentData()
    return JsonResponse({"top10Data":list(top10Data),'mcap':response['MCAP'],'volume':response['VOL']},safe=False)
def all(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT AVG(BID) as BID,AVG(HIGH) as HIGH,AVG(LOW) as LOW,AVG(MCAP) as MCAP, FLOOR(AVG(last_modified_string)) as last_modified_string from stock_stock GROUP BY created_on ORDER BY last_modified_string ASC")
        row = cursor.fetchall()
    return JsonResponse(row,safe=False)