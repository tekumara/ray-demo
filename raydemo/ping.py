import sys

import grpc
import grpc._channel
import ray.core.generated.ray_client_pb2 as ray_client_pb2
import ray.core.generated.ray_client_pb2_grpc as ray_client_pb2_grpc


def ping(address: str) -> ray_client_pb2.ClusterInfoResponse:
    with grpc.insecure_channel(address) as channel:
        stub = ray_client_pb2_grpc.RayletDriverStub(channel)
        return stub.ClusterInfo(ray_client_pb2.ClusterInfoRequest(type="PING"))


try:
    address = sys.argv[1]
except IndexError:
    address = "localhost:10001"

try:
    print(ping(address))
except grpc._channel._InactiveRpcError as e:  # noqa: SLF001
    print(f"{e.code()} {e.details()}")
    exit(42)
