import reflex as rx
import reflex_chakra as rc

from rxconfig import config

class State(rx.State):
    """The app state."""

def Linechart(medidas, mode) -> rx.Component:
    return rx.recharts.line_chart(

        rx.cond(
            mode == "PESO",
            rx.recharts.line(
                data_key="weight",
                stroke="#8884d8",
                type_="monotone",
            ),
        ),
        rx.cond(
            mode == "ALTURA",
            rx.recharts.line(
                data_key="height",
                stroke="#82ca9d",
                type_="monotone",
            ),
        ),
        rx.cond(
            mode == "CADERA",
            rx.recharts.line(
                data_key="hip",
                stroke="#ffc658",
                type_="monotone",
            ),
        ),
        rx.cond(
            mode == "CINTURA",
            rx.recharts.line(
                data_key="waist",
                stroke="#ff7300",
                type_="monotone",
            ),
        ),
        rx.cond(
            mode == "TODO",
            rx.fragment(
                rx.recharts.line(data_key="weight", stroke="#8884d8", type_="monotone"),
                rx.recharts.line(data_key="height", stroke="#82ca9d", type_="monotone"),
                rx.recharts.line(data_key="hip", stroke="#ffc658", type_="monotone"),
                rx.recharts.line(data_key="waist", stroke="#ff7300", type_="monotone"),
            ),
        ),
        rx.recharts.x_axis(
            data_key="date",
            stroke="#111827",                  # color de la línea del eje
            tick={"fill": "#111827"},          # color de los números/fechas
            tick_line=True,                    # o False si no quieres las rayitas
            axis_line=True,
        ),

        rx.recharts.y_axis(
            stroke="#111827",
            tick={"fill": "#111827"},
            tick_line=True,
            axis_line=True,
        ),
        data=medidas,
        width="100%",
        height=350,
    )