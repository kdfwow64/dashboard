from dataclasses import dataclass
from typing import Optional, Union

from dashboards.component import Component


@dataclass
class DropdownOptionValueObject:
    label: str
    value: Union[str, int]

    def to_dict(self):
        return {
            "label": self.label,
            "value": self.value,
        }


@dataclass
class DropdownValueObject:
    title: str
    dropdown_id: str
    var_name: str
    selected_value: Union[str, int, list] = None
    values: list = list[DropdownOptionValueObject]
    values_formatted: list = list
    multiple: bool = False

    def __post_init__(self):
        values = []
        for value in self.values:
            values.append(value.to_dict())

        self.values_formatted = values


@dataclass
class Dropdown(Component):
    title: str = ""
    value: Optional[DropdownValueObject] = None
    template_name: str = "dropdown/index.html"
