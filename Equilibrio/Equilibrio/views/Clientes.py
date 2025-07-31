import reflex as rx

from rxconfig import config

from Equilibrio.components.dialog import Dialog
from Equilibrio.components.acordion import Acordion
from Equilibrio.components.table_clients import TableClients
from   Equilibrio.components.dialog import FormState


class State(rx.State):
    """The app state."""


def Clientes() -> rx.Component:
    return rx.box(

        rx.text("CLIENTES"),
        
        rx.hstack(
            Dialog(),

            rx.box(
            
            rx.heading("Clientes Registrados", size="4"),
            rx.scroll_area(

                rx.flex(
                        rx.hstack(
                        *[
                            rx.foreach(
                                FormState.clients,
                                lambda client: rx.box(
                                    rx.text(f"👤 Nombre: {client.name}"),
                                    rx.text(f"⚧ Género: {client.gender}"),
                                    rx.text(f"🎂 Fecha Nac.: {client.birth_date}"),
                                    rx.text(f"💼 Ocupación: {client.job}"),
                                    rx.text(f"📧 Email: {client.email}"),
                                    rx.text(f"📱 Teléfono: {client.phone}"),

                                    rx.hstack(
                                        rx.button(
                                            "Eliminar",
                                            color_scheme="red",
                                            size="2",
                                            on_click=lambda: FormState.delete_client(client.id), # Sin lambda se ejecutaría automáticamente al cargar la página
                                            margin_top="8px"
                                        ),
                                    ),
                                    border="1px solid gray",
                                    padding="12px",
                                    border_radius="8px",
                                    margin_bottom="10px",
                                    box_shadow="10px 5px 5px gray",
                                    min_width="300px",
                                )
                            )

                        ]
                        ),
                ),
                type="always",
                scrollbars="horizontal",
                style={"height": "auto", "width": "100%"},
            ),
                        
                width="90%",
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


