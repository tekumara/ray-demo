# ray demo

Ray cluster with examples running on Kubernetes (k3d).

## Prerequisites

- python 3
- [k3d](https://github.com/rancher/k3d) to create a k3s kubes cluster (optional)
- [grpcurl](https://github.com/fullstorydev/grpcurl) for network debugging (optional)

Create virtualenv:

```
make install
```

If needed, create a k3s kubes cluster using k3d (optional):

```
make cluster
```

Now set your kube context before running further commands.

## Getting started

Install the ray cluster into kubes:

- [kuberay](#kuberay) operator: `make kuberay raycluster` (recommended)
- [stock](ray-stock-operator.md) python operator: `make ray-kube-install`

## Ingress

For k3d, run `make k3d-ingress`:

- The Ray client server will be exposed on localhost port 10001.
- The Ray dashboard can be accessed on [http://localhost:10001/dashboard/](http://localhost:10001/dashboard/)

Else, run `make forward`:

- The Ray client server will be exposed on localhost port 10001.
- The Ray dashboard can be accessed on [http://localhost:8265/](http://localhost:8265)

## Usage

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
make shell
```

## Kuberay

[kuberay](https://github.com/ray-project/kuberay) is the new goland operator than will supersede the stock python operator. See this [Slack discussion](https://ray-distributed.slack.com/archives/C02GFQ82JPM/p1657910298502319) of the differences.

Kuberay consists of:

- [helm-chart/](https://github.com/ray-project/kuberay/tree/master/helm-chart) - we don't use these
- [ray-operator/config/](https://github.com/ray-project/kuberay/tree/master/ray-operator/config) - kustomize templates, which seem more up to date than the helm charts. Includes
    - crd: the rayclusters, rayjobs, and rayservices CRDs
    - default: crd, rbac, manager, and ray-system namespace 
    - manager: kuberay operator deployment and serivce
    - prometheus
    - rbac: roles, service accounts etc.
- [ray-operator/config/samples](ray-operator/config/samples): raycluster examples, copied into this repo from the [5934974 tree](https://github.com/ray-project/kuberay/tree/5934974/ray-operator/config/samples)
- [manifests/](https://github.com/ray-project/kuberay/tree/master/manifests) kutomize quickstart manifests for installing the default template + [apiserver](https://github.com/ray-project/kuberay/tree/master/apiserver)

`make kuberay` uses the kustomize manifests to create:

cluster scope resources:

- namespace/ray-system created
- customresourcedefinition.apiextensions.k8s.io/rayclusters.ray.io created
- customresourcedefinition.apiextensions.k8s.io/rayjobs.ray.io created
- customresourcedefinition.apiextensions.k8s.io/rayservices.ray.io created

base resources:

- serviceaccount/kuberay-apiserver created
- serviceaccount/kuberay-operator created
- role.rbac.authorization.k8s.io/kuberay-operator-leader-election created
- clusterrole.rbac.authorization.k8s.io/kuberay-apiserver created
- clusterrole.rbac.authorization.k8s.io/kuberay-operator created
- rolebinding.rbac.authorization.k8s.io/kuberay-operator-leader-election created
- clusterrolebinding.rbac.authorization.k8s.io/kuberay-apiserver created
- clusterrolebinding.rbac.authorization.k8s.io/kuberay-operator created
- service/kuberay-apiserver created
- service/kuberay-operator created
- deployment.apps/kuberay-apiserver created
- deployment.apps/kuberay-operator created

`make raycluster` creates the following in the default namespace:

- raycluster-mini-head-svc service
- ray head pod with 1 CPU and 2Gi memory

`make delete` removes the ray cluster

For more info see the [ray-operator readme](https://github.com/ray-project/kuberay/tree/master/ray-operator).

## Limitations

- [Pods aren't restarted when the RayCluster CRD image is updated](https://github.com/ray-project/kuberay/issues/234#issuecomment-1193074275)

