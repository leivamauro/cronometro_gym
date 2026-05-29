# python
import flet as ft
# locales
from constants import *
from controls.member_card import MemberCard
from controls.header import Header
from components.modal_conf import crear_modal_conf
from components.modal_nuevo_miembro import crear_modal_nuevo_miembro
from database_orm import Miembro, session as db_session
from database_orm import _estado_semaforo, _generar_status_text


def abrir_conf(page):
    modal = crear_modal_conf(page, db_session)
    page.show_dialog(modal)


def main(page: ft.Page):
    page.title = "GymFlow Manager"
    page.bgcolor = THEME_BG
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.assets_dir = "src/assets"

    def build_layout():
        is_mobile = page.width is not None and page.width < 600

        header = Header(is_mobile=is_mobile, on_add_member=lambda e: abrir_nuevo_miembro())

        # Obtener todos los miembros de la base de datos y crear una card por cada uno
        miembros = db_session.query(Miembro).all()
        cards = []
        for m in miembros:
            estado = _estado_semaforo(m, db_session)

            if estado == "vencido":
                color = ft.Colors.RED
                payment_due = True
            elif estado == "en_prueba":
                color = ft.Colors.YELLOW
                payment_due = True
            else:
                color = ft.Colors.GREEN
                payment_due = False

            cards.append(
                MemberCard(
                    page=page,
                    is_mobile=is_mobile,
                    name=m.nombre,
                    status_text=_generar_status_text(m, db_session),
                    status_color=color,
                    payment_due=payment_due,
                    miembro_id=m.id,
                    on_guardar=reconstruir,
                )
            )

        members_list = ft.Column(
            controls=cards,
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

    def reconstruir():
        page.controls.clear()
        page.add(build_layout())
        page.update()

    def abrir_nuevo_miembro():
        modal = crear_modal_nuevo_miembro(page, db_session, on_guardar=reconstruir)
        page.show_dialog(modal)

    layout = build_layout()
    page.add(layout)

    def on_resized(e):
        page.controls.clear()
        page.add(build_layout())
        page.update()

    page.on_resized = on_resized


if __name__ == "__main__":
    ft.run(main)
