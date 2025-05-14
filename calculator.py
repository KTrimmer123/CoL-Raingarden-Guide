import json
import math

# Load pre-processed FEH lookup data
with open("raingarden_lookup_data.json") as f:
    data = json.load(f)

lookup_tables = data["tables"]
columns_to_use = data["columns"]

def round_up_to_nearest_10(n):
    return int(math.ceil(n / 10.0)) * 10

def get_required_storage(catchment_area, duration):
    key = str(duration)
    rounded_area = str(round_up_to_nearest_10(catchment_area))
    table = lookup_tables.get(key, {})
    row = table.get(rounded_area)
    if not row:
        return None
    return {
        label: row.get(columns_to_use[label], 0)
        for label in columns_to_use
    }

def calculate_storage(area_m2, void_ratio, depth_mm, freeboard_mm):
    depth_m = depth_mm / 1000
    freeboard_m = freeboard_mm / 1000
    return (area_m2 * depth_m * void_ratio) + (area_m2 * freeboard_m)

def pass_fail(required, available):
    return {label: "PASS" if available >= required[label] else "FAIL" for label in required}
