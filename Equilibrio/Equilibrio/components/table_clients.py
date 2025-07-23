import reflex as rx
import reflex_chakra as rc

from rxconfig import config

from Equilibrio.components.table_row import Table_Row


class State(rx.State):
    """The app state."""

def TableClients() -> rx.Component:
    return rx.table.root(
        rx.table.body(
            Table_Row(
                photo="https://randomuser.me/api/portraits/men/10.jpg",
                name="Luis Ramírez",
                birth="1980/04/12"
            ),
            Table_Row(
                photo="https://randomuser.me/api/portraits/women/11.jpg",
                name="Elena Vargas",
                birth="1979/09/23"
            ),
            Table_Row(
                photo="https://randomuser.me/api/portraits/men/12.jpg",
                name="Javier Ortega",
                birth="1993/01/30"
            ),
            Table_Row(
                photo="https://randomuser.me/api/portraits/women/13.jpg",
                name="Patricia León",
                birth="1986/07/15"
            ),
            Table_Row(
                photo="https://randomuser.me/api/portraits/men/14.jpg",
                name="Sergio Molina",
                birth="1991/11/05"
            ),
            Table_Row(
                photo="https://randomuser.me/api/portraits/women/15.jpg",
                name="Isabel Romero",
                birth="1984/03/18"
            ),
            Table_Row(
                photo="https://randomuser.me/api/portraits/men/16.jpg",
                name="Fernando Gil",
                birth="1989/12/27"
            ),
            Table_Row(
                photo="https://randomuser.me/api/portraits/women/17.jpg",
                name="Carmen Peña",
                birth="1995/06/09"
            ),
            Table_Row(
                photo="https://randomuser.me/api/portraits/men/18.jpg",
                name="Alberto Suárez",
                birth="1982/08/21"
            ),
        ),
        width="100%",
        height="250px",
        variant="surface",
        background_color="gray",
        align="center"

    )