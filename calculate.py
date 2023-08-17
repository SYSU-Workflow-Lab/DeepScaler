svc_ls = ["frontend","adservice", "cartservice", "checkoutservice","currencyservice", "emailservice","paymentservice","productcatalogservice","recommendationservice","shippingservice"]

metrics = ['res', 'req', 'pod', 'cpu']

sla_up = 0.2
sla_down = 0.1
sla_above_count = 0
sla_down_count = 0
counter = 0
cpu_usage_count = 0
cpu_usage_sum = 0
filter_set = {}
pod_map = {}
pod_map_all = {}
mse = 0
mae = 0
res_sum = 0
res_ave = 0
for svc in svc_ls:
  pod_map[svc] = 0

iternum = 1
for svc in svc_ls:
  for m in metrics:
    t_file = '/ssj/ssj/boutiquessj/pyboutique/newData/3.2.2aws/{}_{}_{}.log'.format(iternum, svc, m)
    if m == 'res' and svc == 'frontend':
      data = open(t_file).readlines()
      idx = 0
      for line in data:
        idx += 1
        res = float(line.strip())
        # 剔除错误数据
        if res <= 0.001:
          filter_set[idx] = True
          continue
        counter += 1
        res_sum += res 
        if res > sla_up:
            sla_above_count += 1
        if res < sla_down:
            sla_down_count += 1
      print("sla volate up: %.2f%%" % (sla_above_count / counter * 100))
      print("sla volate down: %.2f%%" % (sla_down_count / counter * 100))
      res_ave = res_sum/counter

    if m == 'res' and svc == 'frontend':
      data = open(t_file).readlines()
      idx = 0
      for line in data:
        idx += 1
        if idx in filter_set:
          continue
        res = float(line.strip())
        # mse += (res-res_ave)**2
        mae += abs(res-0.15)#0.15 average
      mae /= counter
      print("mae:",mae)
    if m == 'cpu':
      data = open(t_file).readlines()
      idx = 0
      for line in data:
        idx += 1
        if idx in filter_set:
          continue
        cpu = float(line.strip())
        if cpu < 100 and cpu >0 :
          cpu_usage_sum += cpu
          cpu_usage_count += 1
    if m == 'pod':
      data = open(t_file).readlines()
      idx = 0
      for line in data:
        idx += 1
        if idx in filter_set:
          continue
        podn = int(line.strip())
        pod_map[svc] += podn
      pod_map_all[svc] = pod_map[svc]
      pod_map[svc] /= counter

cost = 0
cpu_core = {"adservice":0.3, "cartservice":0.3, "checkoutservice":0.2,"currencyservice":0.2, "emailservice":0.2,"frontend":0.2,"paymentservice":0.2,"productcatalogservice":0.2,"recommendationservice":0.2,"shippingservice":0.2}

for svc in svc_ls:
  cost += cpu_core[svc]*pod_map[svc]
  print(svc, "pod num:", pod_map[svc])
print("cost:",cost)