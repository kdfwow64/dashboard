from dataclasses import dataclass

from dashboards.component import Table as BaseTable


@dataclass
class DataTable(BaseTable):
    filter_options: str = None
    page_size: int = 10
    template_name: str = "datatable.html"
