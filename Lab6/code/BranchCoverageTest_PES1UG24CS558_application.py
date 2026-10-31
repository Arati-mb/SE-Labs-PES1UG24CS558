import pytest

from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration
)


def test_buyback_validation_branches():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5)

    with pytest.raises(ValueError):
        process_book_buybacks([], -1)


def test_approved_and_unapproved_batches():
    batches = [
        {
            "intake_approved": False,
            "format": "paperback",
            "books": [{"condition": "good"}]
        },
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"condition": "good"}]
        }
    ]

    result = process_book_buybacks(batches, 0)
    assert result["status"] == "COMPLETED"


def test_all_format_branches():
    batches = [
        {"intake_approved": True, "format": "textbook",
         "books": [{"condition": "good"}]},
        {"intake_approved": True, "format": "hardcover",
         "books": [{"condition": "good"}]},
        {"intake_approved": True, "format": "paperback",
         "books": [{"condition": "good"}]},
        {"intake_approved": True, "format": "unknown",
         "books": []}
    ]

    result = process_book_buybacks(batches, 0)
    assert result["total_payout"] == 63.0


def test_book_condition_branches():
    batches = [{
        "intake_approved": True,
        "format": "paperback",
        "books": [
            {"condition": "mint"},
            {"condition": "poor"},
            {"condition": "good"}
        ]
    }]

    result = process_book_buybacks(batches, 0)
    assert result["total_payout"] == 21.2


def test_rejection_branches():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"missing_pages": 2}]
        },
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"counterfeit": True}]
        },
        {
            "intake_approved": True,
            "format": "textbook",
            "books": [{"counterfeit": True}]
        }
    ]

    result = process_book_buybacks(batches, 0)
    assert result["status"] == "ZERO_CREDIT"


def test_payout_and_status_branches():
    credit_batch = [{
        "intake_approved": True,
        "format": "paperback",
        "books": [{"condition": "good"}],
        "payout_in_credit": True
    }]

    assert process_book_buybacks(credit_batch, 5)["total_payout"] == 13.0

    audit_batches = [
        {"intake_approved": True, "format": "unknown"}
        for _ in range(5)
    ]
    assert process_book_buybacks(audit_batches, 0)["status"] == "AUDIT_REJECTED"


def test_scanner_branches():
    assert inspect_scanner_calibration([]) == "NO_DATA"
    assert inspect_scanner_calibration([[6, 7]]) == "RECALIBRATE"
    assert inspect_scanner_calibration([[6, 2, 7]]) == "CALIBRATED"