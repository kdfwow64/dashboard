from components.constants import LABEL_BACKGROUND_BROWN, LABEL_BACKGROUND_RED

row_names = ["Total", "Studios", "DMED", "Corporate", "DPEP", "Unknown Segment"]
column_names = [
    "Devices Identified",
    "VM Scan Coverage",
    "AV/AM Coverage",
    "High Impact Devices",
    "VM Scan Coverage",
    "AV/AM Coverage",
]
percentage_fields = [False, True, True, False, True, True]


QUERY_TOTAL_DEVICES_IDENTIFIED = "select count(*) from dae_axonius_dashboard_data"
QUERY_TOTAL_VM_SCAN_COVERAGE = "select (count(vm_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where vm_eligible"
QUERY_TOTAL_AV_AM_COVERAGE = "select (count(av_am_coverage)* 100)::numeric / count(*) from dae_axonius_dashboard_data where av_am_eligible"
QUERY_TOTAL_HIGH_IMPACT_DEVICES = "select count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL)"
QUERY_TOTAL_VM_SCAN_COVERAGE_SECOND = "select (count(vm_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and vm_eligible"
QUERY_TOTAL_AV_AM_COVERAGE_SECOND = "select (count(av_am_coverage) * 100)/ count(*) from dae_axonius_dashboard_data where (u_pci or u_sox or u_gdpr or u_hipaa or u_internet_facing or information_classification = 'Confidential') and (amdb_status = 'ACTIVE' or amdb_status is NULL) and av_am_eligible"

QUERY_STUDIOS_DEVICES_IDENTIFIED = (
    f"{QUERY_TOTAL_DEVICES_IDENTIFIED} where segment = 'Studio Entertainment'"
)
QUERY_STUDIOS_VM_SCAN_COVERAGE = (
    f"{QUERY_TOTAL_VM_SCAN_COVERAGE} and segment = 'Studio Entertainment'"
)
QUERY_STUDIOS_AV_AM_COVERAGE = (
    f"{QUERY_TOTAL_AV_AM_COVERAGE} and segment = 'Studio Entertainment'"
)
QUERY_STUDIOS_HIGH_IMPACT_DEVICES = (
    f"{QUERY_TOTAL_HIGH_IMPACT_DEVICES} and segment = 'Studio Entertainment'"
)
QUERY_STUDIOS_VM_SCAN_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_VM_SCAN_COVERAGE_SECOND} and segment = 'Studio Entertainment'"
)
QUERY_STUDIOS_AV_AM_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_AV_AM_COVERAGE_SECOND} and segment = 'Studio Entertainment'"
)

QUERY_DMED_DEVICES_IDENTIFIED = (
    f"{QUERY_TOTAL_DEVICES_IDENTIFIED} where segment = 'DMED'"
)
QUERY_DMED_VM_SCAN_COVERAGE = f"{QUERY_TOTAL_VM_SCAN_COVERAGE} and segment = 'DMED'"
QUERY_DMED_AV_AM_COVERAGE = f"{QUERY_TOTAL_AV_AM_COVERAGE} and segment = 'DMED'"
QUERY_DMED_HIGH_IMPACT_DEVICES = (
    f"{QUERY_TOTAL_HIGH_IMPACT_DEVICES} and segment = 'DMED'"
)
QUERY_DMED_VM_SCAN_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_VM_SCAN_COVERAGE_SECOND} and segment = 'DMED'"
)
QUERY_DMED_AV_AM_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_AV_AM_COVERAGE_SECOND} and segment = 'DMED'"
)

QUERY_CORPORATE_DEVICES_IDENTIFIED = (
    f"{QUERY_TOTAL_DEVICES_IDENTIFIED} where segment = 'Corporate'"
)
QUERY_CORPORATE_VM_SCAN_COVERAGE = (
    f"{QUERY_TOTAL_VM_SCAN_COVERAGE} and segment = 'Corporate'"
)
QUERY_CORPORATE_AV_AM_COVERAGE = (
    f"{QUERY_TOTAL_AV_AM_COVERAGE} and segment = 'Corporate'"
)
QUERY_CORPORATE_HIGH_IMPACT_DEVICES = (
    f"{QUERY_TOTAL_HIGH_IMPACT_DEVICES} and segment = 'Corporate'"
)
QUERY_CORPORATE_VM_SCAN_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_VM_SCAN_COVERAGE_SECOND} and segment = 'Corporate'"
)
QUERY_CORPORATE_AV_AM_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_AV_AM_COVERAGE_SECOND} and segment = 'Corporate'"
)

QUERY_DPEP_DEVICES_IDENTIFIED = (
    f"{QUERY_TOTAL_DEVICES_IDENTIFIED} where segment = 'DPEP'"
)
QUERY_DPEP_VM_SCAN_COVERAGE = f"{QUERY_TOTAL_VM_SCAN_COVERAGE} and segment = 'DPEP'"
QUERY_DPEP_AV_AM_COVERAGE = f"{QUERY_TOTAL_AV_AM_COVERAGE} and segment = 'DPEP'"
QUERY_DPEP_HIGH_IMPACT_DEVICES = (
    f"{QUERY_TOTAL_HIGH_IMPACT_DEVICES} and segment = 'DPEP'"
)
QUERY_DPEP_VM_SCAN_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_VM_SCAN_COVERAGE_SECOND} and segment = 'DPEP'"
)
QUERY_DPEP_AV_AM_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_AV_AM_COVERAGE_SECOND} and segment = 'DPEP'"
)

QUERY_UNKNOWN_DEVICES_IDENTIFIED = (
    f"{QUERY_TOTAL_DEVICES_IDENTIFIED} where segment = 'Unknown'"
)
QUERY_UNKNOWN_VM_SCAN_COVERAGE = (
    f"{QUERY_TOTAL_VM_SCAN_COVERAGE} and segment = 'Unknown'"
)
QUERY_UNKNOWN_AV_AM_COVERAGE = f"{QUERY_TOTAL_AV_AM_COVERAGE} and segment = 'Unknown'"
QUERY_UNKNOWN_HIGH_IMPACT_DEVICES = (
    f"{QUERY_TOTAL_HIGH_IMPACT_DEVICES} and segment = 'Unknown'"
)
QUERY_UNKNOWN_VM_SCAN_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_VM_SCAN_COVERAGE_SECOND} and segment = 'Unknown'"
)
QUERY_UNKNOWN_AV_AM_COVERAGE_SECOND = (
    f"{QUERY_TOTAL_AV_AM_COVERAGE_SECOND} and segment = 'Unknown'"
)


queries = {
    "Total": [
        QUERY_TOTAL_DEVICES_IDENTIFIED,
        QUERY_TOTAL_VM_SCAN_COVERAGE,
        QUERY_TOTAL_AV_AM_COVERAGE,
        QUERY_TOTAL_HIGH_IMPACT_DEVICES,
        QUERY_TOTAL_VM_SCAN_COVERAGE_SECOND,
        QUERY_TOTAL_AV_AM_COVERAGE_SECOND,
    ],
    "Studios": [
        QUERY_STUDIOS_DEVICES_IDENTIFIED,
        QUERY_STUDIOS_VM_SCAN_COVERAGE,
        QUERY_STUDIOS_AV_AM_COVERAGE,
        QUERY_STUDIOS_HIGH_IMPACT_DEVICES,
        QUERY_STUDIOS_VM_SCAN_COVERAGE_SECOND,
        QUERY_STUDIOS_AV_AM_COVERAGE_SECOND,
    ],
    "DMED": [
        QUERY_DMED_DEVICES_IDENTIFIED,
        QUERY_DMED_VM_SCAN_COVERAGE,
        QUERY_DMED_AV_AM_COVERAGE,
        QUERY_DMED_HIGH_IMPACT_DEVICES,
        QUERY_DMED_VM_SCAN_COVERAGE_SECOND,
        QUERY_DMED_AV_AM_COVERAGE_SECOND,
    ],
    "Corporate": [
        QUERY_CORPORATE_DEVICES_IDENTIFIED,
        QUERY_CORPORATE_VM_SCAN_COVERAGE,
        QUERY_CORPORATE_AV_AM_COVERAGE,
        QUERY_CORPORATE_HIGH_IMPACT_DEVICES,
        QUERY_CORPORATE_VM_SCAN_COVERAGE_SECOND,
        QUERY_CORPORATE_AV_AM_COVERAGE_SECOND,
    ],
    "DPEP": [
        QUERY_DPEP_DEVICES_IDENTIFIED,
        QUERY_DPEP_VM_SCAN_COVERAGE,
        QUERY_DPEP_AV_AM_COVERAGE,
        QUERY_DPEP_HIGH_IMPACT_DEVICES,
        QUERY_DPEP_VM_SCAN_COVERAGE_SECOND,
        QUERY_DPEP_AV_AM_COVERAGE_SECOND,
    ],
    "Unknown Segment": [
        QUERY_UNKNOWN_DEVICES_IDENTIFIED,
        QUERY_UNKNOWN_VM_SCAN_COVERAGE,
        QUERY_UNKNOWN_AV_AM_COVERAGE,
        QUERY_UNKNOWN_HIGH_IMPACT_DEVICES,
        QUERY_UNKNOWN_VM_SCAN_COVERAGE_SECOND,
        QUERY_UNKNOWN_AV_AM_COVERAGE_SECOND,
    ],
}

DAEP_QUERY_DATA = []

colors = {
    1: {
        0: LABEL_BACKGROUND_BROWN,
        3: LABEL_BACKGROUND_BROWN,
    },
    2: {
        0: LABEL_BACKGROUND_BROWN,
        3: LABEL_BACKGROUND_BROWN,
    },
    3: {
        0: LABEL_BACKGROUND_BROWN,
        3: LABEL_BACKGROUND_BROWN,
    },
    4: {
        0: LABEL_BACKGROUND_BROWN,
        3: LABEL_BACKGROUND_BROWN,
    },
    5: {
        0: LABEL_BACKGROUND_RED,
        3: LABEL_BACKGROUND_RED,
    },
}

for ind, row_name in enumerate(row_names):
    items = []
    for index, column_name in enumerate(column_names):
        items.append(
            {
                "label": column_name,
                "query": queries[row_name][index],
                "is_percentage_field": percentage_fields[index],
            }
        )
        if colors.get(ind, {}).get(index):
            items[-1]["color"] = colors[ind][index]

    DAEP_QUERY_DATA.append({"title": row_name, "items": items})
