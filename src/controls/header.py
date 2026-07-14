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
            col=BREAK_POINTS,
        )

        # Título
        title = ft.Text(
            "RecoverFit",
            color=THEME_TEXT_PRIMARY,
            size=24 if is_mobile else 32,
            weight="bold",
            text_align=ft.TextAlign.CENTER,
            expand=True,
            col=BREAK_POINTS,
        )

        # Botón
        button = ft.FilledButton(
            content=ft.Text(value="NUEVO MIEMBRO"),
            bgcolor=THEME_TEAL,
            color=THEME_TEAL_TEXT,
            icon=ft.Icons.ADD,
            style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
            on_click=on_add_member or (lambda e: None),
            col=BREAK_POINTS,
        )

        
        content = ft.Row(
            controls=[
                ft.ResponsiveRow(
                    controls=[logo, title, button],
                    spacing=15,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.padding = ft.Padding(20, 16, 20, 16)

        self.content = content
        self.bgcolor = THEME_HEADER_BG
        self.border_radius = ft.BorderRadius(0, 0, 12, 12)
        self.margin = ft.Margin.only(bottom=20)
