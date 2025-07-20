import reflex as rx
import reflex_chakra as rc

from rxconfig import config


class State(rx.State):
    """The app state."""


def Dialog() -> rx.Component:
    return rx.dialog.root(

    rx.dialog.trigger(rx.button("Añadir Cliente", size="4")),
    rx.dialog.content(
        rx.dialog.title("Añadir Cliente"),
        rx.dialog.description(
            "Registra los diferentes datos del cliente",
            size="2",
            margin_bottom="16px",
        ),
        rx.flex(
            rx.text(
                "Name",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
                placeholder="Enter your name",
            ),
            rx.text(
                "Género",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.select(
                ["Masculino","Femenino","Otro","Intersex"]
            ),

            rx.text(
                "Fecha de nacimiento",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
            type="date",
            width="12em"
            ),

            rx.text(
                "Ocupación",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
            ),

            rx.text(
                "Número de teléfono",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
            ),

            rx.text(
                "Email",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
            ),
            direction="column",
            spacing="3",
        ),
        rx.flex(
            rx.dialog.close(
                rx.button(
                    "Cancel",
                    color_scheme="gray",
                    variant="soft",
                ),
            ),
            rx.dialog.close(
                rx.button("Save"),
            ),
            spacing="3",
            margin_top="16px",
            justify="end",
        ),
    ),
)


