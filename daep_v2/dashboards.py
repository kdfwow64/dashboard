from dashboards.dashboard import Dashboard
from dashboards.registry import registry

from daep_v2.data import get_daep_data


class HomePageDashboard(Dashboard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.components["daep_data_panel"] = get_daep_data()


registry.register(HomePageDashboard)
