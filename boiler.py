#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

import os
import time
import RPi.GPIO as GPIO


# Configuration des PIN
LedPin          = 4
BtnPinPlus      = 21
BtnPinMoins     = 17
lcd             = Adafruit_CharLCD(26,19,[13, 06, 05, 11])


# Constantes
chaudiere       = 0
chaudiereM      = 'OFF'
temperatureReglage = 42


# Temperature de la sonde
def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))


# Recuperation de la température réglé pour l'heure actuelle
def getTemperatureReglage():
        global temperatureReglage
        return temperatureReglage


def TemperaturePonctuellePlus(channel):
        global temperatureReglage
        temperatureReglage = temperatureReglage + 1
        print('test')


def TemperaturePonctuelleMoins(channel):
        global temperatureReglage
        temperatureReglage = temperatureReglage - 1

def setChaudiere(valeur):
        global chaudiere
        global chaudiereM

        chaudiere = valeur

        if(chaudiere==1):
                chaudiereM = 'ON'
                GPIO.output(LedPin, GPIO.HIGH)
        else:
                chaudiereM = 'OFF'
                GPIO.output(LedPin, GPIO.LOW)


def setup():
        
        GPIO.setmode(GPIO.BCM)
        
        ### LED Chaudiere
        GPIO.setup(LedPin,GPIO.OUT)

        ### Button Plus
        GPIO.setup(BtnPinPlus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BtnPinPlus, GPIO.FALLING, callback=TemperaturePonctuelleMoins)

        ### Button Moins
        GPIO.setup(BtnPinMoins, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        ### LCD
        lcd.begin(16, 1)
        

# Setup
setup()

# Run
try:
        while True:

                if str(getCPUtemperature()) > str(getTemperatureReglage()):
                        setChaudiere(0)
                        
                # Extinction chaudiere    
                else:
                        setChaudiere(1)
                        
                lcd.clear()
                lcd.message(time.strftime('%d %b  %H:%M:%S\n', time.localtime()))
                lcd.message(getCPUtemperature()+'/'+str(getTemperatureReglage())+'     '+str(chaudiereM))
                sleep(0.5)

# Stop on Ctrl+C and clean up
except KeyboardInterrupt:
        GPIO.cleanup()

