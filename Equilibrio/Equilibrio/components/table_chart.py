import reflex as rx

import reflex_chakra as rc

from rxconfig import config

from Equilibrio.styles.styles import CHART_COLORS


class State(rx.State):
    
    """The app state."""


def TableChart(medidas, mode, diferencia, eliminar) -> rx.Component:

    return rx.table.root(

                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Date"),

                        rx.cond(
                            mode == "PESO",
                            rx.fragment(
                                rx.table.column_header_cell("Peso", color=CHART_COLORS.PESO),
                                rx.table.column_header_cell("Change (%)")
                            )
                        ),

                        rx.cond(
                            mode == "ALTURA",
                            rx.fragment(
                                rx.table.column_header_cell("Altura", color= CHART_COLORS.ALTURA),
                                rx.table.column_header_cell("Change (%)")
                            )
                        ),

                        rx.cond(
                            mode == "CADERA",
                            rx.fragment(
                                rx.table.column_header_cell("Cadera", color= CHART_COLORS.CADERA),
                                rx.table.column_header_cell("Change (%)")
                            )
                        ),

                        rx.cond(
                            mode == "CINTURA",
                            rx.fragment(
                                rx.table.column_header_cell("Cintura", color= CHART_COLORS.CINTURA),
                                rx.table.column_header_cell("Change (%)")
                            )
                        ),
                        rx.cond(
                            mode == "TODO",
                            rx.fragment(
                                rx.table.column_header_cell("Peso", color= CHART_COLORS.PESO),
                                rx.table.column_header_cell("Altura", color= CHART_COLORS.ALTURA),
                                rx.table.column_header_cell("Cadera", color= CHART_COLORS.CADERA),
                                rx.table.column_header_cell("Cintura", color= CHART_COLORS.CINTURA),
                            ),

                        ),
                        

                        
                    ),
                ),

                rx.table.body(
                    rx.foreach(
                        medidas[::-1], # para que se muestre la más reciente arriba
                        lambda md, idx: rx.table.row(

                            rx.table.row_header_cell(md.date),

                            rx.cond(
                                (mode == "PESO"),
                                rx.fragment(
                                    rx.table.cell(md.weight),
                                    rx.table.cell(md.id),
                                    rx.table.cell(diferencia[idx])
                                )
                            ),
                            rx.cond(
                                (mode == "ALTURA"),
                                rx.fragment(
                                    rx.table.cell(md.height),
                                    rx.table.cell(diferencia[idx])
                                )
                            ),
                            rx.cond(
                                (mode == "CADERA"),
                                rx.fragment(
                                    rx.table.cell(md.hip),
                                    rx.table.cell(diferencia[idx])
                                )
                            ),
                            rx.cond(
                                (mode == "CINTURA"),
                                rx.fragment(
                                    rx.table.cell(md.waist),
                                    rx.table.cell(diferencia[idx])
                                )
                            ),
                            rx.cond(
                                (mode == "TODO"),
                                rx.fragment(
                                    rx.table.cell(md.weight),
                                    rx.table.cell(md.height),
                                    rx.table.cell(md.hip),
                                    rx.table.cell(md.waist),
                                    rx.table.cell(rx.button("ELIMINAR", color_scheme="red", size="1", on_click=lambda: eliminar(md.client_id, md.id)))

                                ),

                            rx.table.cell(rx.button("ELIMINAR", color_scheme="red", size="1", on_click=lambda: eliminar(md.client_id, md.id)))

                            ),
                        )
                    )
                ),

        width="100%"
        )