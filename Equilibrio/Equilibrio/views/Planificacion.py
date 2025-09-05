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



    current_activity_level: float
    objective_activity_level: float
    activity_values: dict ={"No definido":1, "Sedentario":1.2, "Ligero":1.375, "Moderado":1.55, "Intenso":1.725}


    def get_current_activity_level(self, level: str):
        self.current_activity_level=self.activity_values[level]

    def get_objective_activity_level(self, level: str):
        self.objective_activity_level=self.activity_values[level]


    @rx.var
    def current_bm(self) -> float:
        
        if self.gender=="1":
            bm= 10*self.last_weight + 6.25*self.last_height - 5*int(self.client_age_data) + 5
        elif self.gender=="0":
            bm= 10*self.last_weight + 6.25*self.last_height - 5*int(self.client_age_data) -161
        else:
            bm= (10*self.last_weight + 6.25*self.last_height - 5*int(self.client_age_data) + 5 + 10*self.last_weight + 6.25*self.last_height - 5*int(self.client_age_data) -161)/2
        return bm


    current_calories: float = 0
    objective_calories: float = 0

    @rx.var
    def current_caloric_needs(self) -> float:
        self.current_calories= self.current_bm * self.current_activity_level
        return self.current_calories
    
    @rx.var
    def objective_caloric_needs(self) -> float:
        self.objective_calories= self.current_bm * self.objective_activity_level
        return self.objective_calories
    
    @rx.var
    def reference_caloric_needs(self) -> str:
        reference1= self.current_bm * 1
        reference2= self.current_bm * 2
        return f"{reference1:.0f}-{reference2:.0f} Kcal"



    fat_percent: list = [20]
    hc_percent: list = [50]
    protein_percent: list = [30]

    def get_fat_percent(self, update_fat_percent):
        self.fat_percent= update_fat_percent

    def get_hc_percent(self, update_hc_percent):
        self.hc_percent= update_hc_percent

    def get_protein_percent(self, update_protein_percent):
        self.protein_percent= update_protein_percent



    fat_g: float
    hc_g: float
    protein_g: float

    @rx.var
    def fat_g_calc(self) -> float:
        self.fat_g= ((self.fat_percent[0] /100) * self.objective_calories) / 9
        return self.fat_g
    
    @rx.var
    def hc_g_calc(self) -> float:
        self.hc_g= ((self.hc_percent[0] /100) * self.objective_calories) / 4
        return self.hc_g
    
    @rx.var
    def protein_g_calc(self) -> float:
        self.protein_g= ((self.protein_percent[0] /100) * self.objective_calories) / 4
        return self.protein_g
    

    def percent_changes(self):
        total_percent= self.fat_percent[0] + self.hc_percent[0] + self.protein_percent[0]

        




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

        rx.vstack(
            rx.text("CÁLCULOS NUTRICIONALES"),
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
                        rx.table.row_header_cell("Nivel de actividad física"),
                        rx.table.cell("-"),
                        rx.table.cell(rx.select(["No definido","Sedentario","Ligero","Moderado","Intenso"], on_change=StatePlanification.get_current_activity_level)),
                        rx.table.cell(rx.select(["No definido","Sedentario","Ligero","Moderado","Intenso"], on_change=StatePlanification.get_objective_activity_level)),
                        rx.table.cell("-")
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("Metabolismo basal"),
                        rx.table.cell("Mifflin-St Jeor"),
                        rx.table.cell(f"{StatePlanification.current_bm:.0f} Kcal"),
                        rx.table.cell("-"),
                        rx.table.cell("-"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("Calorias diarias"),
                        rx.table.cell("-"),
                        rx.table.cell(f"{StatePlanification.current_caloric_needs:.0f} Kcal"),
                        rx.table.cell(f"{StatePlanification.objective_caloric_needs:.0f} Kcal"),
                        rx.table.cell(StatePlanification.reference_caloric_needs),
                    )
                ),
                width="100%"
            ),
            style=SUBSECTION_STACK_STYLE
        ),


        rx.vstack(
            rx.text("DISTRIBUCIÓN DE MACRONUTRIENTES"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell(""),
                        rx.table.column_header_cell("Porcentaje", justify="center"),
                        rx.table.column_header_cell("Cantidad total"),
                        rx.table.column_header_cell("Cantidad en g/kg"),
                        rx.table.column_header_cell("Referencia"),
                    ),
                ),
                rx.table.body(
                    rx.table.row(
                        rx.table.row_header_cell("Grasas"),
                        rx.table.cell(rx.vstack(
                                        rx.flex(rx.heading(f"{StatePlanification.fat_percent:.0f} %"), justify="center", width="100%"), 
                                        rx.slider(color_scheme="yellow", min=0, max=100, step=1, default_value=StatePlanification.fat_percent, on_change=StatePlanification.get_fat_percent),
                                        ),
                                    justify="center"
                                    ),
                        rx.table.cell(f"{StatePlanification.fat_g_calc:.0f} g"),
                        rx.table.cell(rx.select(["No definido","Sedentario","Ligero","Moderado","Intenso"], on_change=StatePlanification.get_objective_activity_level)),
                        rx.table.cell("-")
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("Hidratos de carbono"),
                        rx.table.cell(rx.vstack(
                                        rx.flex(rx.heading(f"{StatePlanification.hc_percent:.0f} %"), justify="center", width="100%"), 
                                        rx.slider(color_scheme="green", min=0, max=100, step=1, default_value=StatePlanification.hc_percent, on_change=StatePlanification.get_hc_percent),
                                        ),
                                    justify="center"
                                    ),                        
                        rx.table.cell(f"{StatePlanification.hc_g_calc:.0f} g"),
                        rx.table.cell("-"),
                        rx.table.cell("-"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("Proteínas"),
                        rx.table.cell(rx.vstack(
                                        rx.flex(rx.heading(f"{StatePlanification.protein_percent:.0f} %"), justify="center", width="100%"), 
                                        rx.slider(color_scheme="pink", min=0, max=100, step=1, default_value=StatePlanification.protein_percent, on_change=StatePlanification.get_protein_percent),
                                        ),
                                    justify="center"
                                    ),                        
                        rx.table.cell(f"{StatePlanification.protein_g_calc:.0f} g"),
                        rx.table.cell(f"{StatePlanification.objective_caloric_needs:.0f} Kcal"),
                        rx.table.cell(StatePlanification.reference_caloric_needs),
                    )
                ),
                width="100%"
            ),
            style=SUBSECTION_STACK_STYLE
        ),



        style=SECTION_CONTAINER_STYLE
    )