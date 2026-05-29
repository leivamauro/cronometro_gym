# python
import flet as ft
# locales
from constants import *


class Header(ft.Container):
    def __init__(self, is_mobile=False, on_add_member=None):
        super().__init__()

        # Logo como círculo
        logo = ft.Container(
            content=ft.Image(
                src="src/assets/icon.png",
                width=40,
                height=40,
                fit="cover",
            ),
            width=50,
            height=50,
            border_radius=25,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        # Título
        title = ft.Text(
            "GymFlow Manager",
            color=THEME_TEXT_PRIMARY,
            size=24 if is_mobile else 32,
            weight="bold",
        )

        # Botón
        button = ft.FilledButton(
            content=ft.Text(value="NUEVO MIEMBRO"),
            bgcolor=THEME_TEAL,
            color=THEME_TEAL_TEXT,
            icon=ft.Icons.ADD,
            style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
            on_click=on_add_member or (lambda e: None),
        )

        # Layout responsive
        if is_mobile:
            content = ft.Column(
                controls=[
                    ft.Row(
                        controls=[logo, title],
                        spacing=15,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[button],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=12,
            )
            self.padding = ft.Padding(20, 16, 20, 16)
        else:
            content = ft.Row(
                controls=[
                    ft.Row(
                        controls=[logo, title],
                        spacing=15,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            self.padding = ft.Padding(20, 16, 20, 16)

        self.content = content
        self.bgcolor = THEME_HEADER_BG
        self.border_radius = ft.BorderRadius(0, 0, 12, 12)
        self.margin = ft.Margin.only(bottom=20)
