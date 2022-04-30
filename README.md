# ray demo

Ray cluster with examples running on Kubernetes (k3d).

## Getting started

Prerequisites:

- docker compose
- [k3d](https://github.com/rancher/k3d) to create a k3s kubes cluster
- python 3
- [grpcurl](https://github.com/fullstorydev/grpcurl) for network debugging (optional)

Create virtualenv:

```
make install
```

Create the k3s kubes cluster using k3d:

```
make cluster
```

Now set your kube context before running further commands.


Install the ray cluster into kubes

* stock python operator: `make ray-kube-install`
* kuberay operatoer: `make kuberay`

Ping head node (once pod is ready):

```
make ping
```

Run example application

```
python rayexample/cluster_info.py
```

Run shell on head pod:

```
kubectl exec -i -t -n ray service/example-cluster-ray-head -- /bin/bash
```

## Ray on Kubes

The [ray helm chart](deploy/charts/ray) deploys the ray CRDs and the [ray operator](https://github.com/ray-project/ray/tree/ray-1.12.0/python/ray/ray_operator) (python) to the default namespace.

The ray operator creates:

- the ray namespace
- a head pod running gcs_server, redis-server, raylet
- 2 worker pods running raylet
- a ClusterIP Service

The helm chart has been taken from the [1.12.0 tree](https://github.com/ray-project/ray/tree/ray-1.12.0/deploy/charts/ray) and updated to use the [rayproject/ray:1.12.0](https://hub.docker.com/r/rayproject/ray) image for the ray operator, head and worker nodes. It is 1.21 GB (!). It is built on python 3.7. Alternate images can be specified in [values.yaml](deploy/charts/ray/values.yaml), eg: [nightly-py39-cpu](https://hub.docker.com/r/rayproject/ray/tags?page=1&name=nightly)

Each pod needs 1 CPU and 1GB RAM, for a total of 4 CPU (ie: operator + head + 2 workers) and 4GB RAM.

### Kuberay

There's also a golang [ray-operator](https://github.com/ray-project/kuberay), which is not yet shipped with ray.

## Ingress

The Ray client server will be exposed on localhost port 10001.
The Ray dashboard can be accessed on [http://localhost:10001/dashboard/](http://localhost:10001/dashboard/)
