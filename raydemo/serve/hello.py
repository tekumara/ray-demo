# File name: hello.py
from ray import serve
from ray.serve.handle import DeploymentHandle
from starlette.requests import Request


@serve.deployment(
    ray_actor_options={
        "runtime_env": {"env_vars": {"RAY_DEBUG": "1"}},
    },
)
class LanguageClassifier:
    def __init__(self, spanish_responder: DeploymentHandle, french_responder: DeploymentHandle):
        self.spanish_responder = spanish_responder
        self.french_responder = french_responder

    async def __call__(self, http_request: Request) -> str:
        request = await http_request.json()
        # breakpoint()
        language, name = request["language"], request["name"]

        if language == "spanish":
            response = self.spanish_responder.say_hello.remote(name)
        elif language == "french":
            response = self.french_responder.say_hello.remote(name)
        else:
            return "Please try again."

        return await response  # type: ignore https://github.com/ray-project/ray/issues/52491


@serve.deployment
class SpanishResponder:
    def say_hello(self, name: str) -> str:
        return f"Hola {name}"


@serve.deployment
class FrenchResponder:
    def say_hello(self, name: str) -> str:
        return f"Bonjour {name}"


# pyright: reportFunctionMemberAccess=false
# see https://github.com/ray-project/ray/issues/52483

spanish_responder = SpanishResponder.bind()
french_responder = FrenchResponder.bind()
language_classifier = LanguageClassifier.bind(spanish_responder, french_responder)
