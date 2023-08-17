## Setup Kubernetes Cluster

The implementation of DeepScaler is based on Kubernetes.

### Install Docker

- Update the package list: `sudo apt update`.
- Install Docker: `sudo apt install docker.io` (tested on Docker version 20.10.12).
- Check the installation and version: `docker -v`.
- Repeat the process on each machine that will act as a node in the Kubernetes cluster.

### Start and Enable Docker

- Set Docker to launch at boot: `sudo systemctl enable docker`.
- Verify Docker is running: `sudo systemctl status docker`.
- Start Docker if it's not running: `sudo systemctl start docker`.
- Repeat the process on each machine that will act as a node in the Kubernetes cluster.

### Install Kubernetes

- Add Kubernetes signing key: `curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add`.
- Add Software Repositories because Kubernetes is not included in the default repositories: `sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"`.
- Install Kubernetes Admin (a tool that helps initialize a cluster):
    - `sudo apt install kubeadm kubelet kubectl`;
    - `sudo apt-mark hold kubeadm kubelet kubectl`;
    - `kubeadm version` (verify the installation, it's good to have the same version for stability);
- Repeat for all Kubernetes nodes.

### Deploy Kubernetes

- [**ALL**] Disable the swap memory on each server: `sudo swapoff -a`.
- [**ALL**] Assign unique hostname for each server node: `sudo hostnamectl set-hostname your_hostname`.
- [**MASTER**] Initialize Kubernetes on the master node: `sudo kubeadm init --pod-network-cidr=xxx`.
    - Once this command finishes, it will display a `kubeadm join` message at the end. Make a note of the whole entry because it will be used to join the worker nodes to the cluster.
    - `--pod-network-cidr=xxx` is for the flannel virtual network to work.
- [**MASTER**] Create a directory for the cluster:
    - `mkdir -p $HOME/.kube`;
    - `sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config`;
    - `sudo chown $(id -u):$(id -g) $HOME/.kube/config`;
- [**MASTER**] Deploy pod network to the cluster. A pod network is a way to allow communication between different nodes in the cluster.
    - `sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml`;
    - Verify the pod network is working: `kubectl get pods --all-namespaces`;
- [**WORKER**] Connect each worker node to the cluster.
    - `sudo kubeadm join --discovery-token abcdef.1234567890abcdef --discovery-token-ca-cert-hash sha256:1234..cdef 1.2.3.4:6443` (replace the alphanumeric codes with those from your master server during initialization);
    - If you forget the command or the token is expired, run `kubeadm token create --print-join-command` from the master server to get a new token.
- [**MASTER**] Check the worker nodes joined to the clusster: `kubectl get nodes`. You should have something like this:

```
ubuntu@dvorak:~$ kubectl get nodes
NAME         STATUS   ROLES    AGE   VERSION
dvorak       Ready    master   22m   v1.23.4
dvorak-2-1   Ready    worker   18m   v1.23.4
dvorak-2-2   Ready    worker   16m   v1.23.4
dvorak-2-3   Ready    worker   16m   v1.23.4
dvorak-2-4   Ready    worker   15m   v1.23.4
...
```

By going through all the instructions above, a Kubernetes cluster should be installed, deployed and ready for use.

[Optional] In order to get a kubectl on some other computer (e.g. laptop) to talk to your cluster, you need to copy the administrator `kubeconfig` file from your control-plane node to your workstation like this:

```
scp root@<control-plane-host>:/etc/kubernetes/admin.conf .
kubectl --kubeconfig ./admin.conf get nodes
```
