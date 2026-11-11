
import math


def verify_isbn10_format(isbn_str):
    if not isinstance(isbn_str, str):
        return None

    cleaned = isbn_str.replace('-', '').strip().upper()

    if len(cleaned) != 10:
        return None

    if not cleaned[:9].isdigit():
        return None

    if not (cleaned[9].isdigit() or cleaned[9] == 'X'):
        return None

    first_digit = int(cleaned[0])
    group_code = cleaned[1:4]
    check_char = cleaned[9]

    return f"Group {group_code}: Starts {first_digit}, Checksum {check_char}"


def calculate_depreciation_factor(book_age_str):
    if not isinstance(book_age_str, str):
        return None

    try:
        parts = book_age_str.split('/')

        if len(parts) != 2:
            return None

        age = float(parts[0])
        life = float(parts[1])

        if not math.isfinite(age) or not math.isfinite(life):
            return None

        if age < 0 or life <= 0:
            return None

        depreciation = 1.0 - (age / life)

        return round(max(0.1, depreciation), 2)

    except (ValueError, TypeError, OverflowError):
        return None


def lookup_condition_multiplier(condition_code):
    if not isinstance(condition_code, str):
        return None

    grade = condition_code.strip().upper()

    multipliers = {
        "MINT": 1.25,
        "LIKE_NEW": 1.00,
        "VERY_GOOD": 0.80,
        "GOOD": 0.60,
        "POOR": 0.30
    }

    return multipliers.get(grade)


def main():
    print("==== Running verify_isbn10_format ====")
    isbn_in = input("Enter ISBN-10 (e.g. 0-306-40615-2): ")
    print(verify_isbn10_format(isbn_in))

    print("\n==== Running calculate_depreciation_factor ====")
    age_in = input("Enter age/lifespan in years (e.g. 3/10): ")
    print("Depreciation Factor:", calculate_depreciation_factor(age_in))

    print("\n==== Running lookup_condition_multiplier ====")
    cond_in = input("Enter condition (e.g. MINT, GOOD, POOR): ")
    print("Multiplier:", lookup_condition_multiplier(cond_in))


if __name__ == "__main__":
    main()
