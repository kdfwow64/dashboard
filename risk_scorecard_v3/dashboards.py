from dashboards.component import Text
from dashboards.dashboard import Dashboard
from dashboards.registry import registry

from components.components import DataTable
from risk_scorecard_v3.data import get_business_supported_data, \
    get_wave_data, get_tower_name_dropdown, BaseScoresByVPSerializer, BaseOpenVulnerabilitiesSerializer, \
    BaseControlFindingsSerializer, BaseBAPPInformationSerializer


def get_filter_options(tower_name: str, wave_ids: list = None, financial_str: str = None):
    filter_options = f" where tower_name = '{tower_name}'"

    if wave_ids is not None:
        result = ','.join(f"'{num.strip()}'" for num in wave_ids)
        filter_options += f" and wave_id in ({result})"

    if financial_str is not None:
        result = ','.join(f"'{num.strip()}'" for num in financial_str.split(','))
        filter_options += f" and is_financial in ({result})"

    return filter_options


class TowerHomeDashboard(Dashboard):
    def __init__(self, tower_name: str, wave_ids: list = None, financial_str: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        filter_options = get_filter_options(tower_name, wave_ids, financial_str)

        self.components["tower_name_dropdown"] = get_tower_name_dropdown(tower_name)
        self.components["wave_id_dropdown"] = get_wave_data(wave_ids)
        self.components["gauge"] = get_business_supported_data(filter_options)

        self.components["scores_by_vp_table_title"] = Text(
            value="Scores by VP",
            grid_css_classes="span-12",
            css_classes="card-title")

        class_attributes = {
            'filter_options': filter_options,
        }

        # ScoresByVPSerializer = type('ScoresByVPSerializer', (BaseScoresByVPSerializer,), class_attributes)
        ScoresByVPSerializer = BaseScoresByVPSerializer.set_filter_options(filter_options)

        self.components["scores_by_vp_table"] = DataTable(
            value=ScoresByVPSerializer,
            grid_css_classes="span-12")

        self.components["bapp_information_table_title"] = Text(
            value="BAPP Information",
            grid_css_classes="span-12",
            css_classes="card-title")

        BAPPInformationSerializer = type('BAPPInformationSerializer', (BaseBAPPInformationSerializer,), class_attributes)
        # BAPPInformationSerializer = BaseBAPPInformationSerializer.set_filter_options(filter_options)
        self.components["bapp_information_table"] = DataTable(
            value=BAPPInformationSerializer,
            grid_css_classes="span-12")

        self.components["control_findings_table_title"] = Text(
            value="Control Findings",
            grid_css_classes="span-12",
            css_classes="card-title")

        ControlFindingsSerializer = type('ControlFindingsSerializer', (BaseControlFindingsSerializer,), class_attributes)
        # ControlFindingsSerializer = BaseControlFindingsSerializer.set_filter_options(filter_options)
        self.components["control_findings_table"] = DataTable(
            value=ControlFindingsSerializer,
            grid_css_classes="span-12")

        self.components["open_vuln_table_title"] = Text(
            value="Open Vulnerabilities",
            grid_css_classes="span-12",
            css_classes="card-title")

        OpenVulnerabilitiesSerializer = type('OpenVulnerabilitiesSerializer', (BaseOpenVulnerabilitiesSerializer,), class_attributes)
        # OpenVulnerabilitiesSerializer = BaseOpenVulnerabilitiesSerializer.set_filter_options(filter_options)
        self.components["open_vuln_table"] = DataTable(
            value=OpenVulnerabilitiesSerializer,
            grid_css_classes="span-12")


registry.register(TowerHomeDashboard)
