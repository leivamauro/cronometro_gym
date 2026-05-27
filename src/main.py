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

        return ft.Column(
            controls=[header, members_list],
            expand=True,
        )

    layout_col = build_layout()
    page.add(layout_col)

    def on_resized(e):
        page.controls.clear()
        page.add(build_layout())
        page.update()

    page.on_resized = on_resized


if __name__ == "__main__":
    ft.run(main)
