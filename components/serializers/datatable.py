from dataclasses import dataclass
from functools import reduce
from datetime import datetime
from typing import Dict, Any

from dashboards.component.table import TableSerializer, SerializedTable as BaseSerializedTable
from dashboards.log import logger
from django.contrib.humanize.templatetags.humanize import naturaltime

from components.constants import DEFAULT_STEPS_FOR_DATATABLE


@dataclass
class SerializedTable(BaseSerializedTable):
    settings: Dict[str, Any] = None


class BaseTableSerializer(TableSerializer):
    steps = DEFAULT_STEPS_FOR_DATATABLE
    percentage_column_ids = []
    href_replace_column_ids = []
    href = ""

    class Meta:
        columns = {}

    @classmethod
    def set_filter_options(cls, filter_options: str):
        serializer = cls()
        serializer.filter_options = filter_options
        return serializer

    @classmethod
    def serialize(cls, **serialize_kwargs) -> SerializedTable:
        self = cls()
        filters = serialize_kwargs.get("filters", {})
        data = self.get_data(**serialize_kwargs)

        # how many results do we have before table filtering and paginating
        initial_count = self.count(data)

        start = 0
        draw = 1
        length = initial_count

        if filters:
            start = int(filters.get("start", start))
            length = int(filters.get("length", length))
            if length < 1:
                length = initial_count
            draw = int(filters.get("draw", draw))

        # apply filtering, sorting and pagination (datatables)
        data = self.filter(data, filters)
        data = self.sort(data, filters)
        processed_data = []
        filtered_count = 0

        # do we still have data after filtering, if so paginate and format
        if self.count(data) > 0:
            page_obj, filtered_count = self.apply_paginator(data, start, length)

            for obj in page_obj.object_list:
                values = {}
                fields = list(self._meta.columns.keys())
                for field in fields:
                    if not isinstance(obj, dict):
                        # reduce is used to allow relations to be traversed.
                        try:
                            value = reduce(getattr, field.split("__"), obj)
                        except AttributeError:
                            logger.warn(f"{field} is not a attribute for this object.")
                            value = None
                    else:
                        value = obj.get(field)

                    if value and isinstance(value, datetime):
                        value = naturaltime(value)

                    elif isinstance(value, bool):
                        value = "Yes" if value else "No"

                    elif value is None:
                        value = "-"

                    if (
                            field == fields[0]
                            and self._meta.first_as_absolute_url
                            and hasattr(obj, "get_absolute_url")
                    ):
                        value = f'<a href="{obj.get_absolute_url()}">{value}</a>'

                    if hasattr(self, f"get_{field}_value"):
                        value = getattr(self, f"get_{field}_value")(obj)

                    values[field] = value

                processed_data.append(values)

        order = [0, "asc"]
        if hasattr(self._meta, "order"):
            order = [
                [
                    list(self._meta.columns.keys()).index(v.replace("-", "")),
                    "desc" if "-" in v else "asc",
                ]
                for v in self._meta.order
            ]

        return SerializedTable(
            data=processed_data,
            settings={
                "steps": self.steps,
                "percentage_column_ids": self.percentage_column_ids,
                "href_replace_column_ids": self.href_replace_column_ids,
                "href": self.href,
            },
            columns=self._meta.columns,
            columns_datatables=[
                {"data": d, "title": t} for d, t in self._meta.columns.items()
            ],
            order=order,
            draw=draw,
            total=initial_count,
            filtered=filtered_count,
        )
