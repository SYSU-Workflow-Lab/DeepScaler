import torch
import numpy as np
from metrics_fetch import save_all_fetch_data
from prepareData import read_and_generate_dataset

# 定义服务和指标
services = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"]
metrics = ['pod', 'cpu', 'res', 'req', 'mem']

# 收集数据
times_train = [
    ('2023-04-20 15:49:40', '2023-04-20 19:40:34')
]
save_all_fetch_data(times_train, 1, root_dir='/data/train/', interval=60, services=services, metrics=metrics)

# 读取并整理数据
def read_and_stack_data(service, metric):
    file = f'/data/train/1_{service}_{metric}.log'
    return np.genfromtxt(file, dtype=np.double)[:, np.newaxis]

data_tensors = {}
for service in services:
    for metric in metrics:
        data_tensors[f'{service}_{metric}'] = read_and_stack_data(service, metric)

# 合并数据
timeLen = len(data_tensors[services[0] + '_cpu'])
combined_data = torch.tensor([]).to(torch.float32)
for i in range(timeLen):
    combined = []
    for metric in metrics:
        combined.append(torch.tensor(np.vstack([service_data[i] for service_data in data_tensors.values() if metric in service_data])).T)
    combined_data = torch.cat((combined_data, torch.cat(combined, dim=1)), dim=0)

combined_data = combined_data[1:]  # 移除第一个空元素
print(combined_data.shape)
np.savez("/data/train1", combined_data.numpy())  # 保存数据

# 读取并生成测试数据集
all_data = read_and_generate_dataset(graph_signal_matrix_filename='/data/train1.npz', num_of_hours=1, num_for_predict=1, points_per_hour=80, save=True)
