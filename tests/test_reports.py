from collections import defaultdict

from src.reports import ReportAgregator, UrlAvgResponseTimeReporter


def test_avg_response_time_computation(fake_log_data):
    reporter = UrlAvgResponseTimeReporter()
    
    for entry in fake_log_data:
        reporter.add_to_report(entry)

    report = reporter.report

    grouped = defaultdict(list)
    for entry in fake_log_data:
        grouped[entry["url"]].append(entry["response_time"])

    for url, response_times in grouped.items():
        expected_total = len(response_times)
        expected_avg = sum(response_times) / expected_total

        assert url in report
        assert report[url]["total"] == expected_total
        assert abs(report[url]["average_response_time"] - expected_avg) < 1e-6

class FakeLogReader:
    def __init__(self, data: list[dict]):
        self.data = data

    def read_one(self):
        for entry in self.data:
            yield entry


def test_report_aggregator(fake_log_data):
    reader = FakeLogReader(data=fake_log_data)
    reporter = UrlAvgResponseTimeReporter()
    aggregator = ReportAgregator(log_reader=reader, reporters=(reporter,))  # type: ignore[arg-type]

    aggregator.run_reporters()
    report = aggregator.reporters[0].report


    grouped = defaultdict(list)
    for entry in fake_log_data:
        grouped[entry["url"]].append(entry["response_time"])

    for url, response_times in grouped.items():
        expected_total = len(response_times)
        expected_avg = sum(response_times) / expected_total

        assert url in report
        assert report[url]["total"] == expected_total
        assert abs(report[url]["average_response_time"] - expected_avg) < 1e-6

