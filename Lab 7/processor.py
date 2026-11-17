import math


def parse_vitals_summary(vitals_csv):
    error = "Invalid vitals: enter finite numbers as HR,SpO2,Temp."

    if not isinstance(vitals_csv, str):
        return error

    parts = vitals_csv.split(",")
    if len(parts) != 3:
        return error

    try:
        hr, spo2, temp = map(float, parts)
    except (ValueError, OverflowError):
        return error

    if not all(math.isfinite(x) for x in (hr, spo2, temp)):
        return error

    if hr <= 0 or not 0 <= spo2 <= 100 or temp <= 0:
        return error

    critical = hr > 120 or spo2 < 90 or temp > 39.0
    status = "CRITICAL" if critical else "STABLE"
    return f"Vitals: HR={hr}, SpO2={spo2}% - {status}"


def compute_patient_bmi(bmi_string):
    error = "Invalid BMI input: enter positive finite weight/height."

    if not isinstance(bmi_string, str):
        return error

    parts = bmi_string.split("/")
    if len(parts) != 2:
        return error

    try:
        weight, height = map(float, parts)

        if not all(
            math.isfinite(x) and x > 0
            for x in (weight, height)
        ):
            return error

        bmi = weight / (height ** 2)

        if not math.isfinite(bmi) or bmi <= 0:
            return error

        return round(bmi, 2)

    except (ValueError, ZeroDivisionError, OverflowError):
        return error


def assign_ward_bed(allocation_code):
    error = "Invalid allocation: enter a known ward and positive bed number."

    if not isinstance(allocation_code, str):
        return error

    parts = allocation_code.strip().split("-")
    if len(parts) != 2:
        return error

    ward, bed_str = (part.strip() for part in parts)

    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics",
    }

    if ward.upper() not in ward_names:
        return error

    try:
        bed_num = int(bed_str)
    except ValueError:
        return error

    if bed_num <= 0:
        return error

    return f"{ward_names[ward.upper()]} Bed #{bed_num}"


def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))


if __name__ == "__main__":
    main()