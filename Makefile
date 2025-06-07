include *.mk

.PHONY: raycluster

## create k3s cluster
cluster:
# add agents to have enough cluster capacity on an instance with only 2 CPU
# increase eviction threshold to provide more disk space headroom as per
# https://github.com/k3d-io/k3d/issues/133#issuecomment-1345263732
	k3d cluster create ray --registry-create ray-registry:0.0.0.0:5550 --agents 2 --wait \
		-p 10001:10001@loadbalancer -p 8265:8265@loadbalancer -p 6379:6379@loadbalancer \
		--k3s-arg '--kubelet-arg=eviction-hard=imagefs.available<1%,nodefs.available<1%@agent:*' \
		--k3s-arg '--kubelet-arg=eviction-minimum-reclaim=imagefs.available=1%,nodefs.available=1%@agent:*' \
		--k3s-arg '--kubelet-arg=eviction-hard=imagefs.available<1%,nodefs.available<1%@server:0' \
		--k3s-arg '--kubelet-arg=eviction-minimum-reclaim=imagefs.available=1%,nodefs.available=1%@server:0'
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write ray)"

kuberay_version = 1.3.2

## install kuberay operator using quickstart manifests
kuberay:
# add helm repo and update to latest
	helm repo add kuberay https://ray-project.github.io/kuberay-helm/
	helm repo update kuberay
# install CRDs & kuberay operator
	helm upgrade --install kuberay-operator kuberay/kuberay-operator --version $(kuberay_version) --wait --debug > /dev/null

## build and push docker image
push: service=app-$(shell uname -m)
push:
	docker compose build $(service) && docker compose push $(service)

## create ray cluster
raycluster: push
	helm upgrade --install raycluster kuberay/ray-cluster --version $(kuberay_version) --values infra/raycluster/values.yaml \
		--wait --debug > /dev/null
# restart needed because of https://github.com/ray-project/kuberay/issues/234
	make restart

## create ray cluster without custom image
raycluster-std:
	helm upgrade --install raycluster kuberay/ray-cluster --version $(kuberay_version) --values infra/raycluster/values.yaml \
		--wait --debug --set image.repository=rayproject/ray --set image.tag=2.45.0-py311 > /dev/null
# restart needed because of https://github.com/ray-project/kuberay/issues/234
	make restart

## restart the ray cluster
restart:
	kubectl delete pod -lapp.kubernetes.io/name=kuberay --wait=false || true

cluster = kuberay
service = raycluster-$(cluster)-head-svc

## install k3d ingress
ingress-k3d:
	helm upgrade --install rayingress infra/ingress-k3d --set cluster=raycluster-$(cluster) --wait

## install nginx ingress with cert-manager
ingress-nginx:
	helm upgrade --install rayingress infra/ingress-nginx --wait

## get shell on head pod
shell:
	kubectl exec -i -t service/$(service) -- /bin/bash

## port forward the service
forward:
	kubectl port-forward svc/$(service) 10001:10001 8265:8265 6379:6379

## status
status:
	uv run ray status --address localhost:6379 -v

## print ray commit
version:
	uv run python -c 'import ray; print(f"{ray.__version__} {ray.__commit__}")'

## remove cluster
delete:
	kubectl delete raycluster raycluster-$(cluster)

## ping server endpoint
ping:
	uv run python -m raydemo.ping

## cluster info
info:
	uv run python -m raydemo.cluster_info

## head node logs
logs-head:
	kubectl logs -lray.io/cluster=raycluster-kuberay -lray.io/node-type=head -c ray-head -f

## worker node logs
logs-worker:
	kubectl logs -lray.io/group=workergroup -f

## auto-scaler logs
logs-as:
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

## run tf_mnist on cluster
tf_mnist:
	uv run python -m raydemo.tf_mnist --address ray://localhost:10001

## list jobs
job-list:
	uv run ray job list --address http://localhost:8265

## serve example
serve:
	uv run serve run raydemo.serve.hello:language_classifier

## serve ping
serve-ping:
	curl -X POST http://localhost:8000 \
		-H "Content-Type: application/json" \
		-d '{"language": "spanish", "name": "world"}'


## serve chain example
serve-chain:
	uv run python -m raydemo.serve.chain

## start ray
start:
	uv run ray start --head

## job submit example (run make start first)
job-submit: export RAY_ADDRESS=ray://localhost:10001
job-submit:
	uv run ray job submit --runtime-env runtime.yaml -- python raydemo/script.py
