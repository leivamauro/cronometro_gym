# python
import flet as ft
# locales
from constants import *
from controls.member_card import MemberCard
from controls.header import Header

def main(page: ft.Page):
    page.title = "GymFlow Manager"
    page.bgcolor = THEME_BG
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.assets_dir = "src/assets"

    header = Header(page=page)

    members_list = ft.Column(
        controls=[
            MemberCard(
                page=page,
                name="Juan Pérez",
                status_text="Cuota al día - Vence el 15 May 2026",
                status_color=ft.Colors.GREEN,
                payment_due=False,
            ),
            MemberCard(
                page=page,
                name="María García",
                status_text="Prueba - 5 días restantes",
                status_color=ft.Colors.YELLOW,
                payment_due=True,
            ),
            MemberCard(
                page=page,
                name="Carlos Rodríguez",
                status_text="Vencido - Debe 2 meses ($6000)",
                status_color=ft.Colors.RED,
                payment_due=True,
            ),
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    page.add(
        ft.Column(
            controls=[header, members_list],
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
