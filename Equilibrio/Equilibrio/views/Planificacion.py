import reflex as rx
from Equilibrio.styles.styles import SECTION_CONTAINER_STYLE, SUBSECTION_STACK_STYLE
from Equilibrio.views.Mediciones import MeasurementState
from Equilibrio.components.dialog import FormState
import math

from datetime import date

    
class StatePlanification(rx.State):
    objective_weight: float = 0.0

    imc: float
    last_weight: float
    last_height: float

    now_imc: float
    now_fat_percent: float

    gender: str
    age: str


    async def get_client_data(self):
        form_state = await self.get_state(FormState)
        self.age= form_state.selected_client_birth_date
        self.gender= form_state.selected_client_gender

        if self.gender=="Masculino":
            self.gender="1"
        elif self.gender=="Femenino":
            self.gender="0"
        else:
            self.gender="0.5"

        yield


    @rx.var
    def client_age_data(self) -> str:

        try:
            current_year = date.today().year

            birth_year = int(self.age[0:4])
            birth_month = int(self.age[5:7])
            birth_specific_day = int(self.age[8:10])

            if birth_year>0:
                if (date.today().month >= birth_month and date.today().day >= birth_specific_day) or (date.today().month > birth_month):
                    year_age= current_year - birth_year
                    year_age= str(year_age)
                    #print(year_age)
                else:
                    year_age= current_year - birth_year - 1
                    year_age= str(year_age)
                    #print(year_age)
            else:
                year_age="0"
            
            return year_age
        
        except:
            return "0"


    async def get_measurements(self):
        measurement_state = await self.get_state(MeasurementState)
        self.last_height= measurement_state.measurements[-1].height
        self.last_weight= measurement_state.measurements[-1].weight

        yield
    

    async def set_objective_weight(self, input_weight: str):  # Cambiar de float a str
        try:
            self.objective_weight = float(input_weight)  
            #print(f"Peso objetivo actualizado a: {self.objective_weight}")
        except ValueError:
            self.objective_weight = 0.0  # Valor por defecto si la conversión falla
            #print("Entrada inválida para el peso objetivo. Debe ser un número. Convirtiendo a 0.0")


    @rx.var
    def range_fat_percent(self) -> str:
        if self.gender == "1":  # Masculino
            return "10-20%"
        elif self.gender == "0":  # Femenino
            return "18-28%"
        else:  # Otro o no especificado
            return "14-24%"
            
    @rx.var
    def objective_imc(self) -> float:
         try:
            self.imc= self.objective_weight / ((self.last_height/100) ** 2)
            return self.imc
         
         except ZeroDivisionError:
            return 0.0
    
    @rx.var
    def current_imc(self) -> float:
         try:
            self.now_imc= self.last_weight / ((self.last_height/100) ** 2)
            return self.now_imc
         
         except:
            return 0.0
    

    @rx.var
    def current_fat_percent(self) -> float:
         try:
            now_fat_percent= 1.39*self.now_imc + 0.16*25 - 10.34*float(self.gender) - 9
            #print(now_fat_percent)
            return now_fat_percent
         
         except:
            return 0.0
         
    @rx.var
    def objective_fat_percent(self) -> float:
         try:
            fat_percent= 1.39*self.imc + 0.16*25 - 10.34*float(self.gender) - 9
            return fat_percent
         
         except:
            return 0.0
         
    @rx.var
    def reference_weight(self) -> str:
         try:
            weight_diff= self.objective_weight - self.last_weight

            if weight_diff > 0:
                weight_diff = f"+{weight_diff:.2f} kg"
            else:
                weight_diff = f"{weight_diff:.2f}"
                weight_diff = weight_diff.replace("-", "")
                weight_diff = f"-{weight_diff} kg"

            return weight_diff
         
         except:
            return "0.0"




def Planificacion() -> rx.Component:
    
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
                        rx.table.cell(StatePlanification.last_weight),
                        rx.table.cell(rx.input(on_change=[StatePlanification.set_objective_weight,
                                                          StatePlanification.get_measurements,
                                                          StatePlanification.get_client_data], width="4em")),
                        rx.table.cell(StatePlanification.reference_weight)
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("Porcentaje de grasa"),
                        rx.table.cell("Ecuación de Peterson"),
                        rx.table.cell(f"{StatePlanification.current_fat_percent:.2f}%"),
                        rx.table.cell(f"{StatePlanification.objective_fat_percent:.2f}%"),
                        rx.table.cell(StatePlanification.range_fat_percent),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("IMC"),
                        rx.table.cell(StatePlanification.client_age_data),
                        rx.table.cell(f"{StatePlanification.current_imc:.2f}"),
                        rx.table.cell(f"{StatePlanification.objective_imc:.2f}"),
                        rx.table.cell("18-25"),
                    )
                ),
                width="100%"
            ),
            style=SUBSECTION_STACK_STYLE
        ),
        style=SECTION_CONTAINER_STYLE
    )