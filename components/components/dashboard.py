from django.views.generic import TemplateView


class BaseDashboardView(TemplateView):
    template_name = "dashboard/index.html"
