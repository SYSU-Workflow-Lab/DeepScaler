import kubernetes as k8s
import urllib3

urllib3.disable_warnings()


class K8sOp:

    def __init__(self):
        # self.config = config
        # if config["is_remote"]:
        # vpc and outer net -> use .kube/config
        k8s.config.load_kube_config(config_file="/root/.kube/config")
        # else:
        #     # pod version -> not use .kube/config
        #     k8s.config.load_incluster_config()
        self.k8sapi = k8s.client.CoreV1Api()
        #self.k8sexapi = k8s.client.ExtensionsV1beta1Api()
        self.k8sexapi = k8s.client.AppsV1Api()

    def get_deployment_instance(self, svc_name, namespace):
        k8sres = self.k8sexapi.list_namespaced_deployment(namespace)
        rt = None
        for r in k8sres.items:
            if r.metadata.name == svc_name:
                rt = r
                break
        return rt

    def scale_deployment_by_instance(self, deploy_instance, replicas):
        deploy_instance.spec.replicas = replicas
        k8sres = self.k8sexapi.patch_namespaced_deployment(
            deploy_instance.metadata.name,
            deploy_instance.metadata.namespace,
            deploy_instance
        )
        return k8sres

    def scale_deployment_by_replicas(self, svc_name, namespace, replicas):
        ins = self.get_deployment_instance(svc_name, namespace)
        if ins is None:
            print("Error: No this deployment!!")
            return
        self.scale_deployment_by_instance(ins, replicas)
    
    def get_deployment_replicas(self, svc_name, namespace):
        # res = self.k8sexapi.read_namespaced_replica_set(svc_name, namespace)
        res = self.k8sexapi.read_namespaced_deployment_scale(svc_name, namespace)
        return res.spec.replicas
