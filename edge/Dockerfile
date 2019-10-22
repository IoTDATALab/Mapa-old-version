
FROM ubuntu:16.04


ADD ./sources.list  /etc/apt/sources.list 
ADD ./edge-asgd.py edge-asgd.py
ADD ./edge-mapa.py edge-mapa.py
ADD ./edge-audp.py edge-audp.py


RUN apt-get clean
RUN apt-get update
RUN apt-get install -y python3 python3-pip mosquitto
RUN pip3 install --default-timeout=100 paho-mqtt matplotlib==3.0 numpy==1.16.4  torch==1.1.0 torchvision==0.3.0 sympy==1.4 -i https://pypi.tuna.tsinghua.edu.cn/simple
