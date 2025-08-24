import reflex as rx
from Equilibrio.styles.styles import SECTION_CONTAINER_STYLE, SUBSECTION_STACK_STYLE
from Equilibrio.views.Mediciones import MeasurementState
from Equilibrio.components.dialog import FormState

from datetime import date

    
class StatePlanification(rx.State):
    client_age: int = 0



def Planificacion() -> rx.Component:
    # Calcular valores usando rx.cond directamente en el componente
    current_weight = rx.cond(
        MeasurementState.measurements.length() > 0,
        MeasurementState.measurements[-1].weight,
        0.0
    )
    
    current_height = rx.cond(
        MeasurementState.measurements.length() > 0,
        MeasurementState.measurements[-1].height,
        0.0
    )
    
    calc_imc = rx.cond(
        current_height > 0,
        current_weight / ((current_height/100) ** 2),
        0.0
    )

    birth_year = rx.cond(
        (FormState.selected_client_birth_date.length() >= 4),
        FormState.selected_client_birth_date[0:4].to(int),
        0
    )

    birth_month = rx.cond(
        (FormState.selected_client_birth_date.length() >= 4),
        FormState.selected_client_birth_date[5:7].to(int),
        0
    )

    birth_specific_day = rx.cond(
        (FormState.selected_client_birth_date.length() >= 4),
        FormState.selected_client_birth_date[8:10].to(int),
        0
    )

    
    current_year = date.today().year
    
    client_age = rx.cond(
        birth_year > 0,
        rx.cond(
            (date.today().month >= birth_month) & (date.today().day >= birth_specific_day),
            current_year - birth_year,
            current_year - birth_year - 1),
        0
    )


    fat_percent=rx.cond(
        FormState.selected_client_gender == "Femenino",
        1.39*calc_imc + 0.16*client_age - 10.34*0 - 9,
        rx.cond(FormState.selected_client_gender == "Masculino",
                1.39*calc_imc + 0.16*client_age - 10.34*1 - 9,
                (1.39*calc_imc + 0.16*client_age - 10.34*1 - 9)/2 + (1.39*calc_imc + 0.16*client_age - 10.34*0 - 9)/2
        )
    )
    
    return rx.box(
        rx.text("PLANIFICACIÓN"),
        rx.vstack(
            rx.text("INFORMACIÓN DEL CLIENTE"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell(""),
                        rx.table.column_header_cell("Fórmula"),
                        rx.table.column_header_cell("Actual"),
                        rx.table.column_header_cell("Objetivo"),
                        rx.table.column_header_cell("Referencia"),
                    ),
                ),
                rx.table.body(
                    rx.table.row(
                        rx.table.row_header_cell("Peso"),
                        rx.table.cell("-"),
                        rx.table.cell(current_weight),
                        rx.table.cell(rx.input(width="4em")),
                        rx.table.cell("-")
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("% de grasa"),
                        rx.table.cell("Ecuación de Peterson"),
                        rx.table.cell(fat_percent),
                        rx.table.cell("-"),
                        rx.table.cell("-"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("IMC"),
                        rx.table.cell("-"),
                        rx.table.cell(f"{calc_imc:.2f}"),
                        rx.table.cell("-"),
                        rx.table.cell("-"),
                    )
                ),
                width="100%"
            ),
            style=SUBSECTION_STACK_STYLE
        ),
        style=SECTION_CONTAINER_STYLE
    )