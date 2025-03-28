
from customtkinter import CTkEntry, CTkFrame, CTkLabel


def create_label_entry_frame(parent: CTkFrame, text: str) -> CTkEntry:
    '''
    Create a frame with a label packed next to the entrybox.

    Args:
        parent (CTkFrame): The parent frame for this subframe to go in.
        text (str): The text to go in the label.

    Returns:
        (CTkEntry): The entry box, to be accessed for data later.
    '''
    # Create a frame to grid things into
    new_frame = CTkFrame(master=parent)
    new_frame.pack(padx=5, pady=5)

    # Create a label
    new_label = CTkLabel(master=new_frame, text=text)
    new_label.grid(column=0, padx=5, pady=5, row=0, sticky='W')

    # Create the entry box
    new_entry = CTkEntry(master=new_frame, width=75)
    new_entry.grid(column=1, padx=5, pady=5, row=0, sticky='E')

    return new_entry
