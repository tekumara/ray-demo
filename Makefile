include *.mk

## create k3s cluster
cluster:
# add agents to have enough cluster capacity on an instance with only 2 CPU
# use latest version of k3s with traefik 2.5 which supports networking.k8s.io/v1
	k3d cluster create ray -i rancher/k3s:v1.23.6-k3s1 -p "10001:80@loadbalancer" --agents 2 --wait
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write ray)"

## install kuberay operator using quickstart manifests
export KUBERAY_VERSION=v0.3.0
kuberay:
	kubectl get customresourcedefinition.apiextensions.k8s.io/rayclusters.ray.io || kubectl create -k "github.com/ray-project/kuberay/manifests/cluster-scope-resources?ref=${KUBERAY_VERSION}&timeout=90s"
	kubectl apply -k "github.com/ray-project/kuberay/manifests/base?ref=${KUBERAY_VERSION}&timeout=90s"

## create ray cluster
cluster = complete
service = raycluster-$(cluster)-head-svc
raycluster:
	kubectl apply -f ray-operator/config/samples/ray-cluster.$(cluster).yaml

## install k3d ingress
k3d-ingress:
	helm upgrade --install example-cluster-ingress ingress --set serviceName=$(service) --wait

## get shell on head pod
shell:
	kubectl exec -i -t service/$(service) -- /bin/bash

## port forward the service
forward:
	kubectl port-forward svc/$(service) 10001:10001 8265:8265

## remove cluster
delete:
	kubectl delete raycluster raycluster-$(cluster)

## ping server endpoint
ping: $(venv)
	$(venv)/bin/python -m rayexample.ping

## enable trafefik debug loglevel
tdebug:
	kubectl -n kube-system patch deployment traefik --type json -p '[{"op": "add", "path": "/spec/template/spec/containers/0/args/0", "value":"--log.level=DEBUG"}]'

## tail traefik logs
tlogs:
	kubectl -n kube-system logs -l app.kubernetes.io/name=traefik -f

## forward traefik dashboard
tdashboard:
	@echo Forwarding traefik dashboard to http://localhost:9000/dashboard/
	tpod=$$(kubectl get pod -n kube-system -l app.kubernetes.io/name=traefik -o custom-columns=:metadata.name --no-headers=true) && \
		kubectl -n kube-system port-forward $$tpod 9000:9000
