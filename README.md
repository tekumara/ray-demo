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

- kuberay operator: `make operator raycluster` (recommended)
- stock python operator: `make ray-kube-install`

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

## Kuberay

The golang ray operator called [kuberay](https://github.com/ray-project/kuberay) is not yet shipped with ray but will supersede the stock python operator (see below).

The following has been copied from the [e80e203 tree](https://github.com/ray-project/kuberay/tree/e80e203):

- [helm-chart/](helm-chart/) - we don't use these
- [ray-operator/config/](ray-operator/config/) - kustomize templates, which seem more up to date than the helm charts

`make operator` uses the kustomize templates to create:

- namespace/ray-system
- customresourcedefinition.apiextensions.k8s.io/rayclusters.ray.io
- customresourcedefinition.apiextensions.k8s.io/rayservices.ray.io
- serviceaccount/kuberay-operator
- role.rbac.authorization.k8s.io/kuberay-operator-leader-election
- clusterrole.rbac.authorization.k8s.io/kuberay-operator
- rolebinding.rbac.authorization.k8s.io/kuberay-operator-leader-election
- clusterrolebinding.rbac.authorization.k8s.io/kuberay-operator
- service/kuberay-operator
- deployment.apps/kuberay-operator

`make raycluster` creates the following in the default namespace:

- raycluster-mini-head-svc service
- ray head pod

`make delete` removes the ray cluster

For more info the [ray-operator readme](https://github.com/ray-project/kuberay/tree/master/ray-operator).

## Ray on Kubes (stock python operator)

The [ray helm chart](deploy/charts/ray) deploys the ray CRDs and the [ray operator](https://github.com/ray-project/ray/tree/ray-1.12.1/python/ray/ray_operator) (python) to the default namespace.

The ray operator creates:

- the ray namespace
- a head pod running gcs_server, redis-server, raylet
- 2 worker pods running raylet
- a ClusterIP Service

The helm chart has been taken from the [1.12.1 tree](https://github.com/ray-project/ray/tree/ray-1.12.1/deploy/charts/ray) and updated:

- to use the [rayproject/ray:1.12.1](https://hub.docker.com/r/rayproject/ray) image for the ray operator, head and worker nodes. It is 1.21 GB (!). It is built on python 3.7. Alternate images can be specified in [values.yaml](deploy/charts/ray/values.yaml), eg: [nightly-py39-cpu](https://hub.docker.com/r/rayproject/ray/tags?page=1&name=nightly)
- bumped the memory from 512Mi to 1Gi

Each pod needs 1 CPU and 1GB RAM, for a total of 4 CPU (ie: operator + head + 2 workers) and 4GB RAM.

The [ray helm chart](deploy/charts/ray) deploys the ray CRDs and the [ray operator](https://github.com/ray-project/ray/tree/ray-1.12.1/python/ray/ray_operator) (python) to the default namespace.

The ray operator creates:

- the ray namespace
- a head pod running gcs_server, redis-server, raylet
- 2 worker pods running raylet
- a ClusterIP Service

The helm chart has been taken from the [1.12.1 tree](https://github.com/ray-project/ray/tree/ray-1.12.1/deploy/charts/ray) and updated:

- to use the [rayproject/ray:1.12.1](https://hub.docker.com/r/rayproject/ray) image for the ray operator, head and worker nodes. It is 1.21 GB (!). It is built on python 3.7. Alternate images can be specified in [values.yaml](deploy/charts/ray/values.yaml), eg: [nightly-py39-cpu](https://hub.docker.com/r/rayproject/ray/tags?page=1&name=nightly)
- bumped the memory from 512Mi to 1Gi

Each pod needs 1 CPU and 1GB RAM, for a total of 4 CPU (ie: operator + head + 2 workers) and 4GB RAM.

## Ingress

The Ray client server will be exposed on localhost port 10001.
The Ray dashboard can be accessed on [http://localhost:10001/dashboard/](http://localhost:10001/dashboard/)
