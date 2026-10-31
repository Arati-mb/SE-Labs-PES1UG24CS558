
import pytest

from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration
)


def test_invalid_inputs():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5)

    with pytest.raises(ValueError):
        process_book_buybacks([], -1)


def test_all_book_formats_and_conditions():
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "books": [
                {"condition": "mint"},
                {"condition": "poor"},
                {"condition": "good"}
            ],
            "payout_in_credit": True
        },
        {
            "intake_approved": True,
            "format": "hardcover",
            "books": [{"condition": "good"}]
        },
        {
            "intake_approved": True,
            "books": [{"condition": "good"}]
        }
    ]

    result = process_book_buybacks(batches, 5)

    assert result == {
        "total_payout": 134.0,
        "status": "COMPLETED"
    }


def test_rejected_books_and_unapproved_batch():
    batches = [
        {
            "intake_approved": False,
            "format": "textbook",
            "books": [{"condition": "good"}]
        },
        {
            "intake_approved": True,
            "format": "unknown",
            "books": []
        },
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [
                {"missing_pages": 2},
                {"counterfeit": True}
            ]
        },
        {
            "intake_approved": True,
            "format": "textbook",
            "books": [{"counterfeit": True}]
        }
    ]

    result = process_book_buybacks(batches, 5)

    assert result == {
        "total_payout": 0.0,
        "status": "ZERO_CREDIT"
    }


def test_audit_rejection():
    batches = [
        {"intake_approved": True, "format": "unknown"}
        for _ in range(5)
    ]

    result = process_book_buybacks(batches, 5)

    assert result == {
        "total_payout": 0.0,
        "status": "AUDIT_REJECTED"
    }


def test_empty_scanner_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_recalibration():
    scanner_matrix = [
        [6, 7, 2]
    ]

    assert inspect_scanner_calibration(scanner_matrix) == "RECALIBRATE"


def test_scanner_calibrated():
    scanner_matrix = [
        [6, 2, 7],
        [3, 4, 5]
    ]

    assert inspect_scanner_calibration(scanner_matrix) == "CALIBRATED"
