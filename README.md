# DeepScaler: Holistic Autoscaling for Microservices Based on Spatiotemporal GNN with Adaptive Graph Learning

![Static Badge](https://img.shields.io/badge/python-3.6-blue) ![Static Badge](https://img.shields.io/badge/PyTorch-red) 
- [Overview](#overview)
- [I. Machine Prerequis](#i-machine-prerequis)
- [II. Installation](#ii-installation)
  * [1. Setup Required Packages](#1-setup-required-packages)
  * [2. Setup Docker](#2-setup-docker)
  * [3. Setup Kubernetes Cluster](#3-setup-kubernetes-cluster)
  * [4. Setup Prometheus](#4-setup-prometheus)
  * [5. Setup Istio](#5-setup-istio)
  * [6. Setup Locust](#6-setup-locust)
  * [7. Setup Jaeger](#7-setup-jaeger)
- [III. Deploy Benchmark Microservices](#iii-deploye-benchmark-microservices)
  * [1. Bookinfo](#1-bookinfo)
  * [2. Online-boutique](#2-online-boutique)
  * [3. Train-ticket](#3-train-ticket)
- [IV. Workload Generation](#iv-workload-generation)
- [V. Train and Test](#v-train-and-test)
  * [1. Model Configuration](#1-model-configuration)
  * [2. Collect the original dataset](#2-collect-the-original-dataset)
  * [3. Process the dataset](#3-process-the-dataset)
  * [4. Export the well-trained model](#4-export-the-well-trained-model)
- [VI. Autoscaling](#vi-autoscaling)
- [VII. Evaluation](#vii-evaluation)
  * [1. Analyze the similarity between the original graph relationship and od, cc.](#1-analyze-the-similarity-between-the-original-graph-relationship-and-od--cc)
  * [2. Compute relevant metrics.](#2-compute-relevant-metrics)
- [VIII. Citation](#viii-citation)
- [IX. Contact](#ix-contact)


## Overview
This repository contains a prototyped version of DeepScaler described in our ASE '23 paper "DeepScaler: Holistic Autoscaling for Microservices Based on Spatiotemporal GNN with Adaptive Graph Learning".

## I. Machine Prerequisite

| **Aspect**                  | **Details**                                                                                                         |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------|
| Operating System	           | Ubuntu 18.04 LTS                                                                                                    |
| Kernel Version	             | 4.15.0                                                                                                              |
| VM Specifications	          | 4 with 12-core 2.2 GHz CPU, 24 GB memory, 100GB disk<br>4 with 24-core 2.2 GHz CPU, 32 GB memory, 500 GB disk |
| Network | ... |

## II. Installation
### 1. Setup Required Packages
+   Python 3.6
+   numpy == 1.21.5
+   pandas == 1.4.4
+   torch == 1.13.1

 ```pip3 install -r requirements.txt```
### 2. Setup Docker
Docker 20.10.12

### 3. Setup Kubernetes Cluster
A running Kubernetes cluster is required before deploying DeepScaler. The following instructions are tested with Kubernetes v1.23.4. For set-up instructions, refer to [this](setUp-k8s.md).


### 4. Setup Prometheus
Prometheus is an open-source monitoring and alerting toolkit used for collecting and storing metrics from various systems.
For detailed installation steps, please refer to [this](https://prometheus.io/docs/introduction/first_steps/).

### 5. Setup Istio
Istio is an open-source service mesh platform that enhances the management and security of microservices in a distributed application. After having a cluster running a supported version of Kubernetes, installing Istio is needed. Follow [these steps](https://istio.io/latest/docs/setup/getting-started/) to get started with Istio.

### 6. Setup Locust
We utilize the [Locust](https://locust.io/) load testing tool, an open-source tool that employs Python code to define user behaviors and simulate millions of users.

### 7. Setup Jaeger
We use Jaeger to initiate scenario A, which involves establishing an invocation relationship among microservices through automated processes.
 Follow [these steps](https://www.jaegertracing.io/docs/1.14/getting-started/) to get started with Jaeger.
 
## III. Deploy Benchmark Microservices
### 1. Bookinfo
```
(1) kubectl create -f <(istioctl kube-inject -f /benchmarks/bookinfo/bookinfo.yaml)
(2) kubectl apply  -f /benchmarks/bookinfo/bookinfo-gateway.yaml)
```
### 2. Online-boutique
```
(1) kubectl create -f <(istioctl kube-inject -f /benchmarks/boutique/boutique.yaml)
(2) kubectl apply  -f /benchmarks/boutique/boutique-gateway.yaml)
```
### 3. Train-ticket
Deploy the Train-Ticket system on K8S with istio.
```
(1) kubectl create -f <(istioctl kube-inject -f /benchmarks/train-ticket/ts-deployment-part1.yml)
(2) kubectl create -f <(istioctl kube-inject -f /benchmarks/train-ticket/ts-deployment-part2.yml)
(3) kubectl create -f <(istioctl kube-inject -f /benchmarks/train-ticket/ts-deployment-part3.yml)
(4) kubectl apply  -f /benchmarks/train-ticket/trainticket-gateway.yaml
```

## IV. Workload Generation

The generated workload intensity varied over time, emulating typical characteristics of microservice workloads, including slight increases, slight decreases, sharp increases, sharp decreases, and continuous fluctuations. The flow data simulation script is collected from FIFA World Cup access datasets and stored in the [file](https://github.com/SYSU-Workflow-Administrator/DeepScaler/blob/main/sendFlow/random-100max.req).

The script [load_generator.py](https://github.com/SYSU-Workflow-Administrator/DeepScaler/blob/main/sendFlow/load_generator.py) is for simulating user behavior for both "Bookinfo" and "Online-Boutique" and [load_generator_train.py](https://github.com/SYSU-Workflow-Administrator/DeepScaler/blob/main/sendFlow/load_generator_train.py) is for simulating user behavior for "Train-Ticket."

Simulate the workload generator:
``` 
sh sendFlow/sendLoop.sh
```

You can refer to this [webpage](https://blog.techbridge.cc/2019/05/29/how-to-use-python-locust-to-do-load-testing/) for customized usage.

## V. Train and Test
### 1. Model Configuration
The information that needs to be configured before model training is stored in [config/train_config.yaml](https://github.com/SYSU-Workflow-Administrator/DeepScaler/blob/main/config/train_config.yaml), and the processed data sets and various model configuration information are stored in [config/train_datasets_speed.yaml](https://github.com/SYSU-Workflow-Administrator/DeepScaler/blob/main/config/train_datasets_speed.yaml). You can modify the tuning parameters yourself.

### 2. Collect the original dataset
```
template = {
    "cpu":"sum(irate(container_cpu_usage_seconds_total{{container=~'{1}',namespace=~'{0}'}}[1m]))/sum(container_spec_cpu_quota{{container=~'{1}',namespace=~'{0}'}}/container_spec_cpu_period{{container=~'{1}',namespace=~'{0}'}})",
    "mem": "sum(container_memory_usage_bytes{{namespace='{0}',container='{1}'}}) / sum(container_spec_memory_limit_bytes{{namespace='{0}',container='{1}'}})",
    "res": "sum(rate(istio_request_duration_milliseconds_sum{{reporter='destination',destination_workload_namespace='{0}',destination_workload='{1}'}}[{2}]))/sum(rate(istio_request_duration_milliseconds_count{{reporter='destination',destination_workload_namespace='{0}',destination_workload='{1}'}}[{2}]))/1000",
    "req": "sum(rate(istio_requests_total{{destination_workload_namespace='{0}',destination_workload='{1}'}}[{2}]))",
    "pod": "count(container_spec_cpu_period{{namespace='{0}',container='{1}'}})"
}
```
Run this code, and the data will be stored in the folder location you have set.
```
python metrics_fetch.py
```
```
#Here's "Online-Boutique" example:
prefix_api = "http://localhost:30090/api/v1/query?query="
namespace = 'boutiquessj'
interval = 120
services = ["adservice", "cartservice", "checkoutservice","currencyservice","emailservice","frontend","paymentservice","productcatalogservice","recommendationservice","shippingservice"]
metrics = ['cpu','res','req','mem','pod']
```
### 3. Process the dataset
Transform the raw dataset into a time-sliced dataset for model training and learning. 
```
python data_process.py
```
### 4. Export the well-trained model

We provide a more detailed and complete command description for training and testing the model:

```
python -u main.py
--model_config_path <model_config_path>
--train_config_path <train_config_path>
--model_name <model_name>
--num_epoch <num_epoch>
--num_iter <num_iter>
--model_save_path <model_save_path>
--max_graph_num <max_graph_num>
```

| Parameter name    | Description of parameter       |
|-------------------|--------------------------------|
| model_config_path | Config path of models          |
| train_config_path | Config path of Trainer         |
| model_name        | Model name to train            |
| num_epoch         | Training times per epoch       |
| num_iter          | Maximum value for iteration    |
| model_save_path   | Model save path                |
| max_graph_num     | Volume of adjacency matrix set |

More parameter information please refer to main.py.
The models exported after running the file are stored in the [model_states](https://github.com/SYSU-Workflow-Administrator/DeepScaler/tree/main/model_states).

## VI. Autoscaling

Utilizing well-trained and tested models to enable automatic scaling of various microservices.

```
python predict_scale.py
```

## VII. Evaluation

### 1. Analyze the similarity between the original graph relationship and od, cc.

```
python similarity.py
 ```

### 2. Compute relevant metrics.

```
python calculate.py
```
## VIII. Citation
If you find this repository useful in your research, please consider citing the following papers:

```
@INPROCEEDINGS{1234567,
  author={Meng, Chunyang and Song, Shijie and Tong, Haogang and Pan, Maolin and Yu, Yang},
  booktitle={2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)}, 
  title={DeepScaler: Holistic Autoscaling for Microservices Based on Spatiotemporal GNN with Adaptive Graph Learnin}, 
  year={2023}
}
```

## IX. Contact
If you have any questions, feel free to contact Shijie Song or Chunyang Meng through Email (<songshj6@mail2.sysu.edu.cn>, <mengchy3@mail2.sysu.edu.cn>) or Github issues. Pull requests are highly welcomed!





