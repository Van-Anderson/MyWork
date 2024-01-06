#Created by Van Anderson using pyqt, background created with turtle

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
import configparser
from time import sleep

class cityWeather():
    APIKey=''
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
            weatherPayload={'lat':self.latitude,'lon':self.longitude,'appid': self.APIKey}
            weatherAPI= requests.get("https://api.openweathermap.org/data/2.5/weather", params=weatherPayload)
            data=weatherAPI.json()
            self.cityName=data['name']
            self.countryCode=data['sys']['country']
            self.latitude=data['coord']['lat']
            self.longitude=data['coord']['lon']
            self.updateTemp()
    def setNewCity(self,inputCityName,inputStateCode,inputCountryCode):
        searchLimit=1
        locationPayload={'q':inputCityName+','+inputStateCode+','+inputCountryCode,'limit':searchLimit,'appid':self.APIKey}
        cityAPI=requests.get("http://api.openweathermap.org/geo/1.0/direct", params=locationPayload)
        data=cityAPI.json()
        config['Location']['cityName']=inputCityName
        config['Location']['stateCode']=inputStateCode
        config['Location']['countryCode']=inputCountryCode
        with open('weatherAppConfig.ini', 'w') as configfile:
            config.write(configfile)
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
        weatherPayload={'lat':self.latitude,'lon':self.longitude,'appid': self.APIKey}
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
                '\nThe high is currently: '+str(self.highTemp)+'\nThe low is currently: '+str(self.lowTemp)+''+self.sunRiseOrSet())
        else:
            return('City: '+self.cityName+'\nCountry: '+self.countryCode +
                '\nLatitude: '+str(round(self.latitude,3))+'\u00b0 \nLongitude: '+str(round(self.longitude,3))+'\u00b0\nCurrent temperature is: '+str(self.currentTemp)+
                '\nThe high is currently: '+str(self.highTemp)+'\nThe low is currently: '+str(self.lowTemp)+ self.sunRiseOrSet())
    
    def updateAPI(self,newAPIKey):
        self.APIKey=newAPIKey
        config['Settings']['APIKey']=newAPIKey
        with open('weatherAppConfig.ini', 'w') as configfile:
            config.write(configfile)
        
    def getAPIKey(self):
        return self.APIKey

class Backend(QObject):
    def __init__(self):
        QObject.__init__(self)
          
    updated = pyqtSignal(str, arguments=['updater'])
    
    @pyqtSlot(str,str,str)
    def updateCity(self, cityText, stateText, countryText):
        if(current.APIKey!=''):
            if(cityText):
                current.setNewCity(cityText,stateText,countryText)
                self.updater(current.displayWeather())
            else:
                self.updater("A city is required input")
        #print(cityText)
        #print(stateText)
        #print(countryText)
    
    @pyqtSlot(str)
    def updateAPI(self, newKey):
        #print(newKey)
        current.updateAPI(newKey)
        
    def updater(self, cur_temp):
        #print(cur_temp)
        self.updated.emit(cur_temp)

    def bootUp(self):
        t_thread = threading.Thread(target=self._bootUp)
        t_thread.daemon = True
        t_thread.start()

    def _bootUp(self):
        while True:
            if(current.APIKey!=''):
                current.updateTemp()
                self.updater(current.displayWeather())
                #print(current.displayWeather())
                #print('update occured')
            else:
                self.updater("Currently no API key is present. Please sign up at openweathermap.com and input your key into the settings tab in the top right. API key activation can take several minutes.")
            sleep(60)





current=cityWeather()
config= configparser.ConfigParser()
config.read('weatherAppConfig.ini')
current.APIKey=config['Settings']['APIKey']
current.setNewCity(config['Location']['cityName'],config['Location']['stateCode'],config['Location']['countryCode'])
QQuickWindow.setSceneGraphBackend('software')
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./main.qml')
back_end=Backend()
engine.rootObjects()[0].setProperty('temp', current.displayWeather())
engine.rootObjects()[0].setProperty('backend', back_end)


back_end.bootUp()
sys.exit(app.exec())






