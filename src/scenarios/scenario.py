from dataclasses import dataclass


class ScenarioBuilder:
    def build(self, name: str, sys_name: str):
        raise NotImplementedError()

    def save(self, path: str):
        raise NotImplementedError()


@dataclass
class Scenario:
    name: str
    builder: ScenarioBuilder

