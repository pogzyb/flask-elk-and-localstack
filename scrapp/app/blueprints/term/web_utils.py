from enum import Enum


class FlashMessages:
    bad_search_form = ('Oops! Try that again.', 'danger')


class ScrapeStatus(str, Enum):
    PENDING = 'pending'
    COMPLETE = 'complete'
    TIMEOUT = 'timeout'
