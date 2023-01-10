#  node & preset  
### 노드에 필요한 설정과 k8s 설치 전에 해야할 설정을 진행
#

1. 노드에서 hostname을 변경합니다.

Master Node
```
sudo -i
sudo hostnamectl set-hostname k8s-master
sudo -i
```

2. swap 해제
```
swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab
```

3. 방화벽 해제
```
sudo ufw disable
```

4. 필요 패키지 설치
```
sudo apt-get update -y
```
```
sudo apt-get install -y curl ethtool ebtables socat conntrack
```

5. iptables가 브리지된 트래픽을 보도록 허용
(Linux 노드의 iptables가 브리지된 트래픽을 올바르게 보기 위한 요구 사항으로 구성 net.bridge.bridge-nf-call-iptables에서 가 1로 설정되어 있는지 확인해야 합니다)
```
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system
```

6. Docker 설치
HTTPS를 통해 리포지토리를 사용할 수 있도록 패키지 인덱스를 업데이트하고 apt패키지를 설치합니다
```
sudo apt-get -y update
sudo apt-get -y install apt-transport-https ca-certificates curl gnupg lsb-release
```

Docker의 공식 GPG 키 추가
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
안정적인 저장소를 설정
```
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
도커 엔진 설치
```
sudo apt-get -y update
```
```
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
```

7. cgroup 설정
```
sudo mkdir /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF
```

8. Docker 실행 및 확인
```
sudo systemctl enable docker
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl status docker
```
![image](https://user-images.githubusercontent.com/92773629/137876933-cb530415-d5f5-4440-91fc-66f1e13c10d8.png)

키보드의 Q 키 또는 <Ctrl + C> 를 입력하면 다시 쉘을 받아옵니다.
