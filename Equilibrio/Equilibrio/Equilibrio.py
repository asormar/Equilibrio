import reflex as rx

from rxconfig import config

from Equilibrio.styles import styles
from Equilibrio.views.Header import Header
from Equilibrio.components.dialog import Dialog
from Equilibrio.views.Clientes import Clientes
from Equilibrio.views.Mediciones import Mediciones
from Equilibrio.views.Planificacion import Planificacion
from Equilibrio.components.dialog import FormState


class State(rx.State):
    """The app state."""

@rx.page(on_load=FormState.load_clients)


def index() -> rx.Component:
    return rx.box(
        Header(),


        rx.hstack(
    
            rx.box(
                rx.flex(
                    Dialog(),
                    justify="center",
                    padding="5px",
                    margin="0.5em 0 0.5em 0"
                ),
                rx.divider( size="4", color= "#2e4153"),
                rx.flex(
                    rx.link(
                        rx.button(
                            rx.icon("circle-user-round"),
                            rx.text("CLIENTES"),
                            variant="ghost",
                            color="white",
                            _hover= {"background_color":"#23313f"}
                            ),
                            href="#client_section"
                        ),
                    rx.link(
                        rx.button(
                            rx.icon("ruler"),
                            rx.text("MEDICIONES"),
                            variant="ghost",
                            color="white",
                            _hover= {"background_color":"#23313f"}
                            ),
                            href="#measurement_section"
                        ),
                    rx.link(
                        rx.button(
                            rx.icon("calculator"),
                            rx.text("PLANIFICACIÓN"),
                            variant="ghost",
                            color="white",
                            _hover= {"background_color":"#23313f"}
                            ),
                            href="#planification_section"
                        ),
                    
                    margin="0.5em",
                    spacing= "2",
                    direction="column"
                ),
                width="18%",
                background_color="#23313f",
                margin="0.5em 0.5em 0 1em",
                border_radius="15px",
                height="400px",
                
                

            ),


            rx.vstack(

                Clientes(),
                Mediciones(),
                Planificacion(),


                width="82%",
                margin="0.5em 1em 0 1em",
            ),



            spacing="0",
            width="100%",
            align_items="start"
        
        ),
        width="100%"
    )
    

app = rx.App(style= styles.BASE_STYLE,)
app.add_page(index)
    