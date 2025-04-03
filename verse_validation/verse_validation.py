
# Optimizations:
#   - I can create footnotes list per verse and query on the fly
#       - "Is {first footnote} valid?"
#           - Yes: Store as valid, and do not create the list
#           - No: Ask for first footnote of next verse
#               - Does this result in a list?
#                   - Yes: Query until end of list for a valid footnote.
#                       If none are found, then verse is invalid.
#                   - No: Verse is invalid

# Order of load:

# New Book Panel to set first book's endpoints

# Select Verse Range Panel to select the range of verses
#   - if end of book is reached, at end of cycle:
#       - Paginate
#       - Is book last book to do?
#           - Yes: Open New Book Panel
#           - No: Wrap up program
# Create Footnotes Per Verse Dict to set the list of footnotes to validate
# Validate Verses to validate each verse by the footnote and add to valid
#   verses

# Need to also save session data per loop, to ensure that if any error occurs,
#   no data or work is lost.
# Need to handle loading paused sessions.
