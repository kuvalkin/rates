import re


def is_port(slug: str) -> bool:
    match = re.search('^[A-Z]{5}$', slug)

    return match is not None
