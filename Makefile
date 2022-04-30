## create k3s cluster
cluster:
# add agents to have enough cluster capacity on an instance with only 2 CPU
# use latest version of k3s with traefik 2.5 which supports networking.k8s.io/v1
	k3d cluster create ray -i rancher/k3s:v1.23.6-k3s1 -p "10001:80@loadbalancer" --agents 2 --wait
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write ray)"

## install ray using the stock ray operator
ray-kube-install: service = example-cluster-ray-head
ray-kube-install:
	helm -n ray upgrade --install example-cluster deploy/charts/ray --create-namespace --wait
	helm -n ray upgrade --install example-cluster-ingress ingress --set serviceName=$(service) --wait

## install ray using kuberay
kuberay: service = example-cluster-ray-head-svc
kuberay:
	kubectl apply -k ray-operator/config/crd
	helm -n kuberay-operator upgrade --install kuberay-operator helm-chart/kuberay-operator --create-namespace --wait
	helm -n ray upgrade --install example-cluster helm-chart/ray-cluster --create-namespace --wait
	helm -n ray upgrade --install example-cluster-ingress ingress --set serviceName=$(service) --wait

## ping server endpoint
ping:
	grpcurl -import-path ./protobuf/ -proto ray_client.proto -plaintext  -d '{ "type": "PING" }' localhost:10001 ray.rpc.RayletDriver/ClusterInfo

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

include *.mk
