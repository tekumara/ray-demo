# ray demo

Ray cluster with examples running on Kubernetes (k3d).

## Prerequisites

- python 3
- [k3d](https://github.com/rancher/k3d) to create a k3s kubes cluster (optional)
- [helm](https://helm.sh/docs/intro/install/) to install the kuberay operator (optional)

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

Install the ray operator (kuberay) and a ray cluster:

```
make kuberay raycluster
```

## Ingress

For k3d, run `make ingress-k3d`:

- The Ray client server will be exposed on localhost port 10001.
- The Ray dashboard can be accessed on [http://localhost:8265/](http://localhost:8265)
- The Ray GCS server will be exposed on localhost port 6379.

Alternatives:

- no ingress: `make forward`
- nginx + cert-manager (dashboard only): `make ingress-nginx`

## Usage

Ping head node (once pod is ready):

```
make ping
```

Run example application

```
python raydemo/cluster_info.py
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
  - manager: kuberay operator deployment and service
  - prometheus
  - rbac: roles, service accounts etc.
- [ray-operator/config/samples](https://github.com/ray-project/kuberay/tree/master/ray-operator/config/samples): raycluster examples
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

## Examples

See examples in [raydemo](raydemo/).

Most examples will start a local ray instance. To use the cluster instead:

```
export RAY_ADDRESS=ray://127.0.0.1:10001
```

## Autoscaler notes

See [autoscaler.md](autoscaler.md)

## References

- [RayCluster Configuration](https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/config.html)

## Sizing

See [[Feature][Docs][Discussion] Provider consistent guidance on resource Request and Limits #744](https://github.com/ray-project/kuberay/issues/744)

## Known issues

- [[Data>] Dataset write_csv AttributeError: ‘Worker’ object has no attribute 'core_worker'](https://github.com/ray-project/ray/issues/35537)
- [core - ray logs CLI doesn't work for kubernetes raycluster](https://github.com/ray-project/ray/issues/31381)
- [[core] single docker image that can run on multiple platforms](https://github.com/ray-project/ray/issues/52475)
- [[core][dashboard]: Package already exists, skipping upload.](https://github.com/ray-project/ray/issues/53635)

Kuberay:

- [[Bug] Worker pods shouldn't terminate with status Error](https://github.com/ray-project/kuberay/issues/3442)
- [Pods aren't restarted when the RayCluster CRD image is updated](https://github.com/ray-project/kuberay/issues/234#issuecomment-1193074275)

Type hint issues:

- [[core] ray.remote Decorator's Return Type Cannot Be Determined by Type Checkers](https://github.com/ray-project/ray/issues/50410)
- [[core] Generate \*.pyi stubs for protobufs](https://github.com/ray-project/ray/issues/52482)
- [[serve] Cannot access attribute "bind" for class "function"](https://github.com/ray-project/ray/issues/52483)
- [[serve] error: "NoReturn" is not awaitable](https://github.com/ray-project/ray/issues/52491)
- [[serve] Cannot access attribute "result" for class "DeploymentResponseGenerator" Attribute "result" is unknown](https://github.com/ray-project/ray/issues/52493)
- [[core] actor constructor type hint should be ActorHandle](https://github.com/ray-project/ray/issues/52771)
- [[core] ActorHandle remote() return type hint should be ObjectRef not Unknown](https://github.com/ray-project/ray/issues/52772)
