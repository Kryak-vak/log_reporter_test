import argparse
import pathlib
from datetime import date
from enum import Enum

from src.logs import LogReader
from src.reports import ReportAgregator, UrlAvgResponseTimeReporter


class ReportEnum(Enum):
    AVERAGE = "average"
    AVERAGE2 = "average2"
    AVERAGE3 = "average3"

    @classmethod
    def to_tuple(cls) -> tuple[str, ...]:
        return tuple(e.value for e in cls)


def main() -> None:
    arg_parser = argparse.ArgumentParser(
        prog="LogReporter",
        description="Create an in-console report of the provided log files",
        epilog="Text at the bottom of help",
        add_help=True
    )

    arg_parser.add_argument(
        "-f", "--file",
        action="extend",
        nargs="*",
        type=pathlib.Path,
        help="a relative or absolute file/folder path/paths",
    )
    arg_parser.add_argument(
        "-d", "--dir",
        action="extend",
        nargs="*",
        type=pathlib.Path,
        help="a relative or absolute file/folder path/paths",
    )
    arg_parser.add_argument(
        "-r", "--report",
        type=str,
        choices=ReportEnum.to_tuple(),
        help="a string specifying the report type",
    )
    arg_parser.add_argument(
        "--date",
        type=date.fromisoformat,
        help="a date string in ISO 8601 format (YYYY-MM-DD)",
    )
    args = arg_parser.parse_args()
    log_reader = LogReader(args.file, args.dir)
    report_agregator = ReportAgregator(
        log_reader=log_reader,
        reporters=(UrlAvgResponseTimeReporter(), )
    )
    report_agregator.run_reporters()

    for reporter in report_agregator.reporters:
        report = reporter.get_report()

        print(report)
    


if __name__ == "__main__":
    main()