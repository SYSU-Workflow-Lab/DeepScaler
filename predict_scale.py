import torch
import numpy as np
from models import AdapGL
import os
import sys
import yaml
import torch
import argparse
import trainer
from utils import scaler
from models import AdapGL
from dataset import TPDataset
from dataset import TPDataset2
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt
import torch
import numpy as np
import datetime
from metrics_fetch import save_all_fetch_data
from prepareData import predict_read_and_generate_dataset
from k8sop import K8sOp
import urllib.parse
import random
import json
import time
import xlwt
import requests
import pandas as pd
import math
import operator
import subprocess
import math


def load_config(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def main(args):
    k8s_op = K8sOp()
    svc_ls = ["adservice", "cartservice", "checkoutservice","currencyservice", "emailservice","frontend","paymentservice","productcatalogservice","recommendationservice","shippingservice"]
    
    c_temp=0#loop time
    while True:
        start = time.time()
        services = ["adservice", "cartservice", "checkoutservice","currencyservice", "emailservice","frontend","paymentservice","productcatalogservice","recommendationservice","shippingservice"]
        metrics = ['pod','cpu','res','req','mem']

        current_time = datetime.datetime.now()
        current_time_str=current_time.strftime('%Y-%m-%d %H:%M:%S')
        if(c_temp==0):
            start_time_str = (current_time-datetime.timedelta(hours=1)-datetime.timedelta(minutes=21)).strftime('%Y-%m-%d %H:%M:%S')#
        else:
            start_time_str = (current_time-datetime.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
        times_original = [
            (str(start_time_str), str(current_time_str))
        ]
        print(times_original)

        save_all_fetch_data(times_original, 1, root_dir='/dataForPredict/', interval=60, services=services)#interval 间隔
        ### pod
        # "adservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[0],metrics[0])
        adservice_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            adservice_pod=np.array([adservice_pod])
        adservice_pod = adservice_pod[:,np.newaxis]
        # "cartservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[1],metrics[0])
        cartservice_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            cartservice_pod=np.array([cartservice_pod])
        cartservice_pod = cartservice_pod[:,np.newaxis]
        # "checkoutservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[2],metrics[0])
        checkoutservice_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            checkoutservice_pod=np.array([checkoutservice_pod])
        checkoutservice_pod = checkoutservice_pod[:,np.newaxis]
        # "currencyservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[3],metrics[0])
        currencyservice_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            currencyservice_pod=np.array([currencyservice_pod])
        currencyservice_pod = currencyservice_pod[:,np.newaxis]
        # "emailservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[4],metrics[0])
        emailservice_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            emailservice_pod=np.array([emailservice_pod])
        emailservice_pod = emailservice_pod[:,np.newaxis]
        # "frontend"
        file = '/dataForPredict/1_{}_{}.log'.format(services[5],metrics[0])
        frontend_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            frontend_pod=np.array([frontend_pod])
        frontend_pod = frontend_pod[:,np.newaxis]
        # "paymentservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[6],metrics[0])
        paymentservice_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            paymentservice_pod=np.array([paymentservice_pod])
        paymentservice_pod = paymentservice_pod[:,np.newaxis]
        # "productcatalogservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[7],metrics[0])
        productcatalogservice_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            productcatalogservice_pod=np.array([productcatalogservice_pod])
        productcatalogservice_pod = productcatalogservice_pod[:,np.newaxis]
        # "recommendationservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[8],metrics[0])
        recommendationservice_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            recommendationservice_pod=np.array([recommendationservice_pod])
        recommendationservice_pod = recommendationservice_pod[:,np.newaxis]
        # "shippingservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[9],metrics[0])
        shippingservice_pod=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            shippingservice_pod=np.array([shippingservice_pod])
        shippingservice_pod = shippingservice_pod[:,np.newaxis]

        ####cpu
        file = '/dataForPredict/1_{}_{}.log'.format(services[0],metrics[1])
        adservice_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            adservice_cpu=np.array([adservice_cpu])
        adservice_cpu = adservice_cpu[:,np.newaxis]
        # "cartservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[1],metrics[1])
        cartservice_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            cartservice_cpu=np.array([cartservice_cpu])
        cartservice_cpu = cartservice_cpu[:,np.newaxis]
        # "checkoutservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[2],metrics[1])
        checkoutservice_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            checkoutservice_cpu=np.array([checkoutservice_cpu])
        checkoutservice_cpu = checkoutservice_cpu[:,np.newaxis]
        # "currencyservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[3],metrics[1])
        currencyservice_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            currencyservice_cpu=np.array([currencyservice_cpu])
        currencyservice_cpu = currencyservice_cpu[:,np.newaxis]
        # "emailservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[4],metrics[1])
        emailservice_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            emailservice_cpu=np.array([emailservice_cpu])
        emailservice_cpu = emailservice_cpu[:,np.newaxis]
        # "frontend"
        file = '/dataForPredict/1_{}_{}.log'.format(services[5],metrics[1])
        frontend_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            frontend_cpu=np.array([frontend_cpu])
        frontend_cpu = frontend_cpu[:,np.newaxis]
        # "paymentservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[6],metrics[1])
        paymentservice_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            paymentservice_cpu=np.array([paymentservice_cpu])
        paymentservice_cpu = paymentservice_cpu[:,np.newaxis]
        # "productcatalogservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[7],metrics[1])
        productcatalogservice_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            productcatalogservice_cpu=np.array([productcatalogservice_cpu])
        productcatalogservice_cpu = productcatalogservice_cpu[:,np.newaxis]
        # "recommendationservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[8],metrics[1])
        recommendationservice_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            recommendationservice_cpu=np.array([recommendationservice_cpu])
        recommendationservice_cpu = recommendationservice_cpu[:,np.newaxis]
        # "shippingservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[9],metrics[1])
        shippingservice_cpu=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            shippingservice_cpu=np.array([shippingservice_cpu])
        shippingservice_cpu = shippingservice_cpu[:,np.newaxis]

        ### res
        # "adservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[0],metrics[2])
        adservice_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            adservice_res=np.array([adservice_res])
        adservice_res = adservice_res[:,np.newaxis]
        # "cartservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[1],metrics[2])
        cartservice_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            cartservice_res=np.array([cartservice_res])
        cartservice_res = cartservice_res[:,np.newaxis]
        # "checkoutservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[2],metrics[2])
        checkoutservice_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            checkoutservice_res=np.array([checkoutservice_res])
        checkoutservice_res = checkoutservice_res[:,np.newaxis]
        # "currencyservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[3],metrics[2])
        currencyservice_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            currencyservice_res=np.array([currencyservice_res])
        currencyservice_res = currencyservice_res[:,np.newaxis]
        # "emailservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[4],metrics[2])
        emailservice_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            emailservice_res=np.array([emailservice_res])
        emailservice_res = emailservice_res[:,np.newaxis]
        # "frontend"
        file = '/dataForPredict/1_{}_{}.log'.format(services[5],metrics[2])
        frontend_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            frontend_res=np.array([frontend_res])
        frontend_res = frontend_res[:,np.newaxis]
        # "paymentservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[6],metrics[2])
        paymentservice_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            paymentservice_res=np.array([paymentservice_res])
        paymentservice_res = paymentservice_res[:,np.newaxis]
        # "productcatalogservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[7],metrics[2])
        productcatalogservice_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            productcatalogservice_res=np.array([productcatalogservice_res])
        productcatalogservice_res = productcatalogservice_res[:,np.newaxis]
        # "recommendationservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[8],metrics[2])
        recommendationservice_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            recommendationservice_res=np.array([recommendationservice_res])
        recommendationservice_res = recommendationservice_res[:,np.newaxis]
        # "shippingservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[9],metrics[2])
        shippingservice_res=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            shippingservice_res=np.array([shippingservice_res])
        shippingservice_res = shippingservice_res[:,np.newaxis]

        ###req
        # "adservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[0],metrics[3])
        adservice_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            adservice_req=np.array([adservice_req])
        adservice_req = adservice_req[:,np.newaxis]
        # "cartservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[1],metrics[3])
        cartservice_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            cartservice_req=np.array([cartservice_req])
        cartservice_req = cartservice_req[:,np.newaxis]
        # "checkoutservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[2],metrics[3])
        checkoutservice_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            checkoutservice_req=np.array([checkoutservice_req])
        checkoutservice_req = checkoutservice_req[:,np.newaxis]
        # "currencyservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[3],metrics[3])
        currencyservice_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            currencyservice_req=np.array([currencyservice_req])
        currencyservice_req = currencyservice_req[:,np.newaxis]
        # "emailservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[4],metrics[3])
        emailservice_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            emailservice_req=np.array([emailservice_req])
        emailservice_req = emailservice_req[:,np.newaxis]
        # "frontend"
        file = '/dataForPredict/1_{}_{}.log'.format(services[5],metrics[3])
        frontend_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            frontend_req=np.array([frontend_req])
        frontend_req = frontend_req[:,np.newaxis]
        # "paymentservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[6],metrics[3])
        paymentservice_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            paymentservice_req=np.array([paymentservice_req])
        paymentservice_req = paymentservice_req[:,np.newaxis]
        # "productcatalogservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[7],metrics[3])
        productcatalogservice_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            productcatalogservice_req=np.array([productcatalogservice_req])
        productcatalogservice_req = productcatalogservice_req[:,np.newaxis]
        # "recommendationservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[8],metrics[3])
        recommendationservice_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            recommendationservice_req=np.array([recommendationservice_req])
        recommendationservice_req = recommendationservice_req[:,np.newaxis]
        # "shippingservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[9],metrics[3])
        shippingservice_req=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            shippingservice_req=np.array([shippingservice_req])
        shippingservice_req = shippingservice_req[:,np.newaxis]

        ###mem
        # "adservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[0],metrics[3])
        adservice_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            adservice_mem=np.array([adservice_mem])
        adservice_mem = adservice_mem[:,np.newaxis]
        # "cartservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[1],metrics[3])
        cartservice_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            cartservice_mem=np.array([cartservice_mem])
        cartservice_mem = cartservice_mem[:,np.newaxis]
        # "checkoutservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[2],metrics[3])
        checkoutservice_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            checkoutservice_mem=np.array([checkoutservice_mem])
        checkoutservice_mem = checkoutservice_mem[:,np.newaxis]
        # "currencyservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[3],metrics[3])
        currencyservice_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            currencyservice_mem=np.array([currencyservice_mem])
        currencyservice_mem = currencyservice_mem[:,np.newaxis]
        # "emailservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[4],metrics[3])
        emailservice_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            emailservice_mem=np.array([emailservice_mem])
        emailservice_mem = emailservice_mem[:,np.newaxis]
        # "frontend"
        file = '/dataForPredict/1_{}_{}.log'.format(services[5],metrics[3])
        frontend_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            frontend_mem=np.array([frontend_mem])
        frontend_mem = frontend_mem[:,np.newaxis]
        # "paymentservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[6],metrics[3])
        paymentservice_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            paymentservice_mem=np.array([paymentservice_mem])
        paymentservice_mem = paymentservice_mem[:,np.newaxis]
        # "productcatalogservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[7],metrics[3])
        productcatalogservice_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            productcatalogservice_mem=np.array([productcatalogservice_mem])
        productcatalogservice_mem = productcatalogservice_mem[:,np.newaxis]
        # "recommendationservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[8],metrics[3])
        recommendationservice_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            recommendationservice_mem=np.array([recommendationservice_mem])
        recommendationservice_mem = recommendationservice_mem[:,np.newaxis]
        # "shippingservice"
        file = '/dataForPredict/1_{}_{}.log'.format(services[9],metrics[3])
        shippingservice_mem=np.genfromtxt(file, dtype=np.double)
        if(c_temp!=0):
            shippingservice_mem=np.array([shippingservice_mem])
        shippingservice_mem = shippingservice_mem[:,np.newaxis]


        timeLen = len(adservice_cpu)
        if c_temp==0:
            xx=torch.tensor([])
        else:
            xx=xx[1:,:,:]
        for i in range(timeLen):
            listpod = np.vstack((adservice_pod[i],cartservice_pod[i],checkoutservice_pod[i],currencyservice_pod[i],emailservice_pod[i],frontend_pod[i],paymentservice_pod[i],productcatalogservice_pod[i],recommendationservice_pod[i],shippingservice_pod[i]))
            listcpu = np.vstack((adservice_cpu[i],cartservice_cpu[i],checkoutservice_cpu[i],currencyservice_cpu[i],emailservice_cpu[i],frontend_cpu[i],paymentservice_cpu[i],productcatalogservice_cpu[i],recommendationservice_cpu[i],shippingservice_cpu[i]))
            listres = np.vstack((adservice_res[i],cartservice_res[i],checkoutservice_res[i],currencyservice_res[i],emailservice_res[i],frontend_res[i],paymentservice_res[i],productcatalogservice_res[i],recommendationservice_res[i],shippingservice_res[i]))
            listreq = np.vstack((adservice_req[i],cartservice_req[i],checkoutservice_req[i],currencyservice_req[i],emailservice_req[i],frontend_req[i],paymentservice_req[i],productcatalogservice_req[i],recommendationservice_req[i],shippingservice_req[i]))
            listmem = np.vstack((adservice_mem[i],cartservice_mem[i],checkoutservice_mem[i],currencyservice_mem[i],emailservice_mem[i],frontend_mem[i],paymentservice_mem[i],productcatalogservice_mem[i],recommendationservice_mem[i],shippingservice_mem[i]))

            listpod = torch.tensor(listpod, dtype=torch.float32)
            listcpu = torch.tensor(listcpu, dtype=torch.float32)
            listres = torch.tensor(listres, dtype=torch.float32)
            listreq = torch.tensor(listreq, dtype=torch.float32)
            listreq = torch.tensor(listmem, dtype=torch.float32)

            
            listt = torch.cat((listpod,listcpu,listres,listreq),dim=1)
            
            yy=torch.unsqueeze(listt,dim=0)
            xx=torch.cat((xx,yy),dim=0)
            
        np.savez("predict_scale", xx)
        all_data = predict_read_and_generate_dataset(graph_signal_matrix_filename='predict_scale.npz', num_of_hours=1, num_for_predict=1, points_per_hour=80, save=True)

        print('generating data is over and begin predict')
        
        model_config = load_config(args.model_config_path)
        train_config = load_config(args.train_config_path)
        torch.manual_seed(train_config['seed'])
        # ----------------------- Load data ------------------------
        Scaler = getattr(sys.modules['utils.scaler'], train_config['scaler'])#StandardScaler
        data_scaler = Scaler(axis=(0, 1, 2))

        data_config = model_config['dataset']
        device = torch.device(data_config['device'])
        data_name = 'predict_scale_r1ssj.npz'

        dataset = TPDataset2(os.path.join(data_config['data_dir'], data_name))
        data_scaler.fit(dataset.data['x'])
        dataset.fit(data_scaler)#
        data_loader = DataLoader(dataset, batch_size=data_config['batch_size'])
        # --------------------- predict setting --------------------
        net_name = args.model_name
        net_config = model_config[net_name]
        net_config.update(data_config)
        Model = getattr(AdapGL, net_name, None)
        if Model is None:
            raise ValueError('Model {} is not right!'.format(net_name))
        net_pred = Model(**net_config).to(device)
        
        net_pred.load_state_dict(torch.load('xxx.pkl'))###import model
        adj = np.load('best_adj_mx.npy')
        torch_adj = torch.from_numpy(adj)
        
        datazz=torch.from_numpy(data_loader.dataset.data['x'])
        pred = net_pred(datazz,torch_adj).detach()
        pred = data_scaler.inverse_transform(data=pred,axis=0)

        adservice = pred[-1,0,0]
        cartservice = pred[-1,0,1]
        checkoutservice = pred[-1,0,2]
        currencyservice = pred[-1,0,3]
        emailservice = pred[-1,0,4]
        frontend = pred[-1,0,5]
        paymentservice = pred[-1,0,6]
        productcatalogservice = pred[-1,0,7]
        recommendationservice = pred[-1,0,8]
        shippingservice = pred[-1,0,9]
        
        pods_num_to_scale ={}
        if(math.isnan(adservice)):
            adservice=1
        if(math.isnan(cartservice)):
            cartservice=1
        if(math.isnan(checkoutservice)):
            checkoutservice=1
        if(math.isnan(currencyservice)):
            currencyservice=1
        if(math.isnan(emailservice)):
            emailservice=1
        if(math.isnan(frontend)):
            frontend=1
        if(math.isnan(paymentservice)):
            paymentservice=1
        if(math.isnan(productcatalogservice)):
            productcatalogservice=1
        if(math.isnan(recommendationservice)):
            recommendationservice=1
        if(math.isnan(shippingservice)):
            shippingservice=1

        restriction=0.35
        if((float(adservice)-math.floor(float(adservice)))<restriction):
            pods_num_to_scale['adservice']=1
        else:
            pods_num_to_scale['adservice']=1
            
        if((float(cartservice)-math.floor(float(cartservice)))<restriction):
            pods_num_to_scale['cartservice']=math.floor(float(cartservice))
        else:
            pods_num_to_scale['cartservice']=math.ceil(float(cartservice))
            
        if((float(checkoutservice)-math.floor(float(checkoutservice)))<restriction):
            pods_num_to_scale['checkoutservice']=math.floor(float(checkoutservice))
        else:
            pods_num_to_scale['checkoutservice']=math.ceil(float(checkoutservice))
            
        if((float(currencyservice)-math.floor(float(currencyservice)))<0.5):
            pods_num_to_scale['currencyservice']=math.floor(float(checkoutservice))
        else:
            pods_num_to_scale['currencyservice']=math.ceil(float(currencyservice))
            
        if((float(emailservice)-math.floor(float(emailservice)))<0.5):
            pods_num_to_scale['emailservice']=math.floor(float(emailservice))
        else:
            pods_num_to_scale['emailservice']=math.ceil(float(emailservice))
                
        if((float(frontend)-math.floor(float(frontend)))<restriction):
            pods_num_to_scale['frontend']=math.floor(float(frontend))
        else:
            pods_num_to_scale['frontend']=math.ceil(float(frontend))          
            
        if((float(paymentservice)-math.floor(float(paymentservice)))<0.5):
            pods_num_to_scale['paymentservice']=math.floor(float(paymentservice))
        else:
            pods_num_to_scale['paymentservice']=math.ceil(float(paymentservice))       
            
        if((float(productcatalogservice)-math.floor(float(productcatalogservice)))<restriction):
            pods_num_to_scale['productcatalogservice']=math.floor(float(productcatalogservice))
        else:
            pods_num_to_scale['productcatalogservice']=math.ceil(float(productcatalogservice))        
            
        if((float(recommendationservice)-math.floor(float(recommendationservice)))<restriction):
            pods_num_to_scale['recommendationservice']=math.floor(float(recommendationservice))
        else:
            pods_num_to_scale['recommendationservice']=math.ceil(float(recommendationservice))  
        if((float(shippingservice)-math.floor(float(shippingservice)))<0.5):
            pods_num_to_scale['shippingservice']=math.floor(float(shippingservice))
        else:
            pods_num_to_scale['shippingservice']=math.ceil(float(shippingservice)) 
        end = time.time()
        print(end-start)
        for svc in svc_ls:
            if pods_num_to_scale[svc]<=0:
                pods_num_to_scale[svc]=1
            k8s_op.scale_deployment_by_replicas(svc, "boutiquessj", pods_num_to_scale[svc])
        print("after scale svc:", pods_num_to_scale)
        end = time.time()
        temp = end-start
        print(temp)
        if(temp<55):
            time.sleep(55-temp)
        c_temp+=1
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_config_path', type=str, default='/config/train_pems04.yaml',
                        help='Config path of models')
    parser.add_argument('--train_config_path', type=str, default='/config/train_config.yaml',
                        help='Config path of Trainer')
    parser.add_argument('--model_name', type=str, default='AdapGLA', help='Model name to train')
    parser.add_argument('--num_epoch', type=int, default=5, help='Training times per epoch')
    parser.add_argument('--num_iter', type=int, default=5, help='Maximum value for iteration')
    parser.add_argument('--model_save_path', type=str, default='/model_states/AdapGLA_1.pkl',
                        help='Model save path')
    parser.add_argument('--max_graph_num', type=int, default=3, help='Volume of adjacency matrix set')
    args = parser.parse_args()

    main(args)
