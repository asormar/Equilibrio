import reflex as rx

class Login(rx.Model, table=True):
    username: str
    email: str
    password: str

def prueba() -> rx.Component:
    return rx.container(
        rx.box(
            rx.vstack(
                rx.vstack(
                    rx.heading("Testing App", size="9"),
                    align="center",
                ),
                rx.heading("Login Page", size="6"),
                align="center",
                padding_bottom="2em",
            ),
            rx.box(
                rx.card(

                )
            )
        )
    )
