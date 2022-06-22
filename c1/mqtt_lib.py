import json
import sys
import ssl
import time
import datetime
import logging, traceback
import paho.mqtt.client as mqtt
from threading import Thread
import queue
q = queue.Queue() #initialises a first in first out queue

class MqttHandler(Thread):
    mqttc = mqtt.Client()

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

        self.IoT_protocol_name = "x-amzn-mqtt-ca"
        self.aws_iot_endpoint = "apvkraojsc3zv-ats.iot.ap-south-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
        self.url = "https://{}".format(self.aws_iot_endpoint)

        self.ca = "./AWS/root-CA.crt" #Amazon's certificate from Third party                                     # Root_CA_Certificate_Name
        self.cert = "./AWS/TestSiteGateway.cert.pem"   # <Thing_Name>.cert.pem.crt. Thing's certificate from Amazon
        self.private = "./AWS/TestSiteGateway.private.key"        # <Thing_Name>.private.key Thing's private key from Amazon
        self.topic = "$aws/things/1/shadow/name/modeconfiguration/update"

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(log_format)
        self.logger.addHandler(handler)

     
        #mqttc = mqtt.Client()
        ssl_context= self.ssl_alpn()
        self.mqttc.tls_set_context(context=ssl_context)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message= self.on_message
        self.mqttc.on_publish = self.on_publish
        self.logger.info("start connect")
        #mqttc.connect(aws_iot_endpoint, port=443)
        self.logger.info("connect success")
        self.mqttc.connect(self.aws_iot_endpoint, port=443)    
        self.mqttc.publish(self.topic,"start")
        self.mqttc.subscribe("$aws/things/1/shadow/name/mode/update")
        self.mqttc.subscribe("$aws/things/1/shadow/name/modeconfiguration/update")
        # #mqttc.loop_forever()
        # mqttc.loop_start()  
   
    def run(self):
            while True:
                self.mqttc.loop()

    def _recv(self):
        if not q.empty():
            m=q.get()
            print('msg recv',m)
            return m

    def on_connect(self, client, userdata, flags, response_code):
        global connflag
        connflag = True
        print("Connected with status: {0}".format(response_code))

    def on_disconnect(self, client, userdata, rc):
            print("Client Disconnected")

    def on_publish(self, client, userdata, mid):
        print (str(userdata) + " -- " + str(mid))
        #client.disconnect()

    def on_message(self, client, userdata, message):
        print("message received " ,message.topic,"  >>  ",str(message.payload.decode("utf-8")))
        q.put((str(message.payload.decode("utf-8")) + "#" + str(message.topic) ))
    
    def _publish(self, topics, msg):
        self.mqttc.publish(topics,msg)    
    

    def ssl_alpn(self):
        try:
            #debug print opnessl version
            self.logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
            ssl_context = ssl.create_default_context()
            ssl_context.set_alpn_protocols([self.IoT_protocol_name])
            ssl_context.load_verify_locations(cafile=self.ca)
            ssl_context.load_cert_chain(certfile=self.cert, keyfile=self.private)

            return  ssl_context
        except Exception as e:
            print("exception ssl_alpn()")
            raise e

    

