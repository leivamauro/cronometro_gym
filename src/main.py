# python
import flet as ft
# locales
from constants import *
from controls.member_card import MemberCard
from controls.header import Header
from components.modal_conf import crear_modal_conf


def abrir_conf(page):
    modal = crear_modal_conf(page)
    page.show_dialog(modal)


def main(page: ft.Page):
    page.title = "GymFlow Manager"
    page.bgcolor = THEME_BG
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.assets_dir = "src/assets"

    def build_layout():
        is_mobile = page.width is not None and page.width < 600

        header = Header(is_mobile=is_mobile)

        members_list = ft.Column(
            controls=[
                MemberCard(
                    page=page,
                    is_mobile=is_mobile,
                    name="Juan Pérez",
                    status_text="Cuota al día - Vence el 15 May 2026",
                    status_color=ft.Colors.GREEN,
                    payment_due=False,
                ),
                MemberCard(
                    page=page,
                    is_mobile=is_mobile,
                    name="María García",
                    status_text="Prueba - 5 días restantes",
                    status_color=ft.Colors.YELLOW,
                    payment_due=True,
                ),
                MemberCard(
                    page=page,
                    is_mobile=is_mobile,
                    name="Carlos Rodríguez",
                    status_text="Vencido - Debe 2 meses ($6000)",
                    status_color=ft.Colors.RED,
                    payment_due=True,
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        # Botón flotante de configuración (abajo a la izquierda)
        settings_fab = ft.Container(
            content=ft.Icon(
                icon=ft.Icons.SETTINGS,
                color=THEME_TEAL_TEXT,
                size=20,
            ),
            width=44,
            height=44,
            border_radius=22,
            bgcolor=THEME_TEAL,
            alignment=ft.Alignment.CENTER,
            on_click=lambda e: abrir_conf(page),
        )

        return ft.Stack(
            controls=[
                ft.Column(controls=[header, members_list], expand=True),
                ft.Container(
                    content=settings_fab,
                    left=20,
                    bottom=20,
                ),
            ],
            expand=True,
        )

    layout = build_layout()
    page.add(layout)

    def on_resized(e):
        page.controls.clear()
        page.add(build_layout())
        page.update()

    page.on_resized = on_resized


if __name__ == "__main__":
    ft.run(main)
