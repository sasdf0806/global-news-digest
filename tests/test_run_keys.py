from datetime import date

from packages.shared.ids import daily_report_run_key


def test_daily_report_key_is_stable() -> None:
    assert daily_report_run_key(date(2026, 9, 2)) == "daily-report:2026-09-02:v1"
