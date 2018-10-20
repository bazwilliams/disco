#!/usr/bin/python

from threading import Thread
import paho.mqtt.client as mqtt
from phue import Bridge, PhueRegistrationException
from rgbxy import Converter
import time

disco_mode = False

try:
    b = Bridge('192.168.1.123')
    b.connect()

    light_names = b.get_light_objects('name')

    lights = [
        light_names['Lounge Lamp'],
        light_names['Lounge Main'] ]

    converter = Converter()

    colours = [
        converter.hex_to_xy('FF0000'),
        converter.hex_to_xy('00FF00'),
        converter.hex_to_xy('0000FF'),
        converter.hex_to_xy('FF00FF') ]
    print("Connected to hue bridge")

except PhueRegistrationException:
    print("No bridge registered, press button on bridge and try again")
    exit(1)


def on_connect(client, userdata, flags, rc):
    topic = "house/livingroom/disco";
    client.subscribe(topic)
    print("Subscribed to "+str(topic))

def on_message(client, userdata, msg):
    global disco_mode
    payload = msg.payload.decode('UTF-8')
    if not disco_mode and payload == "On":
        disco_mode = True
        thread = Disco_Thread()
        thread.start()
    else:
        disco_mode = False

class Disco_Thread(Thread):
    def run(self):
        global disco_mode
        global colours
        global lights
        originalState = dict()
        for light in lights:
            originalState[light] = {
                'on': light.on,
                'transitiontime': light.transitiontime,
                'xy': light.xy
            }

        while(disco_mode):
            for colour in colours:
                for light in lights:
                    light.on = True
                    light.transitiontime = 1
                    light.xy = colour
                    time.sleep(0.1)
        
        for light in lights:
            light.transitiontime = originalState[light]['transitiontime']
            light.xy = originalState[light]['xy']
            light.on = originalState[light]['on']

client = mqtt.Client()
client.connect("192.168.1.126", 1883, 60)
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
