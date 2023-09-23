from datetime import datetime


def get_uk_timestamp_utc_format() -> str:
    local_time = datetime.now()
    return local_time.strftime("%Y-%m-%d %H:%M")
