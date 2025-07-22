import reflex as rx
import reflex_chakra as rc

from rxconfig import config

from Equilibrio.components.table_chart import TableChart


class State(rx.State):
    """The app state."""

def ScrollArea() -> rx.Component:
    return rx.scroll_area(

        rx.flex(
            TableChart()
        ),
        type="always",
        scrollbars="vertical",
        style={"height": "370px"},
    )