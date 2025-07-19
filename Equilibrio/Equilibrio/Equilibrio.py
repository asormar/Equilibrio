import reflex as rx

from rxconfig import config

from Equilibrio.styles import styles
from Equilibrio.views.Clientes import Clientes


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    return rx.box(
            
        rx.hstack(
            rx.text("Header"),
            background_color="lightblue",
            padding="5px",
            margin="5px 5px 10px 5px",
            border_radius="5px"
        ),

        rx.divider( size="4", color_scheme="cyan"),

        rx.flex(

            rx.hstack(
        
                rx.box(
                    rx.text("Columna 1"),
                    width="100%",
                    max_width="5%",
                    background_color="beige",
                    padding="5px",
                    margin="5px 0 0 5px",
                    border_radius="5px",
                    height="400px",

                ),

                rx.divider(orientation="vertical", size="4", color_scheme="cyan"),

                Clientes(),


                #spacing="0",
                width="100%"
            )
        ),
        width="100%"
    )
    

app = rx.App(style= styles.BASE_STYLE)
app.add_page(index)
