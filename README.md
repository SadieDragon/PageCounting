# PageCounting
A script for counting how many pages are necessary in the new journal.

Figures out which verses have valid footnotes, then figures out how many
pages are needed to store all of the verses.

Restarting this to start with a CLI program, that I will eventually transform into a GUI.

## Select Verse Range
Queries what the first and last verse of the current Bible page is.

## Create Footnote List
Queries what the last footnote of the page is, and generates a list of footnotes between the two points.

## Create Footnotes Per Verse Dict
Iterates through the generated list of verses to create a dict of footnotes per verse. Uses the generated list of footnotes for ease.
- If the verse has already been validated, skip it.
- Query the first footnote of the verse for every verse.
    - I will later be adding a function to allow for skipping chunks of verses.
    - If a letter is provided, store in a dict using the layout `{verse: first_letter}`
- Iterate through each verse in the dict, and generate a list between the current verse's first letter and the next verse's first letter.
    - If the last verse has been reached, it simply gets the rest of the footnotes.
    - Store as `{verse: [footnotes]}`

## Query Footnote Validity
Goes through the dict, and per verse query if a footnote is valid.
- Iterate through the list of footnotes.
    - If a footnote is valid, then store the current verse in valid verses, and move on.
    - If the end of the list is reached, then the verse is invalid and will be stored in invalid verses (which will not be getting pagination).

## Pagination and storage
To be described later.
