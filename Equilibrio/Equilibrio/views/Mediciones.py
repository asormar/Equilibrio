import reflex as rx

from rxconfig import config

from Equilibrio.styles.styles import SECTION_CONTAINER_STYLE, SUBSECTION_STACK_STYLE
from Equilibrio.components.scrollarea import ScrollArea
from Equilibrio.components.linechart import Linechart
from Equilibrio.components.table_chart import TableChart
from Equilibrio.database.models import MeasurementModel
from Equilibrio.components.dialog import FormState
from Equilibrio.database.models import ClientEntryModel
from sqlmodel import select


class MeasurementState(rx.State):
    measurements: list[MeasurementModel] = []

    async def add_measurement(self, meditions_data: dict):
        try:
            print(f"Datos de la medición: {meditions_data}")

            # Si viene la fecha vacía, se quita para que se use la automática
            if not meditions_data.get("date"):
                meditions_data.pop("date", None)

            cont=0
            # Reemplazar valores "" por 0 en campos numéricos
            for field in ["weight", "height", "hip", "waist"]:
                if meditions_data.get(field, "") == "" or meditions_data.get(field, "") == "0" or float(meditions_data.get(field, "")) <  0:
                    meditions_data[field] = 0
                    cont +=1
                else:
                    # Opcional: convertir a float para que no haya errores si llega como string numérico
                    meditions_data[field] = float(meditions_data[field])

            if cont >= 4:
                aviso = "Todos los campos están vacíos. No se guardará la medición."
                print(aviso)
                # Crear toast de error
                return rx.toast.error(
                    aviso,
                    position="top-center",
                    duration=4000,
                    style={
                        "width":"400px"
                    }
                )
            
            elif cont >= 1 and cont < 4:
                aviso = "Ningún campo puede ser menor o igual a 0"
                print(aviso)
                # Crear toast de advertencia
                return rx.toast.error(
                    aviso,
                    position="top-center",
                    duration=4000
                )

            with rx.session() as session:
                measurement = MeasurementModel(**meditions_data)
                #print(measurement)
                session.add(measurement)
                session.commit()

            # Recargar las mediciones después de agregar
            self.load_measurements(int(meditions_data["client_id"]))
            


            # Importar StatePlanification aquí para evitar importaciones circulares
            from Equilibrio.views.Planificacion import StatePlanification
            
            # Obtener el estado de planificación y actualizar sus datos
            planification_state = await self.get_state(StatePlanification)
            await planification_state.get_client_data()
            await planification_state.get_measurements()
            


            
            print(f"Mediciones después de agregar: {self.measurements[-1]}")
            
            # Crear toast de éxito
            return rx.toast.success(
                "Medición guardada correctamente",
                position="top-center",
                duration=3000
            )
            
        except ValueError:
            aviso = "Introduce números y no otros caracteres"
            print(aviso)
            # Crear toast de advertencia
            return rx.toast.error(
                aviso,
                position="top-center",
                duration=4000
            )


    def load_measurements(self, client_id: int):
        if client_id is None:
            self.measurements = []
            return
        
        with rx.session() as session:
            self.measurements = session.exec(
                MeasurementModel.select().where(MeasurementModel.client_id == client_id)
            ).all()


    async def delete_all_measurements(self, client_id: int):
        with rx.session() as session:
            measures = session.exec(
                select(MeasurementModel)
                .where(MeasurementModel.client_id == client_id)
            ).all()

            for measure in measures:
                if measure:
                    session.delete(measure)
                    session.commit()
                    print(measure)
                    print(client_id)
            self.load_measurements(client_id)


    async def delete_measurements(self, client_id: int, measure_id: int):
        """Eliminar la última medida por client_id."""
        with rx.session() as session:
            measure_deleted = session.exec(
                select(MeasurementModel)
                .where(MeasurementModel.client_id == client_id,
                       MeasurementModel.id == measure_id)
            ).first()

            print(f"Eliminando registro: {measure_deleted}")
            if measure_deleted:
                session.delete(measure_deleted)
                session.commit()
        
        # Recargar las mediciones después de eliminar
        self.load_measurements(client_id)
        
        # Actualizar también los datos de planificación después de eliminar
        from Equilibrio.views.Planificacion import StatePlanification
        planification_state = await self.get_state(StatePlanification)
        await planification_state.get_client_data()
        await planification_state.get_measurements()


    select_value: str = "PESO"
    def change_value(self, select_value: str):
        """Change the select value var."""
        self.select_value = select_value


    
    @rx.var
    def measurements_chart(self) -> list[dict]:
        """Devuelve las mediciones en formato dict para Recharts."""
        
        # Creamos una lista vacía para almacenar los resultados
        chart_data = []

        tipos= ["weight", "height", "hip", "waist"]
        
        # Iteramos sobre cada medición en self.measurements
        for m in self.measurements:

            if any(getattr(m, tipo) == 0.0 for tipo in tipos):
                continue  # Saltamos esta medición si tiene algún 0.0

            #print(m.weight)

            # Creamos un diccionario para cada medición
            measurement_dict = {
                "date": str(m.date),      # Convertimos la fecha a string
                "weight": m.weight,       # Tomamos el peso directamente
                "height": m.height,       # Tomamos la altura directamente
                "hip": m.hip,            # Tomamos la medida de cadera
                "waist": m.waist,        # Tomamos la medida de cintura
            }
            
            # Agregamos el diccionario a nuestra lista de resultados
            chart_data.append(measurement_dict)
        
        # Devolvemos la lista completa de diccionarios
        return chart_data
    

    @rx.var
    def calculo(self) -> list[str]:
        """Calcula la diferencia para cada medición según el select_value."""
        
        # Lista que almacenará las diferencias para cada fila
        diferencias_por_fila = []

        #print(self.measurements )

        # Recorremos todas las mediciones
        for i, medicion_actual in enumerate(self.measurements):

            
            try:
                # La primera medición no tiene anterior, por lo que la diferencia queda vacía
                if i == 0:
                    diferencias_por_fila.append("")
                    continue

                # Obtenemos la medición anterior
                medicion_anterior = self.measurements[i - 1]

                #print(medicion_actual)
                #print(medicion_anterior)
                

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

                
                if "-" not in diferencia and diferencia != "0.00 %":
                    diferencia= "+"+diferencia

            except ZeroDivisionError:
                diferencia=""


            # Añadimos la diferencia calculada a la lista
            diferencias_por_fila.append(diferencia)



        diferencias_por_fila= diferencias_por_fila[::-1]
        #print(diferencias_por_fila)

        # Devolvemos la lista completa de diferencias
        return diferencias_por_fila


            

    



def Mediciones() -> rx.Component:
    return rx.box(

        rx.text("MEDICIONES", size="7", color= "#dcdaca"),

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

                        width="100%",
                        display= "flex",
                        justify_content= "center",
                        margin="0.5em 0 0 0"
                    ),

            on_submit= MeasurementState.add_measurement

            ),

            direction="column",
            style= SUBSECTION_STACK_STYLE
            
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

                    ScrollArea(TableChart(MeasurementState.measurements, MeasurementState.select_value, MeasurementState.calculo, MeasurementState.delete_measurements)),

                    #rx.text(MeasurementState.calculo),


                    width="100%"
                ),



                width="100%"
            ),

            
            style=SUBSECTION_STACK_STYLE

        ),


        style= SECTION_CONTAINER_STYLE,
        id= "measurement_section"
    )