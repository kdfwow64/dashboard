from django.apps import AppConfig


class RiskScorecardV3Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'risk_scorecard_v3'

    def ready(self):
        import risk_scorecard_v3.dashboards
