import math
import re


def parse_storage_quota(quota_str):
    """
    Parses storage quota string with unit suffix into Gigabytes (GB).
    Format: '<digits><2-letter unit>' (e.g. '500MB', '20GB', '2TB').
    Returns 'Invalid quota' for any malformed input.
    """
    if not isinstance(quota_str, str):
        return "Invalid quota"
    match = re.fullmatch(r"([0-9]+)(MB|GB|TB)", quota_str.strip().upper(), re.ASCII)
    if not match:
        return "Invalid quota"
    multipliers = {"MB": 0.001, "GB": 1.0, "TB": 1000.0}
    try:
        gb_total = int(match.group(1)) * multipliers[match.group(2)]
    except (ValueError, OverflowError):
        return "Invalid quota"
    return f"Quota: {gb_total:.2f} GB"


def compute_compression_ratio(size_metric_str):
    """
    Computes compression ratio: raw_bytes / compressed_bytes.
    Format: 'raw_bytes:compressed_bytes' (e.g. '1024:256').
    Returns None for malformed input or a zero/invalid compressed size.
    """
    if not isinstance(size_metric_str, str):
        return None
    parts = size_metric_str.split(":")
    if len(parts) != 2:
        return None
    try:
        raw_bytes = float(parts[0])
        comp_bytes = float(parts[1])
    except ValueError:
        return None
    if not (math.isfinite(raw_bytes) and math.isfinite(comp_bytes)):
        return None
    if raw_bytes < 0 or comp_bytes <= 0:
        return None
    try:
        return round(raw_bytes / comp_bytes, 2)
    except OverflowError:
        return None


def lookup_bandwidth_tier_rate(tier_descriptor):
    """
    Looks up rate per GB for egress traffic using the first 3 letters of the tier name.
    Returns None for non-string input or an unknown tier.
    """
    if not isinstance(tier_descriptor, str):
        return None
    prefix = tier_descriptor.strip().upper()[:3]
    tier_rates = {"HOT": 0.08, "COL": 0.05, "ARC": 0.02}
    return tier_rates.get(prefix)


def main():
    print("==== Running parse_storage_quota ====")
    q_input = input("Enter quota (e.g. 500MB, 10GB, 2TB): ")
    print(parse_storage_quota(q_input))

    print("\n==== Running compute_compression_ratio ====")
    c_input = input("Enter raw:compressed bytes (e.g. 1024:256): ")
    ratio = compute_compression_ratio(c_input)
    print("Compression Ratio:", ratio if ratio is not None else "Invalid input")

    print("\n==== Running lookup_bandwidth_tier_rate ====")
    t_input = input("Enter tier descriptor (e.g. HOT_TIER, COLD, ARCHIVE): ")
    rate = lookup_bandwidth_tier_rate(t_input)
    print("Rate per GB: $", rate if rate is not None else "Unknown tier")


if __name__ == "__main__":
    main()
