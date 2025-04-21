# File name: chain.py
from typing import cast

from ray import serve
from ray.serve.handle import DeploymentHandle, DeploymentResponse


@serve.deployment
class Adder:
    def __init__(self, increment: int):
        self._increment = increment

    def __call__(self, val: int) -> int:
        return val + self._increment


@serve.deployment
class Multiplier:
    def __init__(self, multiple: int):
        self._multiple = multiple

    def __call__(self, val: int) -> int:
        return val * self._multiple


@serve.deployment(
    ray_actor_options={
        "runtime_env": {"env_vars": {"RAY_DEBUG": "1"}},
    },
)
class Ingress:
    def __init__(self, adder: DeploymentHandle, multiplier: DeploymentHandle):
        self._adder = adder
        self._multiplier = multiplier

    async def __call__(self, input: int) -> int:
        # breakpoint()
        adder_response = cast(DeploymentResponse, self._adder.remote(input))
        # Pass the adder response directly into the multiplier (no `await` needed).
        multiplier_response = cast(DeploymentResponse, self._multiplier.remote(adder_response))
        # `await` the final chained response.
        return await multiplier_response


# pyright: reportFunctionMemberAccess=false
# see https://github.com/ray-project/ray/issues/52483

app = Ingress.bind(
    Adder.bind(increment=1),
    Multiplier.bind(multiple=2),
)

handle: DeploymentHandle = serve.run(app)
response = handle.remote(5)
assert isinstance(response, DeploymentResponse)  # see https://github.com/ray-project/ray/issues/52493
assert response.result() == 12, "(5 + 1) * 2 = 12"
