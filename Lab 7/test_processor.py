from hypothesis import given, strategies as st
from processor import parse_storage_quota, compute_compression_ratio, lookup_bandwidth_tier_rate


@given(st.text() | st.none())
def test_parse_storage_quota_no_crash(s):
    try:
        result = parse_storage_quota(s)
    except Exception as e:
        assert False, f"parse_storage_quota crashed with: {e!r} for input {s!r}"
    assert isinstance(result, str)


@given(st.text() | st.none())
def test_compute_compression_ratio_safe(s):
    try:
        result = compute_compression_ratio(s)
    except Exception as e:
        assert False, f"compute_compression_ratio crashed with: {e!r} for input {s!r}"
    assert result is None or isinstance(result, float)


@given(st.text() | st.none())
def test_lookup_bandwidth_tier_rate_safe(s):
    try:
        result = lookup_bandwidth_tier_rate(s)
    except Exception as e:
        assert False, f"lookup_bandwidth_tier_rate crashed with: {e!r} for input {s!r}"
    assert result is None or result in (0.08, 0.05, 0.02)
