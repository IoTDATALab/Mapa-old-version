#  面向边缘智能的异步差分隐私快速学习算法（MAPA）
## 1. 算法介绍

本算法为克服过时梯度对收敛影响，经典异步并行算法 SOA 收敛较集中式需要更多的迭代次数。我们提出的二阶段加速算法 TSA 和 TAPA 充分开采过时梯度对应的较大步长，使模型在第一阶段快速收敛到最优解周围的特定区域，在第二阶段限制学习率以减轻过时梯度影响确保模型收敛到最优解。算法 TSA 指二阶段加速算法（不含差分隐私保护），全称为 Two-stage accelerating algorithm。TAPA 指二阶段加速隐私算法，全称为 Two-stage accelerating private algorithm.

本项目是一个基于 docker 容器的异步联邦学习方法，三种算法 soa、ts、tapa，分别为传统异步联邦学习、加速联邦学习以及添加差分隐私机制的加速联邦学习。在该项目中，这三种方法分别在 docker-compose.yml 文件中以 soa、ts、tapa 区分，测试结果在各个边缘设备中的 result 文件夹中保存，文件名需要按照规范（devicename-containerid-functionname.txt）命名。

## 2.环境安装

|       OS       | Ubuntu 18.04 |
| :------------: | :----------: |
|     Docker     |   18.09.7    |
| Docker-compose |    1.24.1    |
|    OpenSSH     |     7.6      |

## 3. 项目结构

a) Cloud

```
云端（cloud）
├── cloud-soa.py   传统方法soa
├── cloud-mapa.py  添加噪声的两阶段tapa
├── cloud-ms.py    两阶段加速ts
├── Dockerfile    Docker镜像的构建文件
├── docker-compose.yml   定义服务、网络和卷的YAML文件
├── params.py
└── sources.list

```

b) Edge

```
边缘端（edge）
├── Dockerfile    Docker镜像的构建文件
├── docker-compose.yml   定义服务、网络和卷的YAML文件
├── sources.list
├── edge-soa.py
├── edge-mapa.py
├── edge-ms.py
├── data                               数据集
├   └──MNIST
├      └──  …
└──  result                              输出结果
     └── [EDGE_NUM:3][METHOD:soa]          准确率
 
```

## 4.网络配置
在应用运行前，先进行用户操作设备与工作节点的网络配置，将网络拓扑写入`ssh_config`文件，如：

```
Host cloud
    HostName xxx.xxx.xxx.xxx
    Port 22
    User node2user

Host edge1                                 #节点名称
    HostName xxx.xxx.xxx.xxx                   #ip
    Port 22                                    #port
    User node1user                             #ssh连接的User

```

## 5.参数设置
超参在Makefile文件中定义

```
# In cloud 
CLOUD := cloud
MQTT_IP ?= 192.168.0.101
MQTT_PORT ?= 1884

# In edge
EDGES := edge1
EDGES_NUM ?=1
CONTAINER_NUM ?=3
METHOD ?= soa  #soa, ts, tapa
BATCH_SIZE ?= 24
EPOCH ?= 1
TEST_NUM ?= 100
DATA_ROOT ?= './data/'
RESULT_ROOT ?= './result/'

```

| **cloud**  |                                  |
| :--------- | :------------------------------: |
| CLIENT_NUM |          边缘节点的个数          |
| MQTT_IP    |  Afl_cloud 中 MQTT broker 的 ip  |
| MQTT_PORT  | Afl_cloud 中 MQTT broker 的 port |

| **edge**    |                                   |
| :---------- | :-------------------------------: |
| DATA_ROOT   |         训练、测试数据集          |
| RESULT_ROOT | 结果存储文件目录，格式为'./xxxx/' |
| METHOD      |      方法名（soa、ts、tapa）      |
| EPOCH       |           边缘迭代次数            |
| BATCH_SIZE  |  每个 minibatch 里训练样本的个数  |
| TEST_NUM    |  每训练 TEST_NUM 次进行一次测试   |
| DATA_ROOT   |         训练、测试数据集          |
| RESULT_ROOT | 结果存储文件目录，格式为'./xxxx/' |
| DATA_ROOT   |         训练、测试数据集          |
| RESULT_ROOT | 结果存储文件目录，格式为'./xxxx/' |

## 6.运行
##
在使用流程中，在项目文件夹下，执行 shell 指令进行项目应用：

```
make net_config
# 进行用户操作设备和工作节点间的网络配置，包括ssh免密操作的配置。完成这一步之后，用户操作设备可以直接通过ssh在其他工作节点上执行算法相关步骤。

make build
# 将程序与算法数据包从用户操作设备传输到相应工作节点，并进行镜像构建。

make run
# 启动容器，将参数传输到各个工作节点上，为工作节点分配任务，开始执行算法工作。

make logs
# 看主节点上的工作日志，日志内容跟随当前程序执行情况即时动态刷新。

make result
#将实验结果输出到宿主机。

make clean
# 清理全部容器，释放占用资源。
```
