from components.components.dashboard import BaseDashboardView
from daep_v2.dashboards import HomePageDashboard


class HomePageDashboardView(BaseDashboardView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wave_ids = self.request.GET.getlist("var-wave")
        context["dashboard"] = HomePageDashboard(tower_name=self.request.GET.get("var-tower"), wave_ids=wave_ids,
                                                  financial_str=self.request.GET.get("var-financial"))
        return context
