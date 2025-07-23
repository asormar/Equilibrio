import reflex as rx

from rxconfig import config

from Equilibrio.components.dialog import Dialog
from Equilibrio.components.acordion import Acordion
from Equilibrio.components.table_clients import TableClients


class State(rx.State):
    """The app state."""


def Clientes() -> rx.Component:
    return rx.box(

        rx.text("CLIENTES"),
        
        rx.hstack(
            Dialog(),

            rx.box(
                
                TableClients(),
                width="50%",
                margin="0 0 0 30px"
            )
            
        ),

        

        rx.vstack(

            rx.text("CLIENTE SELECCIONADO"),

            rx.hstack(
                
                rx.flex(
                    rx.avatar(
                        src="/cliente.png",
                        radius="full",
                        size="7"
                    ),
                    
                    rx.vstack(
                        rx.text("NOMBRE"),

                        rx.flex(
                            rx.text("PROFESION", margin_right="2em"),
                            rx.text("FECHA DE NACIMIENTO")
                        ),




                        margin_top="1em",
                        margin_left="0.5em"
                    )
                )
                




            ),
            Acordion(),


            margin="1em",
            padding="0.5em",
            background_color="gray",
            border_radius="5px",
            
        ),





        width="100%",
        background_color="lightgray",
        padding="5px",
        
        border_radius="5px",

    )


