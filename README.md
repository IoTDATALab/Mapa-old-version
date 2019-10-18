# 3.2 面向边缘智能的异步差分隐私快速学习算法（TAPA）
## 1. 算法介绍

本算法为克服过时梯度对收敛影响，经典异步并行算法 SOA 收敛较集中式需要更多的迭代次数。我们提出的二阶段加速算法 TSA 和 TAPA 充分开采过时梯度对应的较大步长，使模型在第一阶段快速收敛到最优解周围的特定区域，在第二阶段限制学习率以减轻过时梯度影响确保模型收敛到最优解。算法 TSA 指二阶段加速算法（不含差分隐私保护），全称为 Two-stage accelerating algorithm。TAPA 指二阶段加速隐私算法，全称为 Two-stage accelerating private algorithm.

本项目是一个基于 docker 容器的异步联邦学习方法，三种算法 soa、ts、tapa，分别为传统异步联邦学习、加速联邦学习以及添加差分隐私机制的加速联邦学习。在该项目中，这三种方法分别在 docker-compose.yml 文件中以 soa、ts、tapa 区分，测试结果在各个边缘设备中的 result 文件夹中保存，文件名需要按照规范（devicename-containerid-functionname.txt）命名。

## 2. 项目结构

（1）项目文件树

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
├── Dockerfile.tx2    Docker镜像的构建文件
├── docker-compose.yml   定义服务、网络和卷的YAML文件
├── docker-compose.tx2.yml   定义服务、网络和卷的YAML文件
├── sources.list
├── sources.tx2.list
├── edge-soa.py
├── edge-mapa.py
├── edge-ms.py
├── data                               数据集
├   └──MNIST
├      └──  …
└──  result                              输出结果
     └── [EDGE_NUM:3][METHOD:soa]          准确率
 
```

（2）文件用途说明

云端 `cloud-soa/tapa/ts.py`、`params.py` 文件是程序运行 python 文件。

边缘端 `data` 文件夹是挂载的数据集存放文件夹，`edge-ts/soa/tapa.py` 文件是程序运行的相关 python 文件，`result`文件夹是挂载的结果存放文件夹。

`docker-compose.yml`文件指定了使用的容器并定义了环境变量等配置。`Dockerfile` 文件定义了运行环境（包括软件包依赖、语言运行环境、语言软件包依赖等）。

## 3.环境安装
### Docker环境安装

`sudo apt-get install docker-ce`
### Docker-Compose安装
`sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose`

## 4.项目运行
(1) 网络配置

ssh_config 文件中填入相应云端IP、PORT等信息


(3） 超参定义

| **cloud**  |                                  |
| :--------- | :------------------------------: |
| MASTER     |         master 节点名称          |
| CLIENT_NUM |          边缘节点的个数          |
| MQTT_IP    |  Afl_cloud 中 MQTT broker 的 ip  |
| MQTT_PORT  | Afl_cloud 中 MQTT broker 的 port |

| **edge**    |                                   |
| :---------- | :-------------------------------: |
| METHOD      |      方法名（soa、ts、tapa）      |
| CLIENT_ID   |           边缘节点名称            |
| EPOCH       |           边缘迭代次数            |
| MQTT_IP     |  Afl_cloud 中 MQTT broker 的 ip   |
| MQTT_PORT   | Afl_cloud 中 MQTT broker 的 port  |
| BATCH_SIZE  |  每个 minibatch 里训练样本的个数  |
| TEST_NUM    |  每训练 TEST_NUM 次进行一次测试   |
| DATA_ROOT   |         训练、测试数据集          |
| RESULT_ROOT | 结果存储文件目录，格式为'./xxxx/' |

（4）指令执行过程

a) cloud 和 edge 进行网络配置：`make net_config`

b) 构建镜像：`make build`

c) 启动容器：`make run`

d) 查看主节点工作日志：`make logs`

e) 传输实验结果：`make result`

f) 清理容器：`make clean`


