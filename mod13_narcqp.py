"""Unit tests for the five stock visualizer input rules."""

import re
import unittest
from datetime import date


def valid_symbol(value):
    return re.fullmatch(r"[A-Z]{1,7}", value) is not None


def valid_chart_type(value):
    return value in ("1", "2")


def valid_time_series(value):
    return value in ("1", "2", "3", "4")


def valid_date(value):
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


class TestStockInputs(unittest.TestCase):
    def check_inputs(self, validator, valid_values, invalid_values):
        for value in valid_values:
            with self.subTest(value=value):
                self.assertTrue(validator(value))
        for value in invalid_values:
            with self.subTest(value=value):
                self.assertFalse(validator(value))

    def test_symbol(self):
        self.check_inputs(
            valid_symbol,
            ("F", "AAPL", "ABCDEFG"),
            ("", "abcdefgh", "ABCDEFGH", "aapl", "AaPL", "A1",
             "BRK.B", " AAPL", "AAPL\n", "É"),
        )

    def test_chart_type(self):
        self.check_inputs(
            valid_chart_type,
            ("1", "2"),
            ("", "0", "3", "12", "01", "1.0", "A", " 1", "2\n"),
        )

    def test_time_series(self):
        self.check_inputs(
            valid_time_series,
            ("1", "2", "3", "4"),
            ("", "0", "5", "14", "04", "4.0", "A", " 4", "4\n"),
        )

    def test_start_date(self):
        self.check_inputs(
            valid_date,
            ("2026-01-01", "2024-02-29"),
            ("", "01/01/2026", "2026-1-01", "2025-02-29",
             "2026-00-01", " 2026-01-01"),
        )

    def test_end_date(self):
        self.check_inputs(
            valid_date,
            ("2026-12-31", "2000-02-29"),
            ("", "20261231", "2026-12-1", "2026-04-31",
             "2026-13-01", "2026-12-31\n", "2026-12-31T00:00:00"),
        )


if __name__ == "__main__":
    unittest.main()
