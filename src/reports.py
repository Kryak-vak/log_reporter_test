from abc import ABC, abstractmethod
from collections import defaultdict
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
    report: report_type = defaultdict(dict)

    def add_to_report(self, log_data: log_data_type) -> None:
        group_key = log_data[self.group_key_name]
        del log_data[self.group_key_name]
        
        self.update_report(group_key, log_data)
    
    @abstractmethod
    def update_report(self, group_key, log_data: log_data_type) -> None:
        pass

    def get_report(self) -> str:
        table_data = [
            [url, *data.values()]
            for url, data in self.report.items()
        ]
        headers = [self.group_key_name, *self.report_keys]

        return tabulate(table_data, headers=headers, floatfmt=".4f")


ReporterType = TypeVar("ReporterType", bound=AbstractReporter)


class UrlAvgResponseTimeReporter(AbstractReporter):
    group_key_name = "url"
    report_keys = ("total", "average_response_time")
    report = defaultdict(lambda: defaultdict(int))

    def update_report(self, group_key: str, log_data: log_data_type) -> None:
        cur_avg = self.report[group_key]["average_response_time"]
        cur_total = self.report[group_key]["total"]
        response_time = log_data["response_time"]

        new_sum = cur_avg * cur_total + response_time
        new_total = cur_total + 1
        self.report[group_key]["average_response_time"] = new_sum / new_total
        self.report[group_key]["total"] += 1
