
import pytest

from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds,
)


def test_empty_wards():
    assert process_triage_wards([], 10)["status"] == "NO_URGENT_CASES"


def test_ward_not_accepting():
    wards = [{"is_accepting": False, "patients": []}]
    assert process_triage_wards(wards, 10)["status"] == "NO_URGENT_CASES"


def test_ward_capacity_available():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 98, "hr": 75}],
        }
    ]
    assert process_triage_wards(wards, 10)["status"] == "TRIAGE_STABLE"


def test_ward_alert():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 0, "hr": 70} for _ in range(5)],
        }
    ]
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


def test_invalid_wards_input():
    with pytest.raises(ValueError):
        process_triage_wards("invalid", 10)


def test_invalid_default_acuity():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_unconscious_outpatient():
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "patients": [
                {"spo2": 98, "hr": 75, "unconscious": True}
            ],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "NO_URGENT_CASES"


def test_low_oxygen_patient():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 85, "hr": 75}],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60


def test_icu_standby():
    wards = [
        {
            "is_accepting": True,
            "icu_standby": True,
            "patients": [{"spo2": 98, "hr": 75}],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 35


def test_unconscious_general_ward():
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "patients": [
                {"spo2": 98, "hr": 75, "unconscious": True}
            ],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 100
