include *.mk

.PHONY: raycluster

## create k3s cluster
cluster:
# add agents to have enough cluster capacity on an instance with only 2 CPU
# use latest version of k3s with traefik 2.5 which supports networking.k8s.io/v1
	k3d cluster create ray -i rancher/k3s:v1.23.6-k3s1 --agents 2 --wait \
		-p 10001:10001@loadbalancer -p 8265:8265@loadbalancer -p 6379:6379@loadbalancer
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write ray)"

kuberay_version = 0.4.0

## install kuberay operator using quickstart manifests
kuberay:
# add helm repo and update to latest
	helm repo add kuberay https://ray-project.github.io/kuberay-helm/
	helm repo update kuberay
# install CRDs & kuberay operator
	helm upgrade --install kuberay-operator kuberay/kuberay-operator --version $(kuberay_version) --wait --debug > /dev/null

## create ray cluster
raycluster:
	helm upgrade --install raycluster kuberay/ray-cluster --version $(kuberay_version) --values raycluster/values.yaml --wait --debug > /dev/null

## restart the ray cluster
restart:
	kubectl delete pod -lapp.kubernetes.io/name=kuberay --wait=false

cluster = kuberay
service = raycluster-$(cluster)-head-svc

## install k3d ingress
k3d-ingress:
	helm upgrade --install example-cluster-ingress ingress --set cluster=raycluster-$(cluster) --wait

## get shell on head pod
shell:
	kubectl exec -i -t service/$(service) -- /bin/bash

## port forward the service
forward:
	kubectl port-forward svc/$(service) 10001:10001 8265:8265 6379:6379

## status
status: $(venv)
	$(venv)/bin/ray status --address localhost:6379

## remove cluster
delete:
	kubectl delete raycluster raycluster-$(cluster)

## ping server endpoint
ping: $(venv)
	$(venv)/bin/python -m rayexample.ping

## head node logs
logs: $(venv)
	kubectl logs -lray.io/cluster=raycluster-kuberay -lray.io/node-type=head -c ray-head -f

## auto-scaler logs
logs-as: $(venv)
	kubectl logs -lray.io/cluster=raycluster-kuberay -lray.io/node-type=head -c autoscaler -f


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
