from decimal import Decimal
from django.db import connection

from components.components import Gauge, GaugeValue
from components.components.dropdown import (
    DropdownValueObject,
    DropdownOptionValueObject,
)
from components.serializers.datatable import BaseTableSerializer
from risk_scorecard_v3.queries import (
    QUERY_SCORE_CARD,
    QUERY_SCORE_CARD_AVG,
    QUERY_SCORES_BY_VP,
    QUERY_BAPP_INFORMATION,
    QUERY_CONTROL_FINDINGS,
    QUERY_OPEN_VULNERABILITIES,
    QUERY_WAVE_IDS,
    QUERY_TOWER_NAMES,
)


SCORE_CARD_LABELS = [
    "Server Patching",
    "Java Patching",
    "AV Coverage",
    "Overdue Critical CF",
    "Overdue High CF",
    "HIPS Compliance",
    "FIM Compliance",
    "Monthly VM Scanning",
    "Daily VM Scanning",
    "SAST Compliance",
    "DR Compliance",
    "PENTest Compliance",
    "Logging to SIEM",
]
SCORES_BY_VP_COLUMNS = [
    "VP Owner Name",
    "BAPP Count",
    "Composite Score",
    "Server Patching",
    "Java Patching",
    "AV Coverage",
    "Overdue Critical CF",
    "Overdue High CF",
    "HIPS Compliance",
    "FIM Compliance",
    "Monthly VM Scanning",
    "Daily VM Scanning",
    "SAST Compliance",
    "DR Compliance",
    "PENTest Compliance",
    "Logging to SIEM",
]
BAPP_INFORMATION_COLUMNS = [
    "BAPP ID",
    "BAPP Name",
    "Product Owner",
    "AV/AM Compliant",
    "Server Patching",
    "Java Patching",
    "No Critical Control Violations Overdue",
    "No High Control Violations Overdue",
    "CV Age Score",
    "VM Age Score",
    "High Impact",
    "BAPP Score",
]
CONTROL_FINDINGS_COLUMNS = [
    "BAPP ID",
    "BAPP Name",
    "Archer Finding",
    "Finding Source",
    "Mandated Remediation Date",
    "First Published",
    "Disney Severity",
    "Effort",
    "Description",
    "Risk Score",
    "Tracking ID",
    "Exception Status",
]
OPEN_VULNERABILITIES_COLUMNS = [
    "BAPP ID",
    "BAPP Name",
    "Hostname",
    "IP Address",
    "Disney Severity",
    "Last Detected",
    "Vulnerability Title",
    "Age",
    "High Impact",
    "Vuln ID",
    "Host ID",
    "Risk Score",
    "Scanner",
    "Description",
    "Solution",
    "Output",
    "Port",
]


def get_business_supported_data(filter_options):
    query = f"{QUERY_SCORE_CARD} {filter_options}"
    avg_query = f"{QUERY_SCORE_CARD_AVG} {filter_options}"

    with connection.cursor() as cursor:
        cursor.execute(avg_query)
        results = cursor.fetchall()

    if results[0][0] is None:
        avg = 0
    else:
        avg = float(round(results[0][0], 2))

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    data = []
    if results[0][0] is not None:
        for index, label in enumerate(SCORE_CARD_LABELS):

            if results[0][index] is None:
                value = GaugeValue.none_value
            else:
                value = float(round(results[0][index], 2))
            data.append({"label": label, "value": value})

    gauge_data = Gauge(
        grid_css_classes="span-12",
        css_classes="card gauge-css-classes",
        value=GaugeValue(
            value=avg,
            title="Composite Score",
            main_chart={"value": avg, "label": ""},
            sub_charts=data,
        ),
    )
    return gauge_data


class BaseScoresByVPSerializer(BaseTableSerializer):
    percentage_column_ids = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    href_replace_column_ids = [0]
    href = "https://saf-console.wdprapps.disney.com/d/9iM1STBVk/vp-owner-view-v3?orgId=1&var-vp_owner={replace}&var-wave=All"
    filter_options = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        columns = {k: k for k in SCORES_BY_VP_COLUMNS}

    def get_data(self, *args, **kwargs):
        query = QUERY_SCORES_BY_VP.format(self.filter_options)

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        data = []
        for res in results:
            data.append(
                {
                    label: float(res[index])
                    if type(res[index]) == Decimal
                    else res[index]
                    for index, label in enumerate(SCORES_BY_VP_COLUMNS)
                }
            )

        return data


class BaseBAPPInformationSerializer(BaseTableSerializer):
    filter_options = ""

    class Meta:
        columns = {k: k for k in BAPP_INFORMATION_COLUMNS}

    def get_data(self, *args, **kwargs):
        query = f"{QUERY_BAPP_INFORMATION} {self.filter_options}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        data = []
        for res in results:
            data.append(
                {
                    label: float(res[index])
                    if type(res[index]) == Decimal
                    else res[index]
                    for index, label in enumerate(BAPP_INFORMATION_COLUMNS)
                }
            )

        return data


class BaseControlFindingsSerializer(BaseTableSerializer):
    percentage_column_ids = [9]
    href_replace_column_ids = [10]
    href = "https://archer.wdpr.disney.com/default.aspx?requestUrl=..%2fGenericContent%2fRecord.aspx%3fid%3d{replace}%26moduleId%3d167"
    filter_options = ""

    class Meta:
        columns = {k: k for k in CONTROL_FINDINGS_COLUMNS}

    def get_data(self, *args, **kwargs):
        query = QUERY_CONTROL_FINDINGS.format(self.filter_options)
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        data = []
        for res in results:
            data.append(
                {
                    label: float(res[index])
                    if type(res[index]) == Decimal
                    else res[index]
                    for index, label in enumerate(CONTROL_FINDINGS_COLUMNS)
                }
            )

        return data


class BaseOpenVulnerabilitiesSerializer(BaseTableSerializer):
    percentage_column_ids = [11]
    href_replace_column_ids = [9]
    href = "https://saf-console.wdprapps.disney.com/d/UYrSFtv4z/vulnerability-details?orgId=1&var-vuln_id={replace}"
    filter_options = ""

    class Meta:
        columns = {k: k for k in OPEN_VULNERABILITIES_COLUMNS}

    def get_data(self, *args, **kwargs):
        query = QUERY_OPEN_VULNERABILITIES.format(self.filter_options)

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        data = []
        for res in results:
            data.append(
                {
                    label: float(res[index])
                    if type(res[index]) == Decimal
                    else res[index]
                    for index, label in enumerate(OPEN_VULNERABILITIES_COLUMNS)
                }
            )

        return data


def get_wave_data(wave_ids: list):
    query = QUERY_WAVE_IDS

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    data = []
    for res in results:
        data.append(DropdownOptionValueObject(label=res[0], value=res[0]))

    value = DropdownValueObject(
        multiple=True,
        var_name="var-wave",
        dropdown_id="wave_id",
        title="Wave",
        values=data,
        selected_value=wave_ids,
    )
    return value


def get_financial_data(financial_str):
    data = []
    data.append(DropdownOptionValueObject(label="All", value="All"))
    data.append(DropdownOptionValueObject(label="true", value="true"))
    data.append(DropdownOptionValueObject(label="false", value="false"))

    value = DropdownValueObject(
        multiple=False,
        var_name="var-financial",
        dropdown_id="financial",
        title="CTO Rep",
        values=data,
        selected_value=financial_str,
    )
    return value


def get_tower_name_dropdown(tower_name: str):
    with connection.cursor() as cursor:
        cursor.execute(QUERY_TOWER_NAMES)
        results = cursor.fetchall()

    data = []
    for res in results:
        data.append(DropdownOptionValueObject(label=res[0], value=res[0]))

    value = DropdownValueObject(
        var_name="var-tower",
        dropdown_id="tower_name",
        title="Tower Name",
        values=data,
        selected_value=tower_name,
    )

    return value
