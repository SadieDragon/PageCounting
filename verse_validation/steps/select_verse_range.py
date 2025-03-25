
# This is step 1 of the process.

from verse_validation.utils import create_list_of_verses, query_points


def select_verse_range(book: str) -> list[str]:
    '''
    Queries what the first and last verse of the current page
    of the Bible are. Assumes the book is known.

    Args:
        book (str): The current book title.

    Returns:
        (list[str]): The list of verses on the page, given the user
            selected first and last verse.
    '''
    # Grab the verse endpoints
    endpoints = query_points('verse')

    # Create the verse string
    verse_range = f'{book} {endpoints[0]}-{endpoints[1]}'

    # Create a list of verses between the first
    # and last verses on the page, and return it
    return create_list_of_verses(verse_range)
