from dataclasses import dataclass
from typing import Optional

from dashboards.component import Component

from components.components.dropdown import DropdownValueObject


@dataclass
class DropdownMenu(Component):
    title: str = ""
    value: Optional[list[DropdownValueObject]] = None
    template_name: str = "dropdown_menu/index.html"
