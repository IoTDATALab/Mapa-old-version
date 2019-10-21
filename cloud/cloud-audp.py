import os
from params import *
import _pickle as cPickle
import paho.mqtt.client as mqtt
import  queue
from sympy import *
from math import sqrt
import math
import numpy as np
import torch

DELAY = int(os.getenv('DELAY'))
EPOCH = int(os.environ.get('EPOCH')) 
BATCH_SIZE = int(os.environ.get('BATCH_SIZE')) 
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
MQTT_IP = os.environ.get('MQTT_IP')
DOWNLOAD_MNIST = False

R = 50
L = 10
lambda1=0.0001
m = 60000
SIGMA = 30
VAREPSILON = 1
T=math.floor(m/BATCH_SIZE)*EPOCH

delta = 0.001
msgQueue = queue.Queue()
    
def noise_fun(b,p):
    noise = -b*np.sign(p-0.5)*math.log(1-2*abs(p-0.5))
    return noise


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
client.subscribe([("audp_grads/#", 2)])
client.loop_start()

if __name__=='__main__':
    x = Symbol('x')
    dS1 = 8/BATCH_SIZE
    b1=dS1/VAREPSILON
    Delta_b=SIGMA**2/BATCH_SIZE+2*dS1**2/VAREPSILON**2
    params = InitializeParameters()
    client.publish("audp_init_params", cPickle.dumps(params), 2)
    for epoch in range(EPOCH):
        print(type(m/BATCH_SIZE))
        for step in range(int(m/BATCH_SIZE)+1):
            LR=1/(2*L*(DELAY+1)+sqrt(Delta_b*(epoch*(m/BATCH_SIZE)+step)))
            print("step:",step,"LR:",LR)
            msglist = msgQueue.get()
            edgetopic = msglist[0]
            edgemsg = msglist[1]
            edgetopic = "audp_params/"+edgetopic.split('/')[1]
            grads = cPickle.loads(edgemsg)
            shape = np.shape(params[0].numpy())
            noise = np.random.rand(shape[0],shape[1],shape[2],shape[3])-0.5
            noise = noise/np.linalg.norm(noise)*noise_fun(b1,np.random.rand())
            noise = torch.from_numpy(noise).float()
            
            for i in range(len(params)):
                params[i] = params[i].float()
                if i%2 == 0:
                    if i==0:
                        params[i] -= LR*(grads[i]+lambda1*params[i]+noise)
                    params[i] -= LR*(grads[i]+lambda1*params[i])
                else : 
                    params[i] -=LR*grads[i]   
            client.publish(edgetopic, cPickle.dumps(params), 2)
            if epoch*(m/BATCH_SIZE)+step==T:
                break
   