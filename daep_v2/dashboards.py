from dashboards.component.layout import ComponentLayout, Card, Div
from dashboards.dashboard import Dashboard
from dashboards.registry import registry

from risk_scorecard_v3.dashboards import get_filter_options
from risk_scorecard_v3.data import get_daep_data


class HomePageDashboard(Dashboard):
    def __init__(self, tower_name: str, wave_ids: list = None, financial_str: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filter_options = get_filter_options(tower_name, wave_ids, financial_str)

        self.components["daep_data_panel"] = get_daep_data(filter_options)


registry.register(HomePageDashboard)
