from dataclasses import dataclass
from typing import Optional

from dashboards.component import Component


@dataclass
class DataPanelItemValueObject:
    label: str
    value: float
    color: str = "linear-gradient(120deg, rgb(21, 49, 130), rgb(28, 105, 174))"
    is_percentage_field: bool = False

    def to_dict(self):
        color = self.color
        if self.is_percentage_field:
            if self.value < 60:
                color = "linear-gradient(120deg, rgb(127, 16, 14), rgb(173, 19, 58))"
            elif self.value < 80:
                color = "linear-gradient(120deg, rgb(211, 210, 5), rgb(249, 187, 17))"
            else:
                color = "linear-gradient(120deg, rgb(26, 78, 27), rgb(58, 116, 39))"

        return {
            "label": self.label,
            "value": f"{round(self.value, 1)}%" if self.is_percentage_field else int(self.value),
            "color": color,
            "is_percentage_field": self.is_percentage_field
        }


@dataclass
class DataPanelRowValueObject:
    label: str
    count_in_row: int = 6
    values: list = list[DataPanelItemValueObject]

    def to_dict(self):
        return {
            "label": self.label,
            "count_in_row": self.count_in_row,
            "values": [value.to_dict() for value in self.values],
        }


@dataclass
class DataPanelValueObject:
    title: str
    values: list = list[DataPanelRowValueObject]
    values_formatted: list = list

    def __post_init__(self):
        values = []
        for value in self.values:
            values.append(value.to_dict())

        self.values_formatted = values


@dataclass
class DataPanel(Component):
    title: str = ""
    value: Optional[DataPanelValueObject] = None
    template_name: str = "datapanel/index.html"
