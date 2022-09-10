from collections import Counter
import socket
import time

import ray

ray.init("ray://127.0.0.1:10001")

print('''This cluster consists of
    {} nodes in total
    {} CPU resources in total
    {} memory resources in total
'''.format(len(ray.nodes()), ray.cluster_resources()['CPU'], ray.cluster_resources()['memory']))

@ray.remote
def f():
    time.sleep(0.001)
    # Return IP address.
    return socket.gethostbyname('localhost')

object_ids = [f.remote() for _ in range(10000)]
ip_addresses = ray.get(object_ids)

print('Tasks executed')
for ip_address, num_tasks in Counter(ip_addresses).items():
    print('    {} tasks on {}'.format(num_tasks, ip_address))
