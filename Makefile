## create k3s cluster
cluster:
	k3d cluster create ray -p "10001:10001@loadbalancer" -p "8265:8265@loadbalancer" -p "8000:8000@loadbalancer"  -p "10002:1001@server:0" --wait
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write ray)"

## install ray
ray-kube-install:
	helm -n ray upgrade --install example-cluster --create-namespace deploy/charts/ray

include *.mk
