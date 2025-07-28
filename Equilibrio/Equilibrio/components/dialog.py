import reflex as rx
import reflex_chakra as rc
import asyncio

from rxconfig import config


class ClientEntryModel(rx.Model, table=True):
    """Model for client entries."""
    
    name: str
    gender: str
    birth_date: str
    job: str
    email: str
    phone: str


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

    def load_clients(self):
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

                rx.button("Save", type="submit"),
                
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


