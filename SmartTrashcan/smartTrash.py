#!/usr/bin/python
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time, threading, ssl
import random
import requests
import json

try:



    def sendMeasurements():
     try:
        GPIO.setmode(GPIO.BOARD)

        PIN_TRIGGER = 7
        PIN_ECHO = 11

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        print ("Waiting for sensor to settle")

        time.sleep(2)

        print ("Calculating distance")

        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time

        distance = round(pulse_duration * 17150, 2)
        fillPercent = round(100 - (distance * 2))

        print ("Distance:",distance,"cm")
        distanceVal = distance
        distanceStr = str(distanceVal)
        fillPercentStr = str(fillPercent)
        distanceFinal = "200,trashCan,distance,"+distanceStr+",cm"
        fillPercentFinal = "200,fillLevel,percent,"+fillPercentStr+",%"
        publish("s/us",distanceFinal)
        publish("s/us",fillPercentFinal)
        print ("Distance Message:", distanceFinal)
        print ("Fill Level Message:", fillPercentFinal)
        
        url = '{url}inventory/managedObjects/{deviceID}'

        token ="{base64 encoded password - username:password}"

        data = {
                "percent_calculation": {
                    "percent_calculation": fillPercent
                    }
                }

        headers = {'Authorization': 'Basic ' + token, "Content-Type": "application/json"}

        #Call REST APIraise
        response = requests.put(url, data=json.dumps(data), headers=headers)

        #Print Response
        print('Response:' + response.text)

        thread = threading.Timer(10, sendMeasurements)
    #thread.daemon=True
        thread.start()

    #while True: time.sleep(100)

     except (KeyboardInterrupt, SystemExit):
        sense.clear()
        print('Process manually terminated, quitting ...')


    def publish(topic, message, waitForAck = False):
      mid = client.publish(topic, message, 2)[1]
      if (waitForAck):
        while mid not in receivedMessages:
          time.sleep(0.25)

    def on_publish(client, userdata, mid):
      receivedMessages.append(mid)

    client = mqtt.Client(client_id="{{clientID}}")

    client.username_pw_set("{tenantID}/{username}", "{password}")
    client.on_publish = on_publish
    client.connect("mqtt.us.cumulocity.com", 1883)
    client.loop_start()
    client.subscribe("s/ds")
    sendMeasurements()


finally:
    GPIO.cleanup()
