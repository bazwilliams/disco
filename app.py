#!/usr/bin/python

from threading import Thread
import paho.mqtt.client as mqtt
from phue import Bridge, PhueRegistrationException
from rgbxy import Converter
import time

disco_mode = False
client = mqtt.Client()

try:
    b = Bridge('192.168.1.123')
    b.connect()

    light_names = b.get_light_objects('name')

    hue_lights = [
        light_names['Lounge Lamp'],
        light_names['Lounge Main'] ]

    converter = Converter()

    hue_colours = [
        converter.hex_to_xy('FF0000'),
        converter.hex_to_xy('00FF00'),
        converter.hex_to_xy('0000FF'),
        converter.hex_to_xy('FF00FF') ]

    mqtt_colours = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 1, 0],
    ]

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
        thread = Hue_Disco_Thread()
        thread.start()
    else:
        disco_mode = False

class MQTT_Disco_Thread(Thread):
    import paho.mqtt.subscribe as subscribe

    def run(self):
        global disco_mode
        global mqtt_colours
        global client

        orignalPayload = subscribe.simple("house/livingroom/christmastree", hostname="192.168.1.126").payload

        while(disco_mode):
            for colour in mqtt_colours:
                payload = "{ \"colours\": [ \"" + colour + "\" ],\"repeat\": true, \"animation\": \"chase\" }"
                client.publish("house/livingroom/christmastree", payload=payload, qos=0, retain=True)
                time.sleep(0.1)

        client.publish("house/livingroom/christmastree", payload=orignalPayload, qos=0, retain=True)

class Hue_Disco_Thread(Thread):
    def run(self):
        global disco_mode
        global hue_colours
        global hue_lights
        originalState = dict()
        for light in hue_lights:
            originalState[light] = {
                'on': light.on,
                'transitiontime': light.transitiontime,
                'xy': light.xy
            }

        while(disco_mode):
            for colour in hue_colours:
                for light in hue_lights:
                    light.on = True
                    light.transitiontime = 1
                    light.xy = colour
                    time.sleep(0.1)
        
        for light in hue_lights:
            light.transitiontime = originalState[light]['transitiontime']
            light.xy = originalState[light]['xy']
            light.on = originalState[light]['on']

client.connect("192.168.1.126", 1883, 60)
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
