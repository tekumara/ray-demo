import random
import string
from collections.abc import Generator

import ray
import ray.actor
from pydantic import BaseModel
from ray.util import ActorPool

# each actor runs in its own Python process


class Prediction(BaseModel):
    key: str
    value: str


@ray.remote
class Predictor:
    def __init__(self):
        print("__init__")

    def predict(self, input_keys: list[str]) -> list[Prediction]:
        return [Prediction(key=k, value=random.choice(string.ascii_letters)) for k in input_keys]


@ray.remote
class Consumer:
    def __init__(self, predictors: list[ray.actor.ActorHandle]):
        print("__init__")
        self.predictors = predictors

    def consume(self, input_keys: list[str]) -> list[Prediction]:
        print(f"consume {input_keys}")

        # here we can fetch other data using the input keys

        # randomly select a predictor
        predictor = random.choice(self.predictors)
        print(f"using predictor {predictor}")

        # call the predictor
        ref = predictor.predict.remote(input_keys)
        # this will block until the result is ready
        ref = ray.get(ref)  # type: ignore see https://github.com/ray-project/ray/issues/52772

        return ref


def main() -> None:
    # create actors
    print("creating actors")

    num_predictors = 3
    predictors = [Predictor.remote() for _ in range(num_predictors)]

    num_consumers = 10
    consumers = [Consumer.remote(predictors) for _ in range(num_consumers)]  # type: ignore see https://github.com/ray-project/ray/issues/52771

    pool = ActorPool(consumers)

    input_keys = [[f"input-{i}-{j}" for j in range(10)] for i in range(10)]
    results: Generator[list[Prediction], None, None] = pool.map_unordered(lambda a, v: a.consume.remote(v), input_keys)

    print("wait on results")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
