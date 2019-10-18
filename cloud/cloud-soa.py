import os
from params import *
import _pickle as cPickle
from math import sqrt
import paho.mqtt.client as mqtt
import  queue

DELAY = int(os.getenv('DELAY'))
EPOCH = int(os.environ.get('EPOCH')) 
BATCH_SIZE = int(os.environ.get('BATCH_SIZE')) 
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
MQTT_IP = os.environ.get('MQTT_IP')

print(MQTT_PORT,MQTT_IP)
DOWNLOAD_MNIST = False
SIGMA = 5
R = 50
L = 10
lambda1=0.0001
m = 60000
msgQueue = queue.Queue()

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
def on_message(mqttc, obj, msg):
    print("received: " + msg.topic + " " + str(msg.qos))
    msglist = []
    msglist.append(msg.topic)
    msglist.append(msg.payload)
    msgQueue.put(msglist)

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_IP,MQTT_PORT, 600)
client.subscribe([("soa_grads/#", 2)])
client.loop_start()

if __name__=='__main__':
    params = InitializeParameters()
    client.publish("soa_init_params", cPickle.dumps(params), 2)
    for epoch in range(EPOCH):
        print(type(m/BATCH_SIZE))
        for step in range(int(m/BATCH_SIZE)+1):
            LR=L*(DELAY+1)**2+SIGMA*sqrt(step+1)/(R*sqrt(BATCH_SIZE));
            LR=1/LR
            print("step:",step,"LR:",LR)
            msglist = msgQueue.get()
            edgetopic = msglist[0]
            edgemsg = msglist[1]
            edgetopic = "soa_params/"+edgetopic.split('/')[1]
            grads = cPickle.loads(edgemsg)

            for i in range(len(params)):
                params[i] = params[i].float()
                if i%2 == 0:
                    params[i] -= LR*(grads[i]+lambda1*params[i])
                else : 
                    params[i] -=LR*grads[i]   
            client.publish(edgetopic, cPickle.dumps(params), 2)