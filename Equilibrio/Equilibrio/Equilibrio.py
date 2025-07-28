import reflex as rx

from rxconfig import config

from Equilibrio.styles import styles
from Equilibrio.views.Clientes import Clientes
from Equilibrio.views.Mediciones import Mediciones


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

        rx.hstack(
    
            rx.box(
                rx.text("Columna 1"),
                width="5%",
                background_color="beige",
                padding="5px",
                margin="5px 5px 0 10px",
                border_radius="5px",
                height="400px",

            ),


            rx.vstack(

                Clientes(),
                Mediciones(),
                


                width="95%",
                margin="5px 10px 0 10px",
            ),



            spacing="0",
            width="100%",
            align_items="start"
        
        ),
        width="100%"
    )
    

app = rx.App(style= styles.BASE_STYLE,)
app.add_page(index)
    