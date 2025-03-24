
from verse_validation.utils import query_points


def select_verse_range() -> list[str]:
    '''
    Queries what the first and last verse of the current page of the Bible
    are. Assumes the book is known.

    Returns:
        (list[str]): The list of verse endpoints
    '''
    # Grab the verse endpoints
    endpoints = query_points('verse')
    print(endpoints)  # DEBUG (shuddup flake8)
