from datetime import date


def daily_report_run_key(report_date: date, pipeline_version: str = "v1") -> str:
    return f"daily-report:{report_date.isoformat()}:{pipeline_version}"
