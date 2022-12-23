# Autoscaler


## Resources 

> Ray resources are logical and don’t need to have 1-to-1 mapping with physical resources. They are mainly used for admission control during scheduling.

> Resource requirements of tasks or actors do NOT impose limits on actual physical resource usage. For example, Ray doesn’t prevent a num_cpus=1 task from launching multiple threads and using multiple physical CPUs. It’s your responsibility to make sure tasks or actors use no more resources than specified via resource requirements.

Resource requirements include CPU, GPU, memory, and custom hardware. They can be fractional.

> Ray nodes start with pre-defiend CPU, GPU, and memory resources. The quantities of these resources on each node are set to the physical quantities auto detected by Ray.

See [Resources](https://docs.ray.io/en/latest/ray-core/scheduling/resources.html)

## Scheduling

> Ray makes sure that the sum of the resource requirements of all of the concurrently running tasks and actors on a given node does not exceed the node’s total resources.

They can be used to limit the amount of concurrency see [Pattern: Using resources to limit the number of concurrently running tasks](https://docs.ray.io/en/latest/ray-core/patterns/limit-running-tasks.html)

 
## Autoscaler

> The Ray autoscaler uses the logical resources expressed in task and actor annotations. For instance, if each Ray container spec in your RayCluster CR indicates a limit of 10 CPUs, and you submit twenty tasks annotated with @ray.remote(num_cpus=5), 10 Ray pods will be created to satisfy the 100-CPU resource demand.

Actual utilization is not considered for autoscaling.

> If a user tries to launch an actor, task, or placement group but there are insufficient resources, the request will be queued. The autoscaler adds nodes to satisfy resource demands in this queue. The autoscaler also removes nodes after they become idle for some time. A node is considered idle if it has no active tasks, actors, or objects.

eg:

Given:

```
worker:
  minReplicas: 1
  maxReplicas: 10
  resources:
    limits:
      cpu: "2"
      memory: "2G"
    requests:
      cpu: "2"
      memory: "2G"
```

And a job that requests 10000 remote functions with `num_cpus=2` the autoscaler will scale the nodes up to the max. If remote function is quick, the 10000 tasks may complete on an existing node before the autoscaler completes. The autoscaler will then start scaling down.

## Troubleshooting

> The autoscaler could not find a node type to satisfy the request

The autoscaler will only schedule a task on a node (ie: pod) that matches the resource requests, eg:

```
@ray.remote(num_cpus=2)
```

Will only run on a pod that has request/limits of 2 CPUs. If no such pods exist you'll get the above error. See [#846](https://github.com/ray-project/kuberay/issues/846)
