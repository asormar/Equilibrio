import reflex as rx
import reflex_chakra as rc

from rxconfig import config

from Equilibrio.components.dialog import FormState
from Equilibrio.database.models import ClientEntryModel


class AcordionState(rx.State):
    accordion_value: str = "item1"  # abierto por defecto

    def close_accordion(self):
        self.accordion_value = "None"  # lo cierra


    def modify_user(self):
        with rx.session() as session:
            client_modificating = session.exec(ClientEntryModel.select().where(ClientEntryModel.id == FormState.selected_client_id)).all()
            print(f"Modificando cliente: {client_modificating}")
            #client.gender = self.gender
            #client.birth_date = self.birth_date
            #client.email = self.email
            #client.phone = self.phone
            #session.add(client)
            #session.commit()


def Acordion() -> rx.Component:
    return rx.accordion.root(

        rx.accordion.item(
            header="Más Información",

            content=rx.form(
                rx.hstack(

                    

                    rx.box(
                        rx.text("Género"),
                        rx.input(
                            width="100%",
                            name="gender",
                            default_value=FormState.selected_client_gender),

                        rx.text("País"),
                        rx.input(
                            width="100%",
                            name="country",
                            default_value="España"),

                        rx.text("Dirección"),
                        rx.input(
                            width="100%",
                            name="direction",
                            default_value="Calle Colón"),
                        

                        width="100%"
                    ),

                    rx.box(
                        rx.text("Nacimiento"),
                        rx.input(
                            width="100%",
                            name="birth_date",
                            default_value=FormState.selected_client_birth_date),

                        rx.text("Email"),
                        rx.input(
                            width="100%",
                            name="email",
                            default_value=FormState.selected_client_email),

                        rx.text("Teléfono"),
                        rx.input(
                            width="100%",
                            name="phone",
                            default_value=FormState.selected_client_phone),


                        width="100%"
                    ),



                    
                    width="100%"
                ),

                rx.flex(

                    rx.button("Save", type="submit"),
                    
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),

                on_submit=AcordionState.modify_user
            )
        ),
        width="100%",
        collapsible=True,
        color_scheme="gray",
        variant="surface",
        show_dividers=False,

        value=AcordionState.accordion_value,  # controlado por el estado
        on_value_change=lambda v: AcordionState.set_accordion_value(v)  # sincroniza si el usuario abre/cierra manualmente
    )