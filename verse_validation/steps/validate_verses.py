
# This is step 3 of the process.

def validate_verses(footnotes_per_verse: dict[str, list[str]]) -> list[str]:
    '''
    Queries if any footnote in the verse is a valid reference.

    Args:
        footnotes_per_verse (dict[str, list[str]]): A dict of verses with a
            list of footnotes mapped to them.

    Returns:
        (list[str]): The valid verses.
    '''
    # The output list
    valid_verses = []

    # Iterate through the dict
    for verse, footnotes in footnotes_per_verse.items():
        # Iterate through the footnotes to check if any are valid
        for footnote in footnotes:
            # Query if the footnote has verses
            msg = f'Does "{footnote}" have any references? (y / n) '
            has_refs = input(msg)

            # If the answer is "y" (or "yes"), then the verse is valid
            # store it, and break out of the loop
            if 'y' in has_refs:
                valid_verses.append(verse)
                break

    return valid_verses


# This code should replace the wonky flagging in this function, by checking
#   for which verses were not marked as valid in the function that calls this.

# You have a list of verses on the page. `verses_on_page`, probably.
# You have the result of this function, which boils down the og list to just
#   the valid verses on the page. `valid_verses`, probably.

# Use this answer to then create `invalid_verses`, which I do also want to
#   store (just not with pagination).
# https://stackoverflow.com/a/41125943
