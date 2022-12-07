import os


def get_date_format() -> str | None:
    return os.getenv('APP_DATE_FORMAT')
