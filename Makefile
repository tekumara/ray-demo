## create k3s cluster
cluster:
	k3d cluster create ray --wait
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write ray)"

## install ray
ray-kube-install:
	helm -n ray upgrade --install example-cluster --create-namespace deploy/charts/ray

include *.mk
