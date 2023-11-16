import requests
import json
import time
import sys
import os
from PyQt6.QtGui import QGuiApplication,QMouseEvent
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import threading
from time import sleep

APIKey='95c63f75de3e5bed395d44378752f62f'


class cityWeather():
    latitude=0
    longitude=0
    cityName=''
    stateCode=''
    countryCode=''
    currentTemp=0
    highTemp=0
    lowTemp=0
    sunrise=0
    sunset=0
    def __init__(self,lat=0,long=0,):
        self.latitude=lat
        self.longitude=long
        if lat!=0 and long!=0:
            weatherPayload={'lat':self.latitude,'lon':self.longitude,'appid': APIKey}
            weatherAPI= requests.get("https://api.openweathermap.org/data/2.5/weather", params=weatherPayload)
            data=weatherAPI.json()
            self.cityName=data['name']
            self.countryCode=data['sys']['country']
            #self.stateCode=data['sys']['state']
            self.latitude=data['coord']['lat']
            self.longitude=data['coord']['lon']
            self.updateTemp()
    def setNewCity(self):
        inputCityName=input("Enter Your City: ")
        inputStateCode=input("Enter Your State: ")
        inputCountryCode=input("Enter Your Country: ")
        searchLimit=1
        locationPayload={'q':inputCityName+','+inputStateCode+','+inputCountryCode,'limit':searchLimit,'appid':APIKey}
        cityAPI=requests.get("http://api.openweathermap.org/geo/1.0/direct", params=locationPayload)
        data=cityAPI.json()
        try:
            self.cityName=data[0]['name']
            self.stateCode=data[0]['state']
            self.countryCode=data[0]['country']
            self.latitude=data[0]['lat']
            self.longitude=data[0]['lon']
            self.updateTemp()
        except (IndexError, KeyError):
            print("Location Not Found")
        

    def updateTemp(self):
        weatherPayload={'lat':self.latitude,'lon':self.longitude,'appid': APIKey}
        weatherAPI= requests.get("https://api.openweathermap.org/data/2.5/weather", params=weatherPayload)
        data=weatherAPI.json()
        self.currentTemp=int((float(data['main']['temp']) - 273.15) * 1.8 + 32)
        self.lowTemp=int((float(data['main']['temp_min']) - 273.15) * 1.8 + 32)
        self.highTemp=int((float(data['main']['temp_max']) - 273.15) * 1.8 + 32)
        self.sunrise=data['sys']['sunrise']
        self.sunset=data['sys']['sunset']

    def sunRiseOrSet(self):
        hours=0
        minutes=0
        curTime=time.time()
        if(curTime<self.sunrise):
            hours=int((self.sunrise-curTime)/3600)
            minutes=int((self.sunrise-curTime)%3600/60)
            return('\nThe sun will rise in: '+str(hours)+' Hours & '+str(minutes)+' Minutes')
        elif(curTime>self.sunrise and curTime<self.sunset):
            hours=int((self.sunset-curTime)/3600)
            minutes=int((self.sunset-curTime)%3600/60)
            return('\nThe sun will set in: '+str(hours)+' Hours & '+str(minutes)+' Minutes')
        else:
            hours=int((curTime-self.sunset)/3600)
            minutes=int((curTime-self.sunset)%3600/60)
            return('\nThe sun set: '+str(hours)+' Hours & '+str(minutes)+' Minutes ago')
             


    def displayWeather(self):
        if(self.stateCode):
            return('City: '+self.cityName+'\nState: '+self.stateCode+'\nCountry: '+self.countryCode +
                '\nLatitude: '+str(round(self.latitude,3))+'\u00b0 \nLongitude: '+str(round(self.longitude,3))+'\u00b0\nCurrent temperature is: '+str(self.currentTemp)+
                '\nThe high is currently: '+str(self.highTemp)+'\nThe low is currently: '+str(self.lowTemp)+'\n'+self.sunRiseOrSet())
        else:
            return('City: '+self.cityName+'\nCountry: '+self.countryCode +
                '\nLatitude: '+str(round(self.latitude,3))+'\u00b0 \nLongitude: '+str(round(self.longitude,3))+'\u00b0\nCurrent temperature is: '+str(self.currentTemp)+
                '\nThe high is currently: '+str(self.highTemp)+'\nThe low is currently: '+str(self.lowTemp)+ self.sunRiseOrSet())
        #print(self.sunRiseOrSet())

class Backend(QObject):
    def __init__(self):
        QObject.__init__(self)
        
        
    updated = pyqtSignal(str, arguments=['updater'])
    

    #TODO: POSSIBLY MAKE TWO MORE TEXT FIELDS THAT CONNECT TO THE BUTTON... MAKE THIS CALL THE UPDATE CITY METHOD... THEN CALL THE UPDATER
    #CHANGE THE NEWCITY METHOD TO TAKE PARAMETERSINSTEAD THANK YOU AMOH
    @pyqtSlot(str)
    def text(self, usertext):
        print(usertext)
    

    def updater(self, cur_temp):
        print(cur_temp)
        self.updated.emit(cur_temp)

    def bootUp(self):
        t_thread = threading.Thread(target=self._bootUp)
        t_thread.daemon = True
        t_thread.start()

    def _bootUp(self):
        while True:
            current.updateTemp()
            self.updater(current.displayWeather())
            #print(current.displayWeather())
            print('update occured')
            sleep(60)



#current =cityWeather(40.5,-88.98)
#current =cityWeather(40.5,-88.98)
current=cityWeather()
#current.displayWeather()
current.setNewCity()
#paris=cityWeather()
#paris.setNewCity()
#current.displayWeather()
#paris.displayWeather()
#print(temp)

QQuickWindow.setSceneGraphBackend('software')
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

engine.load('./UI/main.qml')
back_end=Backend()
engine.rootObjects()[0].setProperty('temp', current.displayWeather())
engine.rootObjects()[0].setProperty('backend', back_end)



back_end.bootUp()
sys.exit(app.exec())






