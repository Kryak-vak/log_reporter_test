from typing import TypeAlias

log_value_type: TypeAlias = str | int | float
log_data_type: TypeAlias = dict[str, log_value_type]
report_type: TypeAlias = dict[log_value_type, dict]

