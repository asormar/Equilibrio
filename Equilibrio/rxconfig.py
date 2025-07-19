import reflex as rx

config = rx.Config(
    app_name="Equilibrio",
    favicon="logo.png",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)