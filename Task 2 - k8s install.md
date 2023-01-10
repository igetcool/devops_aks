# Task 3 - k8s install

###  kubernetes를 설치
#
1. kubeadm, kubelet, kubectl 설치
apt패키지 인덱스를 업데이트하고 Kubernetes apt저장소를 사용하는 데 필요한 패키지를 설치
```
sudo apt-get -y update
sudo apt-get install -y apt-transport-https ca-certificates curl
```
Google Cloud 공개 서명 키를 다운로드
```
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
```
Kubernetes apt리포지토리를 추가
```
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```
apt 패키지 색인을 업데이트하고, kubelet, kubeadm, kubectl을 설치하고 해당 버전을 고정
```
sudo apt-get -y update
```
sudo apt list -a kubeadm
```
sudo apt-get install -y kubelet=1.22.11-00 kubeadm=1.22.11-00 kubectl=1.22.11-00
```
```
sudo apt-mark hold kubelet kubeadm kubectl
```
```
systemctl enable --now kubelet
```

2. kubeadm 초기화
```
kubeadm init --pod-network-cidr=192.168.0.0/16 --apiserver-advertise-address=<master-private-ip>
```
출력결과(kubeadm join 이하 명령어)는 worker node를 다른 노드를 사용하여 연동할 때 사용하는 명령어 입니다.
3~5분 소요됩니다.
![image](https://user-images.githubusercontent.com/92773629/137877948-678049de-4e17-4e11-be31-00daee62ef62.png)




3. Master 노드 설정
사용자에 대해 kubectl이 작동하도록 설정
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
export KUBECONFIG=/etc/kubernetes/admin.conf
```

4. Calico 네트워크 플러그인 설치
```
kubectl create -f https://projectcalico.docs.tigera.io/manifests/tigera-operator.yaml
kubectl create -f https://projectcalico.docs.tigera.io/manifests/custom-resources.yaml

```
확인
watch kubectl get pods -n calico-system


![image](https://user-images.githubusercontent.com/92773629/137878112-476a8d5f-9399-46a9-acaa-5be0a5c0af84.png)

5. kubectl 자동완성 적용
```
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
source /etc/bash_completion
alias k=kubectl
complete -F __start_kubectl k
```


7. node 확인
```
kubectl get nodes
```
