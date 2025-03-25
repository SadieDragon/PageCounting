
from pythonbible import (convert_reference_to_verse_ids,
                         convert_verse_ids_to_references,
                         format_scripture_references,
                         get_references)


def create_list_of_verses(verse_str: str) -> list[str]:
    '''
    Take the input string and convert it to a list of verses.

    Args:
        verse_str (str): Ex: `Gen 1:1-2:5`

    Returns:
        (list[str]): A list of verses.
    '''
    # Convert the input str into a NormalizedReference
    verse_str_ref = get_references(verse_str)[0]

    # Convert the NormalizedReference into a list of verse ids
    verse_ids = convert_reference_to_verse_ids(verse_str_ref)

    # Convert each id to a verse str again
    list_of_verses = []
    for verse_id in verse_ids:
        # Convert the verse id (as a list) to a NormalizedReference
        verse_ref = convert_verse_ids_to_references([verse_id])

        # Format it back into a str, and append to list of verses
        list_of_verses.append(format_scripture_references(verse_ref))

    return list_of_verses
