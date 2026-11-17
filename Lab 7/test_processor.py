import pytest
from hypothesis import given, strategies as st
from processor import (
    parse_vitals_summary,
    compute_patient_bmi,
    assign_ward_bed,
)

inputs = st.one_of(
    st.text(),
    st.none(),
    st.sampled_from([
        "", "80,98", "80,98,37,99", "nan,98,37",
        "70/0", "-70/1.75", "70/1e-300", "inf/1.75",
        "XYZ-1", "ICU-0", "ICU--1",
    ]),
)


@given(inputs)
def test_parse_vitals_summary_no_crash(s):
    try:
        result = parse_vitals_summary(s)
    except Exception as exc:
        pytest.fail(f"Vitals crashed for {s!r}: {exc}")
    assert isinstance(result, str)


@given(inputs)
def test_compute_patient_bmi_safe(s):
    try:
        result = compute_patient_bmi(s)
    except Exception as exc:
        pytest.fail(f"BMI crashed for {s!r}: {exc}")
    assert isinstance(result, (float, str))


@given(inputs)
def test_assign_ward_bed_safe(s):
    try:
        result = assign_ward_bed(s)
    except Exception as exc:
        pytest.fail(f"Ward allocation crashed for {s!r}: {exc}")
    assert isinstance(result, str)