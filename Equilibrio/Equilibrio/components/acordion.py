import reflex as rx
import reflex_chakra as rc

from rxconfig import config

from Equilibrio.components.dialog import FormState
from Equilibrio.database.models import ClientEntryModel, SecondaryDataModel

import asyncio


class AcordionState(rx.State):
    accordion_value: str = "item1"

    accordion_disabled: bool = False  # 🔹 nuevo estado para bloquear el acordeón temporalmente


    async def close_accordion(self):
        self.accordion_value = "None"

    async def pause_accordion(self):
        """Deshabilita el acordeón temporalmente."""
        self.accordion_value = "None"
        self.accordion_disabled = True
        await asyncio.sleep(6)
        self.accordion_disabled = False
        

    selected_client_direction: str = ""
    selected_client_country: str = ""

    async def modify_user(self, form_data: dict):
        """Modificar el cliente y sus datos secundarios."""
        client_id = int(form_data.get("client_id"))

        with rx.session() as session:
            # --- Actualizar datos del cliente principal ---
            client = session.get(ClientEntryModel, client_id)
            if client:
                client.gender = form_data.get("gender", client.gender)
                client.birth_date = form_data.get("birth_date", client.birth_date)
                client.email = form_data.get("email", client.email)
                client.phone = form_data.get("phone", client.phone)
                session.add(client)

            # --- Actualizar datos secundarios ---
            secondary = session.exec(
                SecondaryDataModel.select().where(SecondaryDataModel.client_id == client_id)
            ).first()

            if secondary is None:
                # Si no existe, lo creamos
                secondary = SecondaryDataModel(
                    client_id=client_id,
                    country=form_data.get("country", ""),
                    direction=form_data.get("direction", "")
                )
            else:
                # Si existe, lo actualizamos
                secondary.country = form_data.get("country", secondary.country)
                secondary.direction = form_data.get("direction", secondary.direction)

            self.selected_client_direction = secondary.direction
            self.selected_client_country = secondary.country

            session.add(secondary)
            session.commit()

        # Devuelvo eventos para que Reflex recargue la UI
        return [
            FormState.load_clients(),
            FormState.select_client(client_id),
            AcordionState.close_accordion(),
            AcordionState.pause_accordion(),
        ]







def Acordion() -> rx.Component:
    return rx.accordion.root(

        rx.accordion.item(
            header="Más Información",

            content=rx.form(
                rx.hstack(

                    rx.input(
                        type="hidden",
                        name="client_id",
                        value=FormState.selected_client_id
                    ),



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
                            default_value=FormState.selected_client_country),

                        rx.text("Dirección"),
                        rx.input(
                            width="100%",
                            name="direction",
                            default_value=FormState.selected_client_direction),
                        

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
        disabled=AcordionState.accordion_disabled,  # bloquea el acordeón si es necesario

        value=AcordionState.accordion_value,  # controlado por el estado
        on_value_change=lambda v: AcordionState.set_accordion_value(v)  # sincroniza si el usuario abre/cierra manualmente
    )