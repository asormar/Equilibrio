import reflex as rx
from Equilibrio.styles.styles import SECTION_CONTAINER_STYLE, SUBSECTION_STACK_STYLE
from Equilibrio.views.Mediciones import MeasurementState
from Equilibrio.components.dialog import FormState
from Equilibrio.database.models import PlanificationDataModel
from sqlmodel import select
from datetime import date

    
class StatePlanification(rx.State):

    saved_id: int
    saved_client_id: int
    saved_objective_weight: float = 0.0  # Valor por defecto
    saved_activity_level: str = "No definido"
    saved_objective_activity_level: str = "No definido"
    saved_fat_percent: int = 20  # Valor por defecto
    saved_hc_percent: int = 50   # Valor por defecto
    saved_protein_percent: int = 30  # Valor por defecto

    objective_weight: float = 0.0

    imc: float
    last_weight: float
    last_height: float

    now_imc: float
    now_fat_percent: float

    gender: str
    age: str
    client_id: int

    activity_values: dict ={"No definido":1, "Sedentario":1.2, "Ligero":1.375, "Moderado":1.55, "Intenso":1.725}
    
    # Variables para controlar si los datos ya se han cargado
    data_loaded: bool = False

    @rx.var
    def current_activity_level(self) -> float:
        return self.activity_values.get(self.saved_activity_level, 1)

    @rx.var 
    def objective_activity_level(self) -> float:
        return self.activity_values.get(self.saved_objective_activity_level, 1)

    async def get_client_data(self):
        form_state = await self.get_state(FormState)
        self.age= form_state.selected_client_birth_date
        self.gender= form_state.selected_client_gender
        self.client_id= form_state.selected_client_id

        if self.gender=="Masculino":
            self.gender="1"
        elif self.gender=="Femenino":
            self.gender="0"
        else:
            self.gender="0.5"

    # Método para inicializar todos los datos necesarios
    async def initialize_data(self):
        try:
            if not self.data_loaded:
                await self.get_client_data()
                await self.get_measurements()
                await self.view_planification_data()
                # Inicializar los valores de porcentajes con los datos guardados
                self.fat_percent = [self.saved_fat_percent]
                self.hc_percent = [self.saved_hc_percent] 
                self.protein_percent = [self.saved_protein_percent]
                # También inicializar los valores anteriores
                self.anterior_fat_percent = [self.saved_fat_percent]
                self.anterior_hc_percent = [self.saved_hc_percent]
                self.anterior_protein_percent = [self.saved_protein_percent]
                self.objective_weight = self.saved_objective_weight
                self.data_loaded = True
        except:
            pass

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
                else:
                    year_age= current_year - birth_year - 1
                    year_age= str(year_age)
            else:
                year_age="0"
            
            return year_age
        
        except:
            return "0"

    async def get_measurements(self):
        measurement_state = await self.get_state(MeasurementState)
        try:
            self.last_height= measurement_state.measurements[-1].height
            self.last_weight= measurement_state.measurements[-1].weight
        except IndexError:
            self.last_height= 0
            self.last_weight= 0

    async def set_objective_weight(self, input_weight: str):
        try:
            self.objective_weight = float(input_weight)  
            await self.modify_weight_planification_data()
        except ValueError:
            self.objective_weight = 0.0

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
            return now_fat_percent
         
         except:
            return 0.0
         
    @rx.var
    def objective_fat_percent(self) -> float:
         try:
            fat_percent= 1.39*self.imc + 0.16*25 - 10.34*float(self.gender) - 9
            if fat_percent<0:
                return 0
            else:
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

    def get_current_activity_level(self, level: str):
        self.saved_activity_level = level

    def get_objective_activity_level(self, level: str):
        self.saved_objective_activity_level = level

    @rx.var
    def current_bm(self) -> float:
        if self.gender=="1":
            bm= 10*self.last_weight + 6.25*self.last_height - 5*int(self.client_age_data) + 5
        elif self.gender=="0":
            bm= 10*self.last_weight + 6.25*self.last_height - 5*int(self.client_age_data) -161
        else:
            bm= (10*self.last_weight + 6.25*self.last_height - 5*int(self.client_age_data) + 5 + 10*self.last_weight + 6.25*self.last_height - 5*int(self.client_age_data) -161)/2
        
        if bm<0:
            return 0
        else:
            return bm

    @rx.var
    def current_caloric_needs(self) -> float:
        calc= self.current_bm * self.current_activity_level
        if calc<0:
            return 0
        else:
            return calc

    @rx.var
    def objective_caloric_needs(self) -> float:
        calc= self.current_bm * self.objective_activity_level
        if calc<0:
            return 0
        else:
            return calc
    
    @rx.var
    def reference_caloric_needs(self) -> str:
        reference1= self.current_bm * 1
        reference2= self.current_bm * 2

        if reference1 and reference2 <0:
            return "0-0 Kcal"
        else:
            return f"{reference1:.0f}-{reference2:.0f} Kcal"

    anterior_fat_percent: list = [20]
    fat_percent: list = [20]
    
    anterior_hc_percent: list = [50]
    hc_percent: list = [50]

    anterior_protein_percent: list = [30]
    protein_percent: list = [30]

    def get_fat_percent(self, update_fat_percent):
        if self.hc_percent[0] <= 0 and update_fat_percent[0] > self.fat_percent[0]:
            total_percent= self.fat_percent[0] + self.hc_percent[0] + self.protein_percent[0]
            diff= total_percent - 100
            if diff<0:
                diff= abs(diff)
            self.protein_percent= [self.protein_percent[0] - diff]

        self.fat_percent= update_fat_percent
        self.percent_changes()

        if self.fat_percent[0]==100:
            self.protein_percent=[0]
            self.hc_percent=[0]
            self.fat_percent=[100]

        self.anterior_fat_percent= self.fat_percent

    def get_hc_percent(self, update_hc_percent):
        if self.fat_percent[0] <= 0 and update_hc_percent[0] > self.hc_percent[0]:
            self.fat_percent=[0]
            total_percent= self.fat_percent[0] + self.hc_percent[0] + self.protein_percent[0]
            diff= total_percent - 100
            if diff<0:
                diff= abs(diff)
            self.protein_percent= [self.protein_percent[0] - diff]

        self.hc_percent= update_hc_percent
        self.percent_changes()

        if self.hc_percent[0]==100:
            self.protein_percent=[0]
            self.fat_percent=[0]
            self.hc_percent=[100]

        self.anterior_hc_percent= self.hc_percent

    def get_protein_percent(self, update_protein_percent):
        if self.hc_percent[0] <= 0 and update_protein_percent[0] > self.protein_percent[0]:
            self.hc_percent=[0]
            total_percent= self.fat_percent[0] + self.hc_percent[0] + self.protein_percent[0]
            diff= total_percent - 100
            if diff<0:
                diff= abs(diff)
            self.fat_percent= [self.fat_percent[0] - diff]

        self.protein_percent= update_protein_percent
        self.percent_changes()

        if self.protein_percent[0]==100:
            self.fat_percent=[0]
            self.hc_percent=[0]
            self.protein_percent=[100]

        self.anterior_protein_percent= self.protein_percent

    @rx.var
    def fat_g_calc(self) -> float:
        calc= ((self.fat_percent[0] /100) * self.objective_caloric_needs) / 9
        if calc<0:
            return 0
        else:
            return calc
    
    @rx.var
    def hc_g_calc(self) -> float:
        calc= ((self.hc_percent[0] /100) * self.objective_caloric_needs) / 4
        if calc<0:
            return 0
        else:
            return calc

    @rx.var
    def protein_g_calc(self) -> float:
        calc= ((self.protein_percent[0] /100) * self.objective_caloric_needs) / 4
        if calc<0:
            return 0
        else:
            return calc

    hc_control= False

    def activate_hc_control(self):
        self.hc_control= True

    def desactivate_hc_control(self):
        self.hc_control=False

    def percent_changes(self):
        total_percent= self.fat_percent[0] + self.hc_percent[0] + self.protein_percent[0]
        diff= total_percent - 100
        if diff<0:
            diff= abs(diff)

        # Lógica de ajuste de porcentajes (mantener la misma lógica que tenías)
        if self.hc_control==False:
            if (total_percent != 100 and self.anterior_fat_percent < self.fat_percent) or (total_percent != 100 and self.anterior_protein_percent < self.protein_percent):
                self.hc_percent= [self.hc_percent[0] - diff]
            elif (total_percent == 100 and self.anterior_fat_percent < self.fat_percent) or (total_percent == 100 and self.anterior_protein_percent < self.protein_percent):
                self.hc_percent= [self.hc_percent[0] - diff]
            elif (total_percent != 100 and self.anterior_fat_percent > self.fat_percent) or (total_percent != 100 and self.anterior_protein_percent > self.protein_percent):
                self.hc_percent= [self.hc_percent[0] + diff]
            elif (total_percent == 100 and self.anterior_fat_percent > self.fat_percent) or (total_percent == 100 and self.anterior_protein_percent > self.protein_percent):
                self.hc_percent= [self.hc_percent[0] + diff]

        elif self.hc_control==True:
            if (total_percent != 100 and self.anterior_hc_percent < self.hc_percent):
                self.fat_percent= [self.fat_percent[0] - diff]
            elif (total_percent == 100 and self.anterior_hc_percent < self.hc_percent):
                self.fat_percent= [self.fat_percent[0] - diff]
            elif (total_percent != 100 and self.anterior_hc_percent > self.hc_percent):
                self.fat_percent= [self.fat_percent[0] + diff]
            elif (total_percent == 100 and self.anterior_hc_percent > self.hc_percent):
                self.fat_percent= [self.fat_percent[0] + diff]

        if self.hc_percent[0]>100:
            self.hc_percent=[100]
        elif self.hc_percent[0]<0:
            self.hc_percent=[0]

    @rx.var
    def fat_g_kg(self) -> float:
        try:
            return self.fat_g_calc / self.last_weight
        except ZeroDivisionError:
            return 0
    
    @rx.var
    def hc_g_kg(self) -> float:
        try:
            return self.hc_g_calc / self.last_weight
        except ZeroDivisionError:
            return 0
    
    @rx.var
    def protein_g_kg(self) -> float:
        try:
            return self.protein_g_calc / self.last_weight
        except ZeroDivisionError:
            return 0

    async def add_planification_data(self):
        with rx.session() as session:
            session.add(PlanificationDataModel(
                client_id=self.client_id,
                objective_weight= 0,
                activity_level= "No definido",
                objective_activity_level= "No definido",
                fat_percent= 20,
                hc_percent= 50,
                protein_percent= 30
            ))
            session.commit()
        print("Datos de planificación creados")

    async def view_planification_data(self):
        with rx.session() as session:
            record = session.exec(
                select(PlanificationDataModel).where(PlanificationDataModel.client_id == self.client_id)
            ).first()

            if record:
                self.saved_id= record.id
                self.saved_client_id= record.client_id
                self.saved_objective_weight= record.objective_weight
                self.saved_activity_level= record.activity_level
                self.saved_objective_activity_level= record.objective_activity_level
                self.saved_fat_percent= record.fat_percent
                self.saved_hc_percent= record.hc_percent
                self.saved_protein_percent= record.protein_percent
                print("Datos cargados desde la base de datos:", record)
            
            if not record:
                await self.add_planification_data()
                # Después de crear, volver a cargar
                await self.view_planification_data()

    async def delete_planification_data(self):
        with rx.session() as session:
            records = session.exec(
                select(PlanificationDataModel).where(PlanificationDataModel.client_id == self.client_id)
            ).all()

            if records:
                for record in records:
                    session.delete(record)
                session.commit()
                print("Datos de Planificación eliminados")

    async def modify_percents_planification_data(self):
        with rx.session() as session:
            record = session.exec(
                select(PlanificationDataModel).where(PlanificationDataModel.client_id == self.client_id)
            ).first()

            if record:
                record.fat_percent= self.fat_percent[0]
                record.hc_percent= self.hc_percent[0]
                record.protein_percent= self.protein_percent[0]
                session.add(record)
                session.commit()
                print("Porcentajes guardados")

    async def modify_weight_planification_data(self):
        with rx.session() as session:
            record = session.exec(
                select(PlanificationDataModel).where(PlanificationDataModel.client_id == self.client_id)
            ).first()

            if record:
                record.objective_weight= self.objective_weight
                session.add(record)
                session.commit()
                print("Peso guardado")

    async def modify_levels_planification_data(self):
        with rx.session() as session:
            record = session.exec(
                select(PlanificationDataModel).where(PlanificationDataModel.client_id == self.client_id)
            ).first()

            if record:
                record.activity_level= self.saved_activity_level
                record.objective_activity_level= self.saved_objective_activity_level
                session.add(record)
                session.commit()
                print("Niveles de actividad guardados")

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
                        rx.table.cell(
                            rx.input(
                                value=StatePlanification.saved_objective_weight.to_string(), 
                                on_change=StatePlanification.set_objective_weight,
                                width="4em"
                            )
                        ),
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
                        rx.table.cell(
                            rx.select(
                                ["No definido","Sedentario","Ligero","Moderado","Intenso"], 
                                value=StatePlanification.saved_activity_level, 
                                on_change=[
                                    StatePlanification.get_current_activity_level,
                                    StatePlanification.modify_levels_planification_data
                                ]
                            )
                        ),
                        rx.table.cell(
                            rx.select(
                                ["No definido","Sedentario","Ligero","Moderado","Intenso"], 
                                value=StatePlanification.saved_objective_activity_level, 
                                on_change=[
                                    StatePlanification.get_objective_activity_level,
                                    StatePlanification.modify_levels_planification_data
                                ]
                            )
                        ),
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
                        rx.table.cell(
                            rx.vstack(
                                rx.flex(rx.heading(f"{StatePlanification.fat_percent:.0f} %"), justify="center", width="100%"), 
                                rx.slider(
                                    color_scheme="yellow", 
                                    min=0, 
                                    max=100, 
                                    step=1, 
                                    value=StatePlanification.fat_percent, 
                                    on_change=StatePlanification.get_fat_percent.throttle(10), 
                                    on_focus=StatePlanification.desactivate_hc_control
                                ),
                            ),
                            justify="center"
                        ),
                        rx.table.cell(f"{StatePlanification.fat_g_calc:.0f} g"),
                        rx.table.cell(f"{StatePlanification.fat_g_kg:.2f} g/kg"),
                        rx.table.cell("10 - 35%")
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("Hidratos de carbono"),
                        rx.table.cell(
                            rx.vstack(
                                rx.flex(rx.heading(f"{StatePlanification.hc_percent:.0f} %"), justify="center", width="100%"), 
                                rx.slider(
                                    color_scheme="green", 
                                    min=0, 
                                    max=100, 
                                    step=1, 
                                    value=StatePlanification.hc_percent, 
                                    on_change=StatePlanification.get_hc_percent.throttle(10), 
                                    on_focus=StatePlanification.activate_hc_control
                                ),
                            ),
                            justify="center"
                        ),                        
                        rx.table.cell(f"{StatePlanification.hc_g_calc:.0f} g"),
                        rx.table.cell(f"{StatePlanification.hc_g_kg:.2f} g/kg"),
                        rx.table.cell("45 - 65%"),
                    ),
                    rx.table.row(
                        rx.table.row_header_cell("Proteínas"),
                        rx.table.cell(
                            rx.vstack(
                                rx.flex(rx.heading(f"{StatePlanification.protein_percent:.0f} %"), justify="center", width="100%"), 
                                rx.slider(
                                    color_scheme="pink", 
                                    min=0, 
                                    max=100, 
                                    step=1, 
                                    value=StatePlanification.protein_percent, 
                                    on_change=StatePlanification.get_protein_percent.throttle(10), 
                                    on_focus=StatePlanification.desactivate_hc_control
                                ),
                            ),
                            justify="center"
                        ),                        
                        rx.table.cell(f"{StatePlanification.protein_g_calc:.0f} g"),
                        rx.table.cell(f"{StatePlanification.protein_g_kg:.2f} g/kg"),
                        rx.table.cell("20 - 35%"),
                    )
                ),
                width="100%"
            ),
            on_mouse_leave=StatePlanification.modify_percents_planification_data,
            style=SUBSECTION_STACK_STYLE
        ),

        # Agregar este evento al cargar el componente
        on_mount=StatePlanification.initialize_data,
        style=SECTION_CONTAINER_STYLE
    )