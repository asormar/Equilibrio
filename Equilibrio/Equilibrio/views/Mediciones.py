import reflex as rx

from rxconfig import config

from Equilibrio.components.scrollarea import ScrollArea
from Equilibrio.components.linechart import Linechart
from Equilibrio.database.models import MeasurementModel
from Equilibrio.components.dialog import FormState


class MeasurementState(rx.State):
    measurements: list[MeasurementModel] = []

    async def add_measurement(self, meditions_data: dict):
        print(f"Datos de la medición: {meditions_data}")

        with rx.session() as session:
            measurement = MeasurementModel(**meditions_data)
            print(measurement)
            session.add(measurement)
            session.commit()

        self.load_measurements(int(meditions_data["client_id"]))




    def load_measurements(self, client_id: int):
        with rx.session() as session:
            self.measurements = session.exec(
                MeasurementModel.select().where(MeasurementModel.client_id == client_id)
            ).all()



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
                                name="weight"),

                            rx.text("Altura"),
                            rx.input(
                                width="100%",
                                name="height"),
                            

                            width="100%"
                        ),

                        rx.box(
                            rx.text("Perímetro Cadera"),
                            rx.input(
                                width="100%",
                                name="hip"),

                            rx.text("Perímetro de la cintura"),
                            rx.input(
                                width="100%",
                                name="waist"),


                            width="100%"
                        ),

                        rx.input(name="date", type="date"),
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
                    rx.text("AÑADIR MEDICIÓN DE ..."),

                    rx.flex(

                        rx.input(
                            type="date",
                        ),
                        rx.input(),
                        rx.select(
                            ["kg","lb","oz"]
                        ),
                        rx.button("Registrar"),

                    ),

                    rx.text("PROGRESO"),
                    Linechart(),
                    


                    width="100%"
                ),

                rx.vstack(

                    rx.text("ÚLTIMAS MEDICIONES DE ..."),
                    ScrollArea(),



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


