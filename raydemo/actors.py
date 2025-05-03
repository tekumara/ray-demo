import random
import string
from collections.abc import Generator

import ray
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


def main() -> None:
    # create actors
    print("main")
    predictors = [Predictor.remote() for _ in range(10)]
    pool = ActorPool(predictors)
    print("created actors")

    input_keys = [[f"input-{i}-{j}" for j in range(10)] for i in range(10)]
    results: Generator[list[Prediction], None, None] = pool.map_unordered(lambda a, v: a.predict.remote(v), input_keys)

    print("wait on results")
    for r in results:
        print(r)


def run_sequence() -> None:
    p = Predictor.remote()
    input_keys = [[f"input-{i}-{j}" for j in range(10)] for i in range(10)]
    for k in input_keys:
        print(k)
        r = ray.get(p.predict.remote(k))  # type: ignore
        print(r)


if __name__ == "__main__":
    main()
