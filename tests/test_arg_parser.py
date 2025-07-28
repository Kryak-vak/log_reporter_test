import pathlib
import sys
from datetime import date

from src.main import create_arg_parser


def test_arg_parser_basic(monkeypatch):
    test_args = [
        "testname",
        "-f", "file1.log", "file2.log",
        "-d", "some/dir",
        "-r", "average",
        "--date", "2025-06-22"
    ]

    monkeypatch.setattr(sys, "argv", test_args)

    parser = create_arg_parser()
    args = parser.parse_args()

    assert args.file == [pathlib.Path("file1.log"), pathlib.Path("file2.log")]
    assert args.dir == [pathlib.Path("some/dir")]
    assert args.report == "average"
    assert args.date == date(2025, 6, 22)

def test_arg_parser_no_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["testname"])

    parser = create_arg_parser()
    args = parser.parse_args()

    assert args.file is None
    assert args.dir is None
    assert args.report is None
    assert args.date is None
