# ray example

Prefect multi-module flow running on Kubernetes.

## Getting started

Prerequisites:

- docker compose
- [k3d](https://github.com/rancher/k3d) to create a k3s kubes cluster
- python 3

Install virtualenv:

```
pip install -r requirements.txt
```

Create the kubes cluster:

```
make cluster
```

Install the ray cluster into kubes (set your kube context before running this):

```
make ray-kube-install
```

Run shell on head pod:

```
kubectl exec -i -t -n ray service/example-cluster-ray-head -- /bin/bash
```

## Ray on Kubes

The [ray helm chart](deploy/charts/ray) deploys the [ray operator](https://github.com/ray-project/ray/tree/0c786b1/python/ray/ray_operator) (python). NB: there's also a golang [ray-operator](https://github.com/ray-project/kuberay), which is not yet shipped with ray.

The ray operator creates:

- a head node running gcs_server, redis-server, raylet
- 2 worker nodes running raylet
- a ClusterIP Service

The [rayproject/ray](https://hub.docker.com/r/rayproject/ray) image is used by the ray operator, head and worker nodes. It is 2.5GB (!). It is built on python 3.7. Alternate images can be specified in [values.yaml](deploy/charts/ray/values.yaml), eg: [nightly-py39-cpu](https://hub.docker.com/r/rayproject/ray/tags?page=1&name=nightly)

Each pod needs requests 1 CPU, for a total of 4 CPU (ie: operator + head + 2 workers).

## Ingress

```
# forward dashboard to http://localhost:8265
kubectl -n ray port-forward service/example-cluster-ray-head 8265:8265

# forward server to http://localhost:10001
kubectl -n ray port-forward service/example-cluster-ray-head 10001:10001
```
