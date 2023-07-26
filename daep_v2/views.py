from components.components.dashboard import BaseDashboardView
from daep_v2.dashboards import HomePageDashboard


class HomePageDashboardView(BaseDashboardView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = HomePageDashboard()
        return context
