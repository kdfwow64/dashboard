from decimal import Decimal
from django.db import connection

from components.components import Gauge, GaugeValue, DataPanel, DataPanelValueObject, DataPanelItemValueObject, \
    DataPanelRowValueObject
from components.components.dropdown import Dropdown, DropdownValueObject, DropdownOptionValueObject
from components.constants import LABEL_BACKGROUND_BROWN, LABEL_BACKGROUND_RED, LABEL_BACKGROUND_BLUE
from components.serializers.datatable import BaseTableSerializer


def get_business_supported_data(filter_options):
    query = f"select avg(patch_compliant),avg(patch_compliant_java),avg(av_am_compliant),avg(no_critical_cvs_overdue),avg(no_high_cvs_overdue),avg(hips_compliant),avg(fim_compliant),avg(vm_monthly_scan_compliant),avg(vm_weekly_scan_compliant),avg(sast_compliant),avg(dr_compliant),avg(pentest_compliant),avg(siem_compliant) from scorecard_data_by_bapp {filter_options}"
    avg_query = f"SELECT avg(bapp_score) FROM scorecard_data_by_bapp {filter_options}"

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

    labels = ["Server Patching", "Java Patching", "AV Coverage", "Overdue Critical CF", "Overdue High CF",
              "HIPS Compliance", "FIM Compliance", "Monthly VM Scanning", "Daily VM Scanning", "SAST Compliance",
              "DR Compliance", "PENTest Compliance", "Logging to SIEM"]
    data = []
    if results[0][0] is not None:
        for index, label in enumerate(labels):
            if results[0][index] is None:
                continue
            data.append({"label": label, "value": float(round(results[0][index], 2))})

    gauge_data = Gauge(
        grid_css_classes="span-12",
        css_classes="card gauge-css-classes",
        value=GaugeValue(value=avg, title="Composite Score", main_chart={"value": avg, "label": ""}, sub_charts=data)
    )
    return gauge_data


def get_daep_data():
    queries = [
        {
            "title": "Total",
            "items": [
                {
                    "label": "Devices Identified",
                    "query": "select count(*) from dae_axonius_dashboard_data",
                    "is_percentage_field": False,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where vm_eligible",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where av_am_eligible",
                    "is_percentage_field": True,
                },
                {
                    "label": "High Impact Devices",
                    "query": "select count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL)",
                    "is_percentage_field": False,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and vm_eligible",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and av_am_eligible",
                    "is_percentage_field": True,
                }
            ]
        },
        {
            "title": "Studios",
            "items": [
                {
                    "label": "Devices Identified",
                    "query": "select count(*) from dae_axonius_dashboard_data where segment = 'Studio Entertainment'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_BROWN,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where vm_eligible and segment = 'Studio Entertainment'",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where av_am_eligible and segment = 'Studio Entertainment'",
                    "is_percentage_field": True,
                },
                {
                    "label": "High Impact Devices",
                    "query": "select count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and segment = 'Studio Entertainment'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_BROWN,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and vm_eligible and segment = 'Studio Entertainment'",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select case when count(*) > 0 then (count(av_am_coverage) * 100)/ count(*) else 100 end from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and av_am_eligible and segment = 'Studio Entertainment'",
                    "is_percentage_field": True,
                }
            ]
        },
        {
            "title": "DMED",
            "items": [
                {
                    "label": "Devices Identified",
                    "query": "select count(*) from dae_axonius_dashboard_data where segment = 'DMED'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_BROWN,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where vm_eligible and segment = 'DMED'",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where av_am_eligible and segment = 'DMED'",
                    "is_percentage_field": True,
                },
                {
                    "label": "High Impact Devices",
                    "query": "select count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and segment = 'DMED'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_BROWN,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and vm_eligible and segment = 'DMED'",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and av_am_eligible and segment = 'DMED'",
                    "is_percentage_field": True,
                }
            ]
        },
        {
            "title": "Corporate",
            "items": [
                {
                    "label": "Devices Identified",
                    "query": "select count(*) from dae_axonius_dashboard_data where segment = 'Corporate'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_BROWN,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where vm_eligible and segment = 'Corporate' and (amdb_status = 'ACTIVE' or amdb_status is NULL)",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where av_am_eligible and segment = 'Corporate' and (amdb_status = 'ACTIVE' or amdb_status is NULL)",
                    "is_percentage_field": True,
                },
                {
                    "label": "High Impact Devices",
                    "query": "select count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and segment = 'Corporate'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_BROWN,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and vm_eligible and segment = 'Corporate' and (amdb_status = 'ACTIVE' or amdb_status is NULL)",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and segment = 'Corporate' and (amdb_status = 'ACTIVE' or amdb_status is NULL)",
                    "is_percentage_field": True,
                }
            ]
        },
        {
            "title": "DPEP",
            "items": [
                {
                    "label": "Devices Identified",
                    "query": "select count(*) from dae_axonius_dashboard_data where segment = 'DPEP'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_BROWN,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where vm_eligible and segment = 'DPEP'  ",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where av_am_eligible and segment = 'DPEP'",
                    "is_percentage_field": True,
                },
                {
                    "label": "High Impact Devices",
                    "query": "select count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and segment = 'DPEP'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_BROWN,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and vm_eligible and segment = 'DPEP'",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and av_am_eligible and segment = 'DPEP'",
                    "is_percentage_field": True,
                }
            ]
        },
        {
            "title": "Unknown Segment",
            "items": [
                {
                    "label": "Devices Identified",
                    "query": "select count(*) from dae_axonius_dashboard_data where segment = 'Unknown'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_RED,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where vm_eligible and segment =  'Unknown'",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where av_am_eligible and segment = 'Unknown'",
                    "is_percentage_field": True,
                },
                {
                    "label": "High Impact Devices",
                    "query": "select count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and segment = 'Unknown'",
                    "is_percentage_field": False,
                    "color": LABEL_BACKGROUND_RED,
                },
                {
                    "label": "VM Scan Coverage",
                    "query": "select (count(vm_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and vm_eligible and segment = 'Unknown'",
                    "is_percentage_field": True,
                },
                {
                    "label": "AV/AM Coverage",
                    "query": "select (count(av_am_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and av_am_eligible and segment = 'Unknown'",
                    "is_percentage_field": True,
                }
            ]
        }
    ]

    values = []
    for query in queries:
        val = []
        for item in query["items"]:
            with connection.cursor() as cursor:
                cursor.execute(item["query"])
                results = cursor.fetchall()
            color = item.get("color", LABEL_BACKGROUND_BLUE)
            val.append(
                DataPanelItemValueObject(
                    label=item["label"],
                    value=results[0][0],
                    color=color,
                    is_percentage_field=item["is_percentage_field"],
                )
            )
        values.append(DataPanelRowValueObject(label=query["title"], values=val))

    data_panel = DataPanel(
        grid_css_classes="span-12",
        value=DataPanelValueObject(
            title="DAEP Home Page v2",
            values=values
        )
    )
    return data_panel


scores_by_cp_columns = ["VP Owner Name", "BAPP Count", "Composite Score", "Server Patching", "Java Patching",
                        "AV Coverage", "Overdue Critical CF", "Overdue High CF", "HIPS Compliance", "FIM Compliance",
                        "Monthly VM Scanning", "Daily VM Scanning", "SAST Compliance", "DR Compliance",
                        "PENTest Compliance", "Logging to SIEM"]


class BaseScoresByVPSerializer(BaseTableSerializer):
    percentage_column_ids = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    href_replace_column_ids = [0]
    href = "https://saf-console.wdprapps.disney.com/d/9iM1STBVk/vp-owner-view-v3?orgId=1&var-vp_owner={replace}&var-wave=All"
    filter_options = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        columns = {k: k for k in scores_by_cp_columns}

    def get_data(self, *args, **kwargs):
        query = f"select vp_owner_name, count(bapp_id), avg(bapp_score), avg(patch_compliant), avg(patch_compliant_java), avg(av_am_compliant), avg(no_critical_cvs_overdue), avg(no_high_cvs_overdue), avg(hips_compliant), avg(fim_compliant), avg(vm_monthly_scan_compliant), avg(vm_weekly_scan_compliant), avg(sast_compliant), avg(dr_compliant), avg(pentest_compliant), avg(siem_compliant) from scorecard_data_by_bapp {self.filter_options} group by vp_owner_name"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        data = []
        for res in results:
            data.append({
                label: float(res[index]) if type(res[index]) == Decimal else res[index] for index, label in enumerate(scores_by_cp_columns)
            })

        return data


bapp_information_columns = ["BAPP ID", "BAPP Name", "Product Owner", "AV/AM Compliant", "Server Patching",
                            "Java Patching", "No Critical Control Violations Overdue",
                            "No High Control Violations Overdue", "CV Age Score", "VM Age Score",
                            "High Impact", "BAPP Score"]


class BaseBAPPInformationSerializer(BaseTableSerializer):
    filter_options = ""

    class Meta:
        columns = {k: k for k in bapp_information_columns}

    def get_data(self, *args, **kwargs):
        query = f"SELECT bapp_id, bapp_name , scorecard_data_by_bapp.bapp_owner_name, av_am_compliant , patch_compliant, patch_compliant_java, no_critical_cvs_overdue, no_high_cvs_overdue ,cv_age_score_average, vm_age_score_average ,high_impact ,bapp_score FROM scorecard_data_by_bapp {self.filter_options}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        data = []
        for res in results:
            data.append({
                label: float(res[index]) if type(res[index]) == Decimal else res[index] for index, label in enumerate(bapp_information_columns)
            })

        return data


control_findings_columns = ["BAPP ID", "BAPP Name", "Archer Finding", "Finding Source", "Mandated Remediation Date", "First Published", "Disney Severity", "Effort", "Description", "Risk Score", "Tracking ID", "Exception Status"]


class BaseControlFindingsSerializer(BaseTableSerializer):
    percentage_column_ids = [9]
    href_replace_column_ids = [10]
    href = "https://archer.wdpr.disney.com/default.aspx?requestUrl=..%2fGenericContent%2fRecord.aspx%3fid%3d{replace}%26moduleId%3d167"
    filter_options = ""

    class Meta:
        columns = {k: k for k in control_findings_columns}

    def get_data(self, *args, **kwargs):
        query = f"select bapp_id, bapp_name, finding_id, finding_source, mandated_remediation_date, first_published, disney_severity_rating, effort, finding_short_description, archer_finding_risk_scores.risk_score, archer_findings_exported.tracking_id, archer_findings_exported.exception_status from scorecard_data_by_bapp left join archer_findings_exported on scorecard_data_by_bapp.bapp_id = ANY(string_to_array(archer_findings_exported.bapp_ids, ';')) left join archer_finding_risk_scores on archer_finding_risk_scores.tracking_id = archer_findings_exported.tracking_id {self.filter_options} and finding_id is not null and finding_source not in ('AWS Inspector', 'Tenable IO', 'Qualys')"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        data = []
        for res in results:
            data.append({
                label: float(res[index]) if type(res[index]) == Decimal else res[index] for index, label in enumerate(control_findings_columns)
            })

        return data


open_vulnerabilities_columns = ["BAPP ID", "BAPP Name", "Hostname", "IP Address", "Disney Severity", "Last Detected",
                                "Vulnerability Title", "Age", "High Impact", "Vuln ID", "Host ID", "Risk Score",
                                "Scanner", "Description", "Solution", "Output", "Port"]


class BaseOpenVulnerabilitiesSerializer(BaseTableSerializer):
    percentage_column_ids = [11]
    href_replace_column_ids = [9]
    href = "https://saf-console.wdprapps.disney.com/d/UYrSFtv4z/vulnerability-details?orgId=1&var-vuln_id={replace}"
    filter_options = ""

    class Meta:
        columns = {k: k for k in open_vulnerabilities_columns}

    def get_data(self, *args, **kwargs):
        query = f"select q.bapp_id, bapp_name, hostname_preferred, ips_v4_preferred, CASE WHEN disney_severity = 5 THEN 'Disney-Critical' WHEN disney_severity = 4 THEN 'Disney-High' WHEN disney_severity = 3 THEN 'Disney-Moderate' WHEN disney_severity = 2 THEN 'Disney-Low' WHEN disney_severity = 1 THEN 'Disney-Info' ELSE 'Not Rated' END , last_detected::date, title, vi_age, q.high_impact, vuln_identifier, internal_axon_id, (age_score * .25) + (high_impact_score * .25) + (severity_score * .50), vuln_source, description, solution, output, port from (select hostname_preferred, ips_v4_preferred, disney_severity, CASE WHEN disney_severity = 5 THEN 100 WHEN disney_severity = 4 THEN 80 WHEN disney_severity = 3 THEN 60 WHEN disney_severity = 2 THEN 40 WHEN disney_severity = 1 THEN 20 ELSE 0 END AS severity_score, last_detected::date, title, vi_age, LEAST(100.0 * (vi_age)::numeric / (3 * 365)::numeric, 100.0) AS age_score, high_impact, CASE WHEN high_impact is null THEN 0 WHEN high_impact THEN 100 ELSE 50 END AS high_impact_score, unnest(string_to_array(CASE WHEN dae_axonius_per_vuln_dashboard_data.bapp_ids IS NULL AND dae_axonius_per_vuln_dashboard_data.segment = 'DPEP'::text THEN 'BAPPDPEPUNK'::text ELSE dae_axonius_per_vuln_dashboard_data.bapp_ids END, ','::text)) as bapp_id, type_preferred, vuln_source, vuln_identifier, internal_axon_id, description, output, solution, port from dae_axonius_per_vuln_dashboard_data where disney_severity >= (SELECT setting_value FROM settings where setting_key = 'patching_min_sev')::INT) as q left join scorecard_data_by_bapp on q.bapp_id = scorecard_data_by_bapp.bapp_id where q.bapp_id in (select bapp_id FROM scorecard_data_by_bapp {self.filter_options})"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        data = []
        for res in results:
            data.append({
                label: float(res[index]) if type(res[index]) == Decimal else res[index] for index, label in enumerate(open_vulnerabilities_columns)
            })

        return data


def get_wave_data(wave_ids: list):
    query = "select distinct(wave_id) from scorecard_data_by_bapp order by wave_id desc"

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    data = []
    for res in results:
        data.append(DropdownOptionValueObject(
            label=res[0],
            value=res[0]
        ))

    dropdown = Dropdown(
        value=DropdownValueObject(
            multiple=True,
            var_name="var-wave",
            dropdown_id="wave_id",
            title="Wave",
            values=data,
            selected_value=wave_ids,
        )
    )
    return dropdown


def get_tower_name_dropdown(tower_name: str):
    query = "select tower_name from towers_v2"

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    data = []
    for res in results:
        data.append(DropdownOptionValueObject(
            label=res[0],
            value=res[0]
        ))

    dropdown = Dropdown(
        value=DropdownValueObject(
            var_name="var-tower",
            dropdown_id="tower_name",
            title="Tower Name",
            values=data,
            selected_value=tower_name,
        )
    )
    return dropdown
