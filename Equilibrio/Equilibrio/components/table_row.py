import reflex as rx
import reflex_chakra as rc

from rxconfig import config


class State(rx.State):
    """The app state."""

def Table_Row(photo:str, name:str, birth:str) -> rx.Component:
    return rx.table.row(
        
        rx.table.row_header_cell(rx.image(
            photo,
            width="130px",
            height="auto",
            border_radius="15px 15px",
            border="5px solid #555",)),

        rx.table.cell(rx.text(name, size="5"), font_weight="bold", color="black",justify="center",),
        rx.table.cell(rx.text(birth, size="5"), font_weight="bold", color="black",justify="center",),

        height="100px",
        align="center",
        
    )