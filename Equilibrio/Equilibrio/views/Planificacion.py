import reflex as rx

from Equilibrio.styles.styles import SECTION_CONTAINER_STYLE

def Planificacion() -> rx.Component:
    return rx.box(
        rx.text("PLANIFICACIÓN"),

        style= SECTION_CONTAINER_STYLE
    )