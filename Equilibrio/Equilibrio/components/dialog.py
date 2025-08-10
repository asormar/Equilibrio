import reflex as rx
import reflex_chakra as rc
import asyncio

from rxconfig import config

from Equilibrio.database.models import ClientEntryModel, SecondaryDataModel

class FormState(rx.State):
    form_data: dict = {}
    clients: list[ClientEntryModel] = []

    async def handle_submit(self, form_data: dict):
        """Guardar el formulario y actualizar la lista."""
        self.form_data = form_data

        with rx.session() as session:
            new_client = ClientEntryModel(**form_data)
            session.add(new_client)
            session.commit()

        self.load_clients()

    async def load_clients(self):
        """Cargar todos los registros de la base de datos."""
        with rx.session() as session:
            self.clients = session.exec(ClientEntryModel.select()).all()


    async def delete_client(self, client_id: int):
        """Eliminar cliente por ID."""
        with rx.session() as session:
            client = session.exec(
                ClientEntryModel.select().where(ClientEntryModel.id == client_id)
            ).first()
            if client:
                session.delete(client)
                session.commit()
        self.load_clients()


    # Campos seleccionados del cliente
    selected_client_id: int | None = None
    selected_client_name: str = ""
    selected_client_gender: str = ""
    selected_client_birth_date: str = ""
    selected_client_job: str = ""
    selected_client_email: str = ""
    selected_client_phone: str = ""

    # Datos secundarios
    selected_client_country: str = ""
    selected_client_direction: str = ""

    def select_client(self, client_id: int):
        """Selecciona un cliente y guarda todos sus datos en el estado."""
        self.selected_client_id = client_id

        # Buscar primero en la lista cargada
        client = next((c for c in self.clients if c.id == client_id), None)

        if client is None:
            with rx.session() as session:
                client = session.get(ClientEntryModel, client_id)

        if client:
            self.selected_client_name = client.name
            self.selected_client_gender = client.gender
            self.selected_client_birth_date = client.birth_date
            self.selected_client_job = client.job
            self.selected_client_email = client.email
            self.selected_client_phone = client.phone

            # --- Cargar datos secundarios ---
            with rx.session() as session:
                secondary = session.exec(
                    SecondaryDataModel.select().where(SecondaryDataModel.client_id == client_id)
                ).first()
                if secondary:
                    self.selected_client_country = secondary.country
                    self.selected_client_direction = secondary.direction
                else:
                    self.selected_client_country = ""
                    self.selected_client_direction = ""

        else:
            self.selected_client_name = ""
            self.selected_client_gender = ""
            self.selected_client_birth_date = ""
            self.selected_client_job = ""
            self.selected_client_email = ""
            self.selected_client_phone = ""
            self.selected_client_country = ""
            self.selected_client_direction = ""




def Dialog() -> rx.Component:
    return rx.dialog.root(

    rx.dialog.trigger(rx.button("Añadir Cliente", size="4")),
    rx.dialog.content(
        rx.dialog.title("Añadir Cliente"),
        rx.dialog.description(
            "Registra los diferentes datos del cliente",
            size="2",
            margin_bottom="16px",
        ),
        rx.form(
            rx.text(
                "Name",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
                placeholder="Enter your name",
                name="name",
            ),
            rx.text(
                "Género",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.select(
                ["Masculino","Femenino","Otro","Intersex"],
                name="gender"
            ),

            rx.text(
                "Fecha de nacimiento",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
            type="date",
            name="birth_date",
            ),

            rx.text(
                "Ocupación",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
                name="job",
            ),

            rx.text(
                "Número de teléfono",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
                type="tel",
                name="phone",
            ),

            rx.text(
                "Email",
                as_="div",
                size="2",
                margin_bottom="4px",
                weight="bold",
            ),
            rx.input(
                type="email",
                name="email",
            ),

            rx.flex(

                rx.button("Save", type="submit", on_click=FormState.load_clients),
                
                rx.dialog.close(
                    rx.button("Close", color_scheme="red"),
                    
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),

            on_submit=FormState.handle_submit,
            #reset_on_submit=True,
        ),

        rx.divider(),
        rx.heading("Results"),
        rx.text(FormState.form_data.to_string()),

        rx.divider(),

    ),
    

)


