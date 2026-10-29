
import pytest
from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds,
)


def test_invalid_wards():
    with pytest.raises(ValueError):
        process_triage_wards("invalid", 10)


def test_negative_default_score():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_empty_wards():
    result = process_triage_wards([], 10)
    assert result == {
        "acuity_score": 0,
        "status": "NO_URGENT_CASES",
    }


def test_non_accepting_ward():
    result = process_triage_wards(
        [{"is_accepting": False, "patients": []}], 10
    )
    assert result["status"] == "NO_URGENT_CASES"


def test_normal_patient():
    wards = [{
        "is_accepting": True,
        "tier": "general",
        "patients": [{"spo2": 98, "hr": 75}],
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10
    assert result["status"] == "TRIAGE_STABLE"


def test_low_spo2_patient():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 85, "hr": 80}],
    }]
    assert process_triage_wards(wards, 10)["acuity_score"] == 60


def test_high_heart_rate_patient():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 95, "hr": 130}],
    }]
    assert process_triage_wards(wards, 10)["acuity_score"] == 60


def test_invalid_vitals_are_flagged():
    wards = [{
        "is_accepting": True,
        "patients": [
            {"spo2": 0, "hr": 70},
            {"spo2": 98, "hr": 0},
        ],
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_general_patient():
    wards = [{
        "is_accepting": True,
        "tier": "general",
        "patients": [{"spo2": 98, "hr": 70, "unconscious": True}],
    }]
    assert process_triage_wards(wards, 10)["acuity_score"] == 100


def test_unconscious_outpatient():
    wards = [{
        "is_accepting": True,
        "tier": "outpatient",
        "patients": [{"spo2": 98, "hr": 70, "unconscious": True}],
    }]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "NO_URGENT_CASES"


def test_icu_standby():
    wards = [{
        "is_accepting": True,
        "icu_standby": True,
        "patients": [],
    }]
    assert process_triage_wards(wards, 10)["acuity_score"] == 25


def test_ward_alert():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 0, "hr": 70} for _ in range(5)],
    }]
    assert process_triage_wards(wards, 10)["status"] == "WARD_ALERT"


def test_empty_oxygen_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_normal_oxygen_pressure():
    assert monitor_oxygen_manifolds([[5.0, 4.5, 4.0]]) == "PRESSURE_NORMAL"


def test_single_pressure_drop_resets():
    assert monitor_oxygen_manifolds([[3.5, 4.5, 3.5]]) == "PRESSURE_NORMAL"


def test_repeated_pressure_drop():
    assert monitor_oxygen_manifolds([[3.5, 3.0]]) == "PRESSURE_FAILURE"


def test_pressure_failure_in_later_manifold():
    assert monitor_oxygen_manifolds([[5.0], [3.0, 3.5]]) == "PRESSURE_FAILURE"
