#! /usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#poweron the RPI GSM SIM900 module
def PowerON_SIM900_module():
    #GPIO.setup(17,GPIO.OUT)
    #GPIO.output(17,GPIO.HIGH)
    return;

#poweron the relay
def PowerONRelay():
    GPIO.setup(22,GPIO.OUT);
    GPIO.output(22,GPIO.HIGH);
    return;

#poweroff the relay
def PowerOFFRelay():
    GPIO.setup(22,GPIO.OUT);
    GPIO.output(22,GPIO.LOW);
    return;

#check unread arrived messages
def CheckNewUnreadMessage(ser):
    print 'Check for new messages..\n';
    ser.write('at\r');
    time.sleep(3);
    line=ser.read(size=64);
    print line;
    ser.write('AT+CMGL="REC UNREAD"\r')
    #ser.write('AT+CMGL="ALL"\r')
    time.sleep(3);
    response=ser.read(size=2000);
    print response;
    return response;

#function to send confirmation SMS
def SendSMS(ser,value):
    #send SMS about the action
    ser.write('at\r');
    time.sleep(3);
    line=ser.read(size=64);
    print line;
    ser.write('AT+CMGS="+841243683496"\r');
    time.sleep(3);
    if (value==1):
        ser.write('Relay powered ON!\r');
    elif (value==0):
        ser.write('Relay powered OFF!\r');
    elif (value==2):
        ser.write('Started!\r');
    time.sleep(3);
    ser.write(chr(26));
    return;

#function to delete messages…(GSM900 stores only 30 messages..)
def DeleteAllMsg(ser):
    ser.write('at\r');
    time.sleep(3);
    line=ser.read(size=64);
    print line;
    ser.write('AT+CMGD=1,4\r');
    time.sleep(3);
    return;

#main program —————————————–
PowerON_SIM900_module();
print 'Registering the sim…\n';
time.sleep(15); #wait for sim to resgister to the net

#open serial link on /dev/ttyAMA0. It is open only one time:it remains open for all operation time.
#No more open+close action is now requested.
print 'Opening communications serial…\n';
ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1);
#ser.open();
#SendSMS(ser, 2);

#check continuous loop
#print “Starting main loop\n”;
arrived_messages=0;
while True:
    message=CheckNewUnreadMessage(ser);
    if(message.find("poweron")<>-1):
        #PowerONRelay();
        #send message to my phone that Relay is ON
        SendSMS(ser, 1);
        print 'PowerON commanded\n';
        arrived_messages=arrived_messages+1;
    elif (message.find("poweroff")<>-1):
        #PowerOFFRelay();
        #send message to my phone that Relay is OFF
        SendSMS(ser, 0);
        print 'PowerOFF commanded\n';
        arrived_messages=arrived_messages+1;
    if (arrived_messages>20):
        DeleteAllMsg(ser)
        time.sleep(5);
