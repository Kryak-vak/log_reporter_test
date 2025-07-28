from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date, datetime
from typing import TypeVar

from tabulate import tabulate

from src.common_types import log_data_type, report_type
from src.logs import LogReader


class ReportAgregator:
    def __init__(
        self,
        log_reader: LogReader,
        reporters: tuple["ReporterType", ...]
    ) -> None:
        self.log_reader = log_reader
        self.reporters = reporters
        self.reports: list[report_type] = []
    
    def run_reporters(self) -> None:
        for log_data in self.log_reader.read_one():
            for reporter in self.reporters:
                reporter.add_to_report(log_data)


class AbstractReporter(ABC):
    group_key_name: str
    report_keys: tuple[str, ...]

    def __init__(self, date: date | None) -> None:
        self.date = date
        if self.date is None:
            self.add_to_report = self._add_to_report
        
        self.report: report_type = defaultdict(dict)

    def add_to_report(self, log_data: log_data_type) -> None:
        log_date_str = log_data["@timestamp"]
        assert isinstance(log_date_str, str)

        log_date = datetime.fromisoformat(log_date_str).date()
        if log_date != self.date:
            return None
        
        self._add_to_report(log_data)

    def _add_to_report(self, log_data: log_data_type) -> None:
        group_key = log_data[self.group_key_name]
        self.update_report(group_key, log_data)
    
    @abstractmethod
    def update_report(self, group_key, log_data: log_data_type) -> None:
        pass

    def get_formatted_report(self) -> str:
        table_data = [
            [url, *(data[key] for key in self.report_keys)]
            for url, data in self.report.items()
        ]
        headers = [self.group_key_name, *self.report_keys]

        return tabulate(table_data, headers=headers, floatfmt=".4f")


ReporterType = TypeVar("ReporterType", bound=AbstractReporter)


class UrlAvgResponseTimeReporter(AbstractReporter):
    group_key_name = "url"
    report_keys = ("total", "average_response_time")
    
    def __init__(self, date: date | None = None) -> None:
        super().__init__(date=date)

        self.report = defaultdict(lambda: defaultdict(int))

    def update_report(self, group_key: str, log_data: log_data_type) -> None:
        cur_avg = self.report[group_key]["average_response_time"]
        cur_total = self.report[group_key]["total"]
        response_time = log_data["response_time"]

        new_sum = cur_avg * cur_total + response_time
        new_total = cur_total + 1
        self.report[group_key]["average_response_time"] = new_sum / new_total
        self.report[group_key]["total"] += 1
