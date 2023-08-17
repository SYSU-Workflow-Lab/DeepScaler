#coding=utf-8
import urllib.parse
import requests
import os
import datetime
import time
import pandas as pd
import numpy as np
template = {
    "vCPU": "sum(rate(container_cpu_usage_seconds_total{{namespace='{0}',container='{1}'}}[{2}]))",
    "cpu":"sum(irate(container_cpu_usage_seconds_total{{container=~'{1}',namespace=~'{0}'}}[1m]))/sum(container_spec_cpu_quota{{container=~'{1}',namespace=~'{0}'}}/container_spec_cpu_period{{container=~'{1}',namespace=~'{0}'}})",
    "mem": "sum(container_memory_usage_bytes{{namespace='{0}',container='{1}'}}) / sum(container_spec_memory_limit_bytes{{namespace='{0}',container='{1}'}})",
    "mem_": "sum(container_memory_usage_bytes{{namespace='{0}',container='{1}'}})",
    "res": "sum(rate(istio_request_duration_milliseconds_sum{{reporter='destination',destination_workload_namespace='{0}',destination_workload='{1}'}}[{2}]))/sum(rate(istio_request_duration_milliseconds_count{{reporter='destination',destination_workload_namespace='{0}',destination_workload='{1}'}}[{2}]))/1000",
    "req": "sum(rate(istio_requests_total{{destination_workload_namespace='{0}',destination_workload='{1}'}}[{2}]))",
    "pod": "count(container_spec_cpu_period{{namespace='{0}',container='{1}'}})"
}
prefix_api = "http://localhost:30090/api/v1/query?query="
namespace = 'boutiquessj'
interval = 120
services = ["adservice", "cartservice", "checkoutservice","currencyservice","emailservice","frontend","paymentservice","productcatalogservice","recommendationservice","shippingservice"]


metrics = ['cpu','res','req','pod']
training_root_dir = ''

def fetch_cpu_usage(svc_name, namespace=namespace, interval=30):
    cpu_api = template["cpu"].format(namespace, svc_name, str(interval)+'s')
    url = prefix_api + urllib.parse.quote_plus(cpu_api)
    res = requests.get(url).json()["data"]
    v = 0
    if "result" in res and len(res["result"]) > 0 and "value" in res["result"][0]:
        v = res["result"][0]["value"][1]
    return float(v)


def fetch_mem_usage(svc_name, namespace=namespace):
    mem_api = template["mem"].format(namespace, svc_name)
    url = prefix_api + urllib.parse.quote_plus(mem_api)
    res = requests.get(url).json()["data"]
    v = 0
    if "result" in res and len(res["result"]) > 0 and "value" in res["result"][0]:
        v = res["result"][0]["value"][1]
    return float(v)


def fetch_res_time(svc_name, namespace=namespace, interval=30):
    res_api = template["res"].format(namespace, svc_name, str(interval)+'s')
    url = prefix_api + urllib.parse.quote_plus(res_api)
    res = requests.get(url).json()["data"]
    if "result" in res and len(res["result"]) > 0 and "value" in res["result"][0]:
        v = res["result"][0]["value"]
        if v[1] != 'NaN':
            return float(v[1])
    return 0


def fetch_req(svc_name, namespace=namespace, interval=30):
    req_api = template["req"].format(namespace, svc_name, str(interval)+'s')
    url = prefix_api + urllib.parse.quote_plus(req_api)
    req = requests.get(url).json()["data"]
    if "result" in req and len(req["result"]) > 0 and "value" in req["result"][0]:
        v = req["result"][0]["value"]
        if v[1] != 'NaN':
            return int(float(v[1]))
    return 0


def fetch_prior_req(svc_name, namespace=namespace, interval=30, delta=30):
    req_api = template["req"].format(namespace, svc_name, str(interval)+'s')
    url = prefix_api + urllib.parse.quote_plus(req_api) + "&time=" + str(time.time() - delta)
    req = requests.get(url).json()["data"]
    if "result" in req and len(req["result"]) > 0 and "value" in req["result"][0]:
        v = req["result"][0]["value"]
        if v[1] != 'NaN':
            return int(float(v[1]))
    return 0


def fetch_pods(svc_name, namespace=namespace):
    pod_api = template["pod"].format(namespace, svc_name)
    url = prefix_api + urllib.parse.quote_plus(pod_api)
    print(url)
    #pod = requests.get(url).json()
    pod = requests.get(url).json()["data"]
    if "result" in pod and len(pod["result"]) > 0 and "value" in pod["result"][0]:
        v = pod["result"][0]["value"]
        if v[1] != 'NaN':
            return int(float(v[1]))
    return 0


def save_fetch_data(svc_name, mode, start_time, latsted_time, interval, save_file):
    api_str = template[mode].format(namespace, svc_name, str(interval)+'s')#mode为pod，
    # start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    with open(save_file, 'w') as f:
        for i in range(0, latsted_time, int(interval)):#以interval为间隔
            t = start_time + datetime.timedelta(seconds=i)#加时间
            unixtime = time.mktime(t.timetuple())#返回用秒数来表示时间的浮点数。
            url = prefix_api + urllib.parse.quote_plus(api_str) + "&time=" + str(unixtime)
            res = requests.get(url).json()["data"]
            if "result" in res and len(res["result"]) > 0 and "value" in res["result"][0]:
                v = res["result"][0]["value"]
                if v[1] == 'NaN':
                    print("0", file=f)
                else:
                    print(str(v[1]), file=f)
            else:
                print("0", file=f)


def save_all_fetch_data(times=[], start_iter=1, root_dir='/home/boutiquessj/pythonForK6/data/', interval=interval, services=services, metrics=metrics):
    if not os.path.exists(root_dir):#若不存在则创建一个
        os.makedirs(root_dir)
    for i, (start_time, end_or_lasted) in enumerate(times):
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') #+ datetime.timedelta(hours=8)
        if type(end_or_lasted) == str:
            end_time = datetime.datetime.strptime(end_or_lasted, '%Y-%m-%d %H:%M:%S') #+ datetime.timedelta(hours=8)#######因为时区问题要加8
            lasted_time = int((end_time-start_time).total_seconds())#有多少秒
        else:
            lasted_time = int(end_or_lasted)
        if os.path.exists(root_dir+'{}_productpage_res.log'.format(start_iter+i)):
            print("Iternum needs update")
            return
        for svc in services:
            for m in metrics:
                save_fetch_data(svc, m, start_time, lasted_time, interval, root_dir+"{}_{}_{}.log".format(start_iter+i, svc, m))
                print("saved file:"+root_dir+"{}_{}_{}.log".format(start_iter+i, svc, m))

def load_fetch_data(root_dir, start_iter=1, end_iter=None, services=services, metrics=metrics) -> pd.DataFrame:
    if not end_iter:
        end_iter = start_iter
    data = {}
    for svc in services:
        data[svc] = {}
        for m in metrics:
            data[svc][m] = []
    for svc in services:
        for m in metrics:
            for iternum in range(start_iter, end_iter+1):
                path = root_dir + '{}_{}_{}.log'.format(iternum, svc, m)
                with open(path, 'r') as f:
                    lines = f.readlines()
                data[svc][m] += list(map(lambda x:float(x), lines))
    D = [data[svc][m] for svc in services for m in metrics]
    data_df = pd.DataFrame(np.array(D).T, columns=[svc+"_"+m for svc in services for m in metrics])
    return data_df


def load_processed_fetch_data(iternums=[1, 2], root_dir=training_root_dir, metrics=metrics):
    data_df = load_fetch_data(iternums, root_dir, metrics)
    D, l = [], len(metrics)
    for r in data_df.values:
        D.append([1]+list(r[:l]))
        D.append([2]+list(r[l:2*l]))
        D.append([3]+list(r[2*l:3*l]))
        D.append([4]+list(r[3*l:]))
    data_df = pd.DataFrame(D, columns=['svc']+metrics)
    data_df['pod'] = data_df['pod'].astype(int)
    return data_df

if __name__ == '__main__':
 
    times = [
        ('2023-03-04 04:09:01', '2023-03-04 05:25:15')

    ]#
    save_all_fetch_data(times, 1, root_dir='/ssj/ssj/boutiquessj/pyboutique/newData/slohpa/', interval=30, services=services)#interval 间隔
    print("ok")