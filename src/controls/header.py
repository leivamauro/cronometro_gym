# python
import flet as ft
# locales
from constants import *


class Header(ft.Container):

    def __init__(self, on_add_member=None, on_settings=None):
        super().__init__()

        # Logo como círculo
        logo = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src="icon.png",
                        width=50,
                        height=50,
                        fit="cover",
                    ),
                    width=50,
                    height=50,
                    border_radius=25,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
            ],
            col=BREAK_POINTS,
            alignment=ft.MainAxisAlignment.CENTER,
        ) 

        # Título
        title = ft.Text(
            "RecoverFit",
            color=THEME_TEXT_PRIMARY,
            size=32,
            weight="bold",
            text_align=ft.TextAlign.CENTER,
            expand=True,
            col=BREAK_POINTS,
        )

        # Botón agregar
        add_button = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.ADD,
                icon_color=THEME_TEAL_TEXT,
                icon_size=22,
                mouse_cursor=ft.MouseCursor.CLICK,
                tooltip="Agregar miembro",
                on_click=on_add_member or (lambda e: None),
            ),
            width=44,
            height=44,
            border_radius=22,
            bgcolor=BTNS_BG,
            alignment=ft.Alignment.CENTER,
        )

        # Botón configuración
        settings_button = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.SETTINGS,
                icon_color=THEME_TEAL_TEXT,
                icon_size=22,
                mouse_cursor=ft.MouseCursor.CLICK,
                tooltip="Configuración",
                on_click=on_settings or (lambda e: None),
            ),
            width=44,
            height=44,
            border_radius=22,
            bgcolor=BTNS_BG,
            alignment=ft.Alignment.CENTER,
        )

        buttons_row = ft.Row(
            controls=[add_button, settings_button],
            spacing=10,
            alignment=ft.MainAxisAlignment.END,
            col=BREAK_POINTS,
        )

        
        content = ft.Row(
            controls=[
                ft.ResponsiveRow(
                    controls=[logo, title, buttons_row],
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