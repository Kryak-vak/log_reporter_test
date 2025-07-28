from src.logs import LogReader


def test_log_reader_reads_files(fake_log_data, fake_log_file):
    reader = LogReader(file_paths=[fake_log_file])
    logs = list(reader.read_one())

    assert logs == fake_log_data