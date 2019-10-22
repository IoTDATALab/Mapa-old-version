
FROM ubuntu:16.04


ADD ./sources.list  /etc/apt/sources.list 
ADD ./cloud-asgd.py cloud-asgd.py
ADD ./cloud-mapa.py cloud-mapa.py
ADD ./cloud-audp.py cloud-audp.py
ADD ./params.py params.py


RUN apt-get clean
RUN apt-get update
RUN apt-get install -y python3 python3-pip mosquitto
RUN pip3 install --default-timeout=100 paho-mqtt matplotlib==3.0 numpy==1.16.4  torch==1.1.0 torchvision==0.3.0 sympy==1.4 -i https://pypi.tuna.tsinghua.edu.cn/simple
