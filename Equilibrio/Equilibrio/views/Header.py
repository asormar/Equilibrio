import reflex as rx


def Header() -> rx.Component:
        return rx.hstack(
            rx.image("equilibrio_header_largo.png", border_radius="50px 50px"),
            background_color="#7492A6",
            padding="5px",
            margin="5px 5px 10px 5px",
            border_radius="5px",
            justify="center"
        ),