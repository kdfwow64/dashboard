from django.db import connection

from components.components import (
    DataPanelRowValueObject,
    DataPanel,
    DataPanelValueObject,
    DataPanelItemValueObject,
)
from components.constants import LABEL_BACKGROUND_BLUE
from daep_v2.queries import DAEP_QUERY_DATA


def get_daep_data():
    queries = DAEP_QUERY_DATA
    values = []
    for query in queries:
        val = []
        for item in query["items"]:
            with connection.cursor() as cursor:
                cursor.execute(item["query"])
                results = cursor.fetchall()
            color = item.get("color", LABEL_BACKGROUND_BLUE)
            val.append(
                DataPanelItemValueObject(
                    label=item["label"],
                    value=results[0][0],
                    color=color,
                    is_percentage_field=item["is_percentage_field"],
                )
            )
        values.append(DataPanelRowValueObject(label=query["title"], values=val))

    data_panel = DataPanel(
        grid_css_classes="span-12",
        value=DataPanelValueObject(title="DAEP Home Page v2", values=values),
    )
    return data_panel
