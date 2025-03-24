
from string import Template


def query_points(item: str) -> list[str]:
    '''
    Queries the first and last points of the page for whatever item is
    passsed in.

    Args:
        item (str): `verse` or `footnote`

    Returns:
        (list[str]): The endpoints.
    '''
    # Repeated part of the message
    message_template = Template('What is the $count $item of the page? ')

    # Ask for the first and last of the item
    endpoints = []
    for count in ['first', 'last']:
        # Update the prompt by filling in the template
        prompt = message_template.substitute(count=count, item=item)

        # Query, and store the input
        endpoints.append(input(prompt))

    return endpoints
