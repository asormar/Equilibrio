import reflex as rx
import reflex_chakra as rc

from rxconfig import config


class State(rx.State):
    """The app state."""

def TableClients() -> rx.Component:
    return rx.table.root(
                rx.table.body(
                    rx.table.row(
                        rx.table.row_header_cell("07/09/2025"),
                        rx.table.cell("130 kg"),
                        rx.table.cell(""),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("08/09/2025"),
                        rx.table.cell("129 kg"),
                        rx.table.cell("-1 %"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("09/09/2025"),
                        rx.table.cell("129.3"),
                        rx.table.cell("+0.2%"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("10/09/2025"),
                        rx.table.cell("129.1"),
                        rx.table.cell("-0.2%"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("11/09/2025"),
                        rx.table.cell("128.6"),
                        rx.table.cell("-0.7%"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("11/09/2025"),
                        rx.table.cell("128.6"),
                        rx.table.cell("-0.7%"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("11/09/2025"),
                        rx.table.cell("128.6"),
                        rx.table.cell("-0.7%"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("11/09/2025"),
                        rx.table.cell("128.6"),
                        rx.table.cell("-0.7%"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("11/09/2025"),
                        rx.table.cell("128.6"),
                        rx.table.cell("-0.7%"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("11/09/2025"),
                        rx.table.cell("128.6"),
                        rx.table.cell("-0.7%"),
                    ),
                ),
                width="100%",
                size="1"
            )