# ray demo

Ray cluster with examples running on Kubernetes (k3d).

## Prerequisites

- python 3
- [k3d](https://github.com/rancher/k3d) to create a k3s kubes cluster (optional)

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
- [stock](ray-stock-operator.md) python operator: `make ray-kube-install` (deprecated)

## Ingress

For k3d, run `make k3d-ingress`, else run `make forward`:

- The Ray client server will be exposed on localhost port 10001.
- The Ray dashboard can be accessed on [http://localhost:8265/](http://localhost:8265)
- The Ray GCS server will be exposed on localhost port 6379.

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

Kuberay consists of:

- [helm-chart/](https://github.com/ray-project/kuberay/tree/master/helm-chart) - helm charts for the apiserver, operator and a ray-cluster (recommended)
- [ray-operator/config/](https://github.com/ray-project/kuberay/tree/master/ray-operator/config) - kustomize templates, which seem more up to date than the helm charts. Includes
  - crd: the rayclusters, rayjobs, and rayservices CRDs
  - default: crd, rbac, manager, and ray-system namespace
  - manager: kuberay operator deployment and serivce
  - prometheus
  - rbac: roles, service accounts etc.
- [ray-operator/config/samples](ray-operator/config/samples): raycluster examples
- [manifests/](https://github.com/ray-project/kuberay/tree/master/manifests) kutomize quickstart manifests for installing the default template + [apiserver](https://github.com/ray-project/kuberay/tree/master/apiserver)

`make kuberay` installs the [kuberay-operator helm chart](https://github.com/ray-project/kuberay/tree/master/helm-chart/kuberay-operator) which creates:

[CRDs](https://github.com/ray-project/kuberay/tree/master/helm-chart/kuberay-operator/crds):

- customresourcedefinition.apiextensions.k8s.io/rayclusters.ray.io created
- customresourcedefinition.apiextensions.k8s.io/rayjobs.ray.io created
- customresourcedefinition.apiextensions.k8s.io/rayservices.ray.io created

And the following [resources](https://github.com/ray-project/kuberay/tree/master/helm-chart/kuberay-operator/templates) in the default namespace:

- ServiceAccount kuberay-operator
- ClusterRole rayjob-editor-role
- ClusterRole rayjob-viewer-role
- ClusterRole rayservice-editor-role
- ClusterRole rayservice-viewer-role
- ClusterRole kuberay-operator
- ClusterRoleBinding kuberay-operator
- Role kuberay-operator
- RoleBinding kuberay-operator
- Service kuberay-operator
- Deployment kuberay-operator 

`make raycluster` creates the following in the default namespace:

- raycluster-kuberay-head-svc service
- ray head pod with limits of 1 CPU and 2Gi memory
- ray worker pod with limits of 1 CPU and 2Gi memory

`make delete` removes the ray cluster

For more info see the [ray-operator readme](https://github.com/ray-project/kuberay/tree/master/ray-operator).

## Autoscaler notes

See [autoscaler.md](autoscaler.md)

## References 

- [RayCluster Configuration](https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/config.html)

## Sizing

See [[Feature][Docs][Discussion] Provider consistent guidance on resource Request and Limits #744](https://github.com/ray-project/kuberay/issues/744)

## Known issues

- [Pods aren't restarted when the RayCluster CRD image is updated](https://github.com/ray-project/kuberay/issues/234#issuecomment-1193074275)
- [core - ray logs CLI doesn't work for kubernetes raycluster](https://github.com/ray-project/ray/issues/31381)
