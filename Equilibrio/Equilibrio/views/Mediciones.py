import reflex as rx

from rxconfig import config

from Equilibrio.components.scrollarea import ScrollArea
from Equilibrio.components.linechart import Linechart
from Equilibrio.components.table_chart import TableChart
from Equilibrio.database.models import MeasurementModel
from Equilibrio.components.dialog import FormState


class MeasurementState(rx.State):
    measurements: list[MeasurementModel] = []

    async def add_measurement(self, meditions_data: dict):
        print(f"Datos de la medición: {meditions_data}")

        # Si viene la fecha vacía, se quita para que se use la automática
        if not meditions_data.get("date"):
            meditions_data.pop("date", None)

        # Reemplazar valores "" por 0 en campos numéricos
        for field in ["weight", "height", "hip", "waist"]:
            if meditions_data.get(field, "") == "":
                meditions_data[field] = 0
            else:
                # Opcional: convertir a float para que no haya errores si llega como string numérico
                meditions_data[field] = float(meditions_data[field])

        with rx.session() as session:
            measurement = MeasurementModel(**meditions_data)
            print(measurement)
            session.add(measurement)
            session.commit()

        self.load_measurements(int(meditions_data["client_id"]))
        print(f"Mediciones después de agregar: {self.measurements[-1]}")




    def load_measurements(self, client_id: int):
        if client_id is None:
            self.measurements = []
            return
        
        with rx.session() as session:
            self.measurements = session.exec(
                MeasurementModel.select().where(MeasurementModel.client_id == client_id)
            ).all()


    select_value: str = "PESO"
    def change_value(self, select_value: str):
        """Change the select value var."""
        self.select_value = select_value


    
    @rx.var
    def measurements_chart(self) -> list[dict]:
        """Devuelve las mediciones en formato dict para Recharts."""
        return [
            {
                "date": str(m.date),      # asegúrate de que sea string o formato ISO
                "weight": m.weight,
                "height": m.height,
                "hip": m.hip,
                "waist": m.waist,
            }
            for m in self.measurements
        ]
    

    @rx.var
    def calculo(self) -> list[str]:
        """Calcula la diferencia para cada medición según el select_value."""
        
        # Lista que almacenará las diferencias para cada fila
        diferencias_por_fila = []

        # Recorremos todas las mediciones
        for i, medicion_actual in enumerate(self.measurements):

            # La primera medición no tiene anterior, por lo que la diferencia queda vacía
            if i == 0:
                diferencias_por_fila.append("")
                continue

            # Obtenemos la medición anterior
            medicion_anterior = self.measurements[i - 1]

            # Inicializamos la variable de diferencia
            diferencia = ""

            # Calculamos la diferencia según el tipo seleccionado
            if self.select_value == "PESO":
                diferencia_valor = (medicion_actual.weight - medicion_anterior.weight) / medicion_actual.weight * 100
                diferencia = f"{diferencia_valor:.2f} %"
            elif self.select_value == "ALTURA":
                diferencia_valor = (medicion_actual.height - medicion_anterior.height) / medicion_actual.height * 100
                diferencia = f"{diferencia_valor:.2f} %"
            elif self.select_value == "CADERA":
                diferencia_valor = (medicion_actual.hip - medicion_anterior.hip) / medicion_actual.hip * 100
                diferencia = f"{diferencia_valor:.2f} %"
            elif self.select_value == "CINTURA":
                diferencia_valor = (medicion_actual.waist - medicion_anterior.waist) / medicion_actual.waist * 100
                diferencia = f"{diferencia_valor:.2f} %"
            elif self.select_value == "TODO":
                # Para TODO no calculamos diferencia
                diferencia = ""

            # Añadimos la diferencia calculada a la lista
            diferencias_por_fila.append(diferencia)

        # Devolvemos la lista completa de diferencias
        return diferencias_por_fila


            

    



def Mediciones() -> rx.Component:
    return rx.box(

        rx.text("MEDICIONES"),
        rx.text(FormState.selected_client_id.to_string()),

        rx.flex(   

                rx.form(

                    rx.text("MEDICIONES BÁSICAS"),

                    rx.hstack(

                        rx.box(
                            rx.text("Peso"),
                            rx.input(
                                width="100%",
                                name="weight",
                                default_value=""),

                            rx.text("Altura"),
                            rx.input(
                                width="100%",
                                name="height",
                                default_value=""),
                            

                            width="100%"
                        ),

                        rx.box(
                            rx.text("Perímetro Cadera"),
                            rx.input(
                                width="100%",
                                name="hip",
                                default_value=""),

                            rx.text("Perímetro de la cintura"),
                            rx.input(
                                width="100%",
                                name="waist",
                                default_value=""),


                            width="100%"
                        ),
                        rx.input(
                            type="hidden",
                            name="client_id",
                            value=FormState.selected_client_id.to_string()
                        ),



                        width="100%"
                    ),

                    rx.box(
                        rx.button(
                            rx.text("Registrar", size="4"),
                            type="submit",
                            color_scheme="green",
                            size="2",
                            width="7em",
                            height="3em",
                        ),

                        rx.text(MeasurementState.measurements.to_string()),

                        width="100%",
                        display= "flex",
                        justify_content= "center",
                        margin="0.5em 0 0 0"
                    ),

            on_submit= MeasurementState.add_measurement

            ),

            direction="column",
            margin="1em",
            padding="0.5em",
            background_color="gray",
            border_radius="5px",
            
        ),



        rx.vstack(

            rx.hstack(
                rx.vstack(

                    rx.text("PROGRESO"),
                    Linechart(MeasurementState.measurements_chart, MeasurementState.select_value),
                    


                    width="100%"
                ),

                rx.spacer(),

                rx.vstack(

                    rx.flex(
                        rx.text("ÚLTIMAS MEDICIONES DE"),
                        rx.select(["PESO", "ALTURA", "CADERA", "CINTURA", "TODO"], name="measurement_type", default_value="PESO", size="1", on_change=MeasurementState.change_value),
                    ),

                    ScrollArea(TableChart(MeasurementState.measurements, MeasurementState.select_value, MeasurementState.calculo)),

                    #rx.text(MeasurementState.calculo),


                    width="100%"
                ),



                width="100%"
            ),

            
            margin="1em",
            padding="0.5em",
            background_color="gray",
            border_radius="5px",

        ),





        width="100%",
        background_color="lightgray",
        padding="5px",
        margin="5px 5px 0 0",
        border_radius="5px",

    )


