import pytest
from cloud_storage_tier import process_storage_tenants, monitor_replication_latency


def t(tier="hot", buckets=None, vault=False, active=True):
    return {"account_active": active, "tier": tier, "has_backup_vault": vault,
            "buckets": buckets if buckets is not None else []}


def b(size, corrupted=False, egress=0):
    return {"size_gb": size, "corrupted": corrupted, "egress_gb": egress}


def test_single_active_hot_tenant():
    r = process_storage_tenants([t(buckets=[b(100, egress=50)])], 10.0)
    assert r == {"total_billed": 2.5, "status": "BILLED"}


def test_invalid_tenants_type():
    with pytest.raises(ValueError):
        process_storage_tenants("bad", 1.0)


def test_negative_fee():
    with pytest.raises(ValueError):
        process_storage_tenants([], -1.0)


def test_inactive_tenant_skipped():
    r = process_storage_tenants([t(active=False, buckets=[b(100)])], 1.0)
    assert r == {"total_billed": 0.0, "status": "ZERO_USAGE"}


def test_cool_and_archive_rates():
    r = process_storage_tenants([t("cool", [b(100)]), t("archive", [b(100)])], 0)
    assert r["total_billed"] == 2.0


def test_unknown_tier_flagged():
    r = process_storage_tenants([t("weird", [b(100)])], 0)
    assert r["status"] == "ZERO_USAGE"


def test_invalid_size_flagged():
    r = process_storage_tenants([t(buckets=[b(0)])], 0)
    assert r["status"] == "ZERO_USAGE"


def test_corrupted_hot_bucket_no_charge():
    r = process_storage_tenants([t(buckets=[b(100, True), b(100)])], 0)
    assert r["total_billed"] == 2.5


def test_corrupted_archive_zeroes_charge():
    r = process_storage_tenants([t("archive", [b(100), b(100, True), b(100)])], 0)
    assert r["status"] == "ZERO_USAGE"


def test_large_bucket_discount_egress_and_vault():
    r = process_storage_tenants([t(buckets=[b(1000, egress=150)], vault=True)], 10.0)
    assert r["total_billed"] == 22.5 + 4.0 + 10.0


def test_audit_flagged():
    r = process_storage_tenants([t(buckets=[b(100), b(0), b(0), b(0), b(0), b(0)])], 0)
    assert r == {"total_billed": 2.5, "status": "AUDIT_FLAGGED"}


def test_latency_no_data():
    assert monitor_replication_latency([]) == "NO_DATA"


def test_latency_alert():
    assert monitor_replication_latency([[100], [250, 300]]) == "SYNC_LAG_ALERT"


def test_latency_synced():
    assert monitor_replication_latency([[250, 100, 250]]) == "SYNCED"
