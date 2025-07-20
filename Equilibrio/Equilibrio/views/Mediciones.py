import reflex as rx

from rxconfig import config

from Equilibrio.components.scrollarea import ScrollArea
from Equilibrio.components.linechart import Linechart


class State(rx.State):
    """The app state."""


def Mediciones() -> rx.Component:
    return rx.box(

        rx.text("MEDICIONES"),

        rx.vstack(

            rx.text("MEDICIONES BÁSICAS"),

            rx.hstack(

                rx.box(
                    rx.text("Peso"),
                    rx.input(
                        width="100%",
                        default_value="Femenino"),

                    rx.text("Altura"),
                    rx.input(
                        width="100%",
                        default_value="España"),
                    

                    width="100%"
                ),

                rx.box(
                    rx.text("Perímetro Cadera"),
                    rx.input(
                        width="100%",
                        default_value="17/03/2002"),

                    rx.text("Perímetro de la cintura"),
                    rx.input(
                        width="100%",
                        default_value="carlosgimenex@gmail.com"),


                    width="100%"
                ),
                



                width="100%"
            ),




            margin="1em",
            padding="0.5em",
            background_color="gray",
            border_radius="5px",
            
        ),



        rx.vstack(

            rx.hstack(
                rx.vstack(
                    rx.text("AÑADIR MEDICIÓN DE ..."),

                    rx.flex(

                        rx.input(
                            type="date",
                        ),
                        rx.input(),
                        rx.select(
                            ["kg","lb","oz"]
                        ),
                        rx.button("Registrar"),

                    ),

                    rx.text("PROGRESO"),
                    Linechart(),
                    


                    width="100%"
                ),

                rx.vstack(

                    rx.text("ÚLTIMAS MEDICIONES DE ..."),
                    ScrollArea(),



                    width="100%"
                ),



                width="100%"
            ),

            
            margin="1em",
            padding="0.5em",
            background_color="gray",
            border_radius="5px",

        ),





        width="100%",
        max_width="95%",
        background_color="lightgray",
        padding="5px",
        margin="5px 5px 0 0",
        border_radius="5px",

    )


