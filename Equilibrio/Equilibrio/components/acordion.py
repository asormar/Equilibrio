import reflex as rx
import reflex_chakra as rc

from rxconfig import config


class State(rx.State):
    """The app state."""


def Acordion() -> rx.Component:
    return rx.accordion.root(

        rx.accordion.item(
            header="Más Información",
            content=rx.hstack(

                rx.box(
                    rx.text("Género"),
                    rx.input(
                        width="100%",
                        default_value="Femenino"),

                    rx.text("País"),
                    rx.input(
                        width="100%",
                        default_value="España"),

                    rx.text("Dirección"),
                    rx.input(
                        width="100%",
                        default_value="Calle Colón"),
                    

                    width="100%"
                ),

                rx.box(
                    rx.text("Nacimiento"),
                    rx.input(
                        width="100%",
                        default_value="17/03/2002"),

                    rx.text("Email"),
                    rx.input(
                        width="100%",
                        default_value="carlosgimenex@gmail.com"),

                    rx.text("Teléfono"),
                    rx.input(
                        width="100%",
                        default_value="675290372"),


                    width="100%"
                ),



                
                width="100%"
            )
        ),
        width="100%",
        collapsible=True,
        color_scheme="gray",
        variant="surface",
        show_dividers=False
    )