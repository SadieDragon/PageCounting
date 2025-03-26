
# This is step 1 of the process.

from string import Template
from verse_validation.utils import create_list_of_verses


def select_verse_range(book: str, current_page: int) -> list[str]:
    '''
    Queries what the first and last verse of the current page
    of the Bible are. Assumes the book is known.

    Args:
        book (str): The current book title.
        current_page (int): The current page of the Bible.

    Returns:
        (list[str]): The list of verses on the page, given the user
            selected first and last verse.
    '''
    # Repeated part of the message
    message_template = Template(('What is the $count verse of the page'
                                 f' ({current_page})? '))

    # Ask for the first and last of the item
    endpoints = []
    for count in ['first', 'last']:
        # Update the prompt by filling in the template
        prompt = message_template.substitute(count=count)

        # Query, and store the input
        endpoints.append(input(prompt))

    # Create the verse string
    verse_range = f'{book} {endpoints[0]}-{endpoints[1]}'

    # Create a list of verses between the first
    # and last verses on the page, and return it
    return create_list_of_verses(verse_range)
