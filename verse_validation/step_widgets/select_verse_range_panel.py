
# This is for step 1

from customtkinter import CTk, CTkButton, CTkEntry, CTkFrame, CTkLabel
from pythonbible import (convert_reference_to_verse_ids,
                         convert_verse_ids_to_references,
                         format_scripture_references,
                         get_references)
from verse_validation.gui_utils import create_label_entry_frame


class SelectVerseRangePanel(CTkFrame):
    book: str
    # callback: None

    first_verse_entry: CTkEntry
    last_verse_entry: CTkEntry

    def __init__(self,
                 parent: CTk,
                 book: str,
                 current_page: int,
                 callback=None):
        '''
        The panel for the first step of the process: Select Verse Range

        Args:
            parent (CTk): The parent window.
            book (str): The current book.
            current_page (int): The current page.
            callback: To-be-defined - Used to return to the parent class
                with the information.
        '''
        # Create the frame for all of this stuff to go into
        super().__init__(parent)

        # Store the information that was passed in
        self.book = book
        self.callback = callback

        # PEP8 compliant text var for the information label
        text = f'Select verse range for page {current_page} ({self.book})'
        # The label that will inform the user what to do
        info_label = CTkLabel(self, text=text)
        info_label.pack(padx=5, pady=5)

        # Create the entries for the first and last verse to be selected in
        # TODO: Make first_verse be a drop down; previous last verse, or the
        #   next verse in the book?
        self.first_verse_entry = create_label_entry_frame(self, 'First Verse:')
        self.last_verse_entry = create_label_entry_frame(self, 'Last Verse:')

        # Create a button for the user to confirm and finish.
        submit_button = CTkButton(self, text='Confirm', command=self.submit)
        submit_button.pack(padx=5, pady=5)

    def submit(self):
        '''
        Collect the endpoints from the entries, and then create a verse str.
        From there, create a list of verses to return to the callback fn.
        '''
        # Grab the end points from the entries
        first_verse = self.first_verse_entry.get()
        last_verse = self.last_verse_entry.get()

        # If both first and last are not selected, then do not finish
        if not (first_verse and last_verse):
            # TODO: Make this a pop up
            print('I did not get data in both entries. Try again.')
            return

        # TODO: Make a cleanup for if I hit a random button while inputting

        # Create the str to create a list of verses from
        verse_range = f"{self.book} {first_verse}-{last_verse}"

        # Create the list of verses
        verse_list = self.create_list_of_verses(verse_range)

        print(verse_list)  # DEBUG
        # Return to the parent fn
        # self.callback(verse_list)

        # Also, remove this panel
        self.destroy()

    def create_list_of_verses(self, verse_str: str) -> list[str]:
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
