
# This is for step 1

from collections.abc import Callable
from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel
from pythonbible import (convert_reference_to_verse_ids,
                         convert_verse_ids_to_references,
                         format_scripture_references,
                         get_references)
from verse_validation.step_widgets.base_step_panel import BaseStepPanel


class SelectVerseRangePanel(BaseStepPanel):
    def __init__(self,
                 parent: CTk,
                 book: str,
                 current_page: int,
                 callback: Callable = None
                 ):
        super().__init__(parent, callback)
