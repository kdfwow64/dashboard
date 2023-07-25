from django.urls import path

from risk_scorecard_v3.views import TowerHomeDashboardView

urlpatterns = [
    path(
        "tower_home_dashboard",
        TowerHomeDashboardView.as_view(),
        name="tower_home_dashboard"
    ),
]
