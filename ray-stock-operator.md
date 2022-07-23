# Ray on Kubes (stock python operator)

The [ray helm chart](deploy/charts/ray) deploys the ray CRDs and the [ray operator](https://github.com/ray-project/ray/tree/ray-1.12.1/python/ray/ray_operator) (python) to the default namespace.

Run `make ray-kube-install`. The ray operator creates:

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
