from dataclasses import dataclass, field

from dashboards.component import Gauge as BaseGauge
from dashboards.component.gauge.gauge import GaugeValue as BaseGaugeValue


class Step:
    value: float
    color: str

    def __init__(self, value: float, color: str):
        self.value = value
        self.color = color

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "color": self.color
        }


DEFAULT_STEPS_FOR_GAUGE = [
    Step(value=70, color="rgb(196, 22, 42)"),   # red
    Step(value=85, color="rgb(224, 180, 0)"),   # yellow
    Step(value=100, color="rgb(55, 135, 45)")   # green
]


@dataclass
class GaugeValue(BaseGaugeValue):
    max: float = 100
    steps: list = field(default_factory=lambda: DEFAULT_STEPS_FOR_GAUGE)
    steps_list: list = list
    value_color: str = ""
    symbol: str = "%"
    sub_charts: list = field(default_factory=list)
    main_chart: dict = field(default_factory=dict)
    title: str = ""

    def __post_init__(self):
        steps_list = [step.to_dict() for step in self.steps]
        self.steps_list = steps_list

        for step in self.steps:
            if self.value <= step.value:
                self.value_color = step.color
                break


@dataclass
class Gauge(BaseGauge):
    template_name: str = "gauge/index.html"
