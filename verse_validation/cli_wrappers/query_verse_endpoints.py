
# This is the CLI input for part 1.

def query_verse_endpoints(current_page: int) -> list[str]:
    '''
    Queries what the first and last verse of
    the current page of the Bible are.

    Args:
        current_page (int): The current page of the Bible.

    Returns:
    (list[str]): The user selected first and last verse.
    '''
    # The message template for the query
    message_template = ('What is the {count} verse of the page'
                        f' ({current_page})? ')

    # Ask for the first and last verse of the page
    endpoints = []
    for count in ['first', 'last']:
        endpoints.append(input(message_template.format(count=count)))

    return endpoints
