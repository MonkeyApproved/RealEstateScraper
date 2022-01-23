import re
from logging import getLogger
from datetime import date

logger = getLogger("Date Conversion")
date_pattern = re.compile("(?P<day>\d{1,2}) (?P<month>[^\x00-\x7F]+) (?P<year>\d{4})")


greek_month_names = {
    "Ιανουαρίου": 1,
    "Φεβρουαρίου": 2,
    "Μαρτίου": 3,
    "Απριλίου": 4,
    "Μαΐου": 5,
    "Ιουνίου": 6,
    "Ιουλίου": 7,
    "Αυγούστου": 8,
    "Σεπτεμβρίου": 9,
    "Οκτωβρίου": 10,
    "Νοεμβρίου": 11,
    "Δεκεμβρίου": 12,
}


def parse_greek_date(date_string: str):
    match = date_pattern.match(date_string)
    if not match:
        logger.warning(f'unknown date format: "{date_string}"')
        return None

    # convert month name to month number
    month = greek_month_names.get(match.group("month"), None)
    if month is None:
        logger.warning(f'unknown month: "{match.group("month")}"')
        return None

    day = int(match.group("day"))
    year = int(match.group("year"))
    return date(year=year, month=month, day=day)
