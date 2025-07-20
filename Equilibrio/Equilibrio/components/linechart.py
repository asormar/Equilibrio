import reflex as rx
import reflex_chakra as rc

from rxconfig import config

class State(rx.State):
    """The app state."""

def Linechart() -> rx.Component:
    return rx.recharts.line_chart(

        rx.recharts.line(
            data_key="pv",
        ),
        rx.recharts.line(
            data_key="uv",
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        #data=data,
        width="100%",
        height=300,
    )