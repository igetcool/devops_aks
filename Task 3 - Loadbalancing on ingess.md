# Task 2 - Loadbalancing on ingess

### Ingress 의 구현체인 Contorller 설치와 로드밸런싱 실습
#


1. 웹브라우저로 아래 링크에 접속하여 ingress controller 설치 전 확인
```
https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.0/deploy/static/provider/baremetal/deploy.yaml
```

링크처럼 1개의 yaml 파일안에 여러 리소스를 구현할 수 있습니다.

2. nginx ingress controller 설치
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.0/deploy/static/provider/baremetal/deploy.yaml
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
```  
위 명령어처럼 링크에 있는 yaml파일도 kubectl을 통해 제어할 수 있습니다.

라벨 세팅 및 확인
```
kubectl label node k8s-worker1 homepage=ok
kubectl label node k8s-worker1 customer=ok
kubectl label node k8s-worker2 homepage=ok
kubectl label node k8s-worker2 schedule=ok
kubectl label node k8s-worker3 customer=ok
kubectl label node k8s-worker3 schedule=ok
kubectl get nodes --show-labels

kubectl get nodes -l homepage=ok
kubectl get nodes -l customer=ok
kubectl get nodes -l schedule=ok
```
3. 홈페이지에 관한 Service, Pod 리소스 생성
```
cat <<EOF | kubectl create -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: hp-daemonset
spec:
  selector:
    matchLabels:
      category: homepage
  template:
    metadata:
      labels:
        category: homepage
    spec:
      nodeSelector:
        homepage: ok
      containers:
      - name: container
        image: ghcr.io/wsjang619/home
---
apiVersion: v1
kind: Service
metadata:
  name: hp-svc
spec:
  selector:
    category: homepage
  ports:
  - port: 8080
    targetPort: 80
EOF
```

4. 고객센터에 관한 Service, Pod 리소스 생성
```
cat <<EOF | kubectl create -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: ct-daemonset
spec:
  selector:
    matchLabels:
      category: customer
  template:
    metadata:
      labels:
        category: customer
    spec:
      nodeSelector:
        customer: ok
      containers:
      - name: container
        image: ghcr.io/wsjang619/customer
---
apiVersion: v1
kind: Service
metadata:
  name: ct-svc
spec:
  selector:
    category: customer
  ports:
  - port: 8080
    targetPort: 80
EOF
```


5. 연간 스케쥴 페이지에 관한 Service, Pod 리소스 생성
```
cat <<EOF | kubectl create -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: sc-daemonset
spec:
  selector:
    matchLabels:
      category: schedule
  template:
    metadata:
      labels:
        category: schedule
    spec:
      nodeSelector:
        schedule: ok
      containers:
      - name: container
        image: ghcr.io/wsjang619/schedule
---
apiVersion: v1
kind: Service
metadata:
  name: sc-svc
spec:
  selector:
    category: schedule
  ports:
  - port: 8080
    targetPort: 80
EOF
```

6. 로드밸런싱 용 ingress 생성
```
cat <<EOF | kubectl create -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: lb-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hp-svc
            port:
              number: 8080
      - path: /customer
        pathType: Prefix
        backend:
          service:
            name: ct-svc
            port:
              number: 8080
      - path: /schedule
        pathType: Prefix
        backend:
          service:
            name: sc-svc
            port:
              number: 8080
EOF
```

7. 위에서 생성한 리소스 확인
```
kubectl get pod -o wide
kubectl get service
kubectl get ingress
```

8. ingress controller 가 만든 Nodeport 유형의 서비스의 Nodeport를 확인
```
kubectl get svc -n ingress-nginx
```

9. 노드의 ip와 13과정에서 확인한 Nodeport를 확인하여 접근시도
```
curl <node ip>:<13에서 확인한 portnumber>
curl <node ip>:<13에서 확인한 portnumber>/customer
curl <node ip>:<13에서 확인한 portnumber>/schedule
```

10. 위 정보로 nlb 구성 


15. clear
```
kubectl delete pod,svc,ingress --all
```
