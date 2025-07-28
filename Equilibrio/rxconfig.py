import reflex as rx

config = rx.Config(
    app_name="Equilibrio",
    favicon="logo.png",
    db_url="sqlite:///reflex.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)