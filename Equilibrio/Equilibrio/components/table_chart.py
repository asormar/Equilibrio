# components/table_chart.py
import reflex as rx

def TableChart(medidas, mode) -> rx.Component:
    def generar_fila(m):
        return rx.cond(
            mode == "PESO", [m.date, m.weight],
            rx.cond(
                mode == "ALTURA", [m.date, m.height],
                rx.cond(
                    mode == "CADERA", [m.date, m.hip],
                    rx.cond(
                        mode == "CINTURA", [m.date, m.waist],
                        [m.date, m.weight, m.height, m.hip, m.waist],
                    ),
                ),
            ),
        )

    # Cabeceras según modo
    headers = rx.cond(
        mode == "PESO", ["Fecha", "Peso (kg)"],
        rx.cond(
            mode == "ALTURA", ["Fecha", "Altura (cm)"],
            rx.cond(
                mode == "CADERA", ["Fecha", "Cadera (cm)"],
                rx.cond(
                    mode == "CINTURA", ["Fecha", "Cintura (cm)"],
                    ["Fecha", "Peso (kg)", "Altura (cm)", "Cadera (cm)", "Cintura (cm)"],
                ),
            ),
        ),
    )

    # Fila de cabeceras
    header_row = rx.hstack(
        rx.foreach(
            headers,
            lambda h: rx.text(h, font_weight="bold", width="100%"),
        ),
        rx.spacer(),
        width="100%",
        margin_bottom="10px",
    )

    # Cada fila como hstack de valores
    data_rows = rx.vstack(
        rx.foreach(
            medidas,
            lambda m: rx.hstack(
                rx.foreach(
                    generar_fila(m),
                    lambda value: rx.text(value, width="100%"),
                ),
                rx.spacer(),
                width="100%",
            ),
        ),
        rx.spacer(),
        width="100%",
    )

    return rx.vstack(
        header_row,
        data_rows,
        rx.spacer(),
        width="100%",
    )
