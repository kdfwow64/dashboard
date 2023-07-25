from django.urls import path

from daep_v2.views import HomePageDashboardView

urlpatterns = [
    path(
        "homepage_dashboard/",
        HomePageDashboardView.as_view(),
        name="homepage_dashboard"
    ),
]
