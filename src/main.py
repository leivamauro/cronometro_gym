# python
import os
import sys
import logging
from pathlib import Path

_log_dir = Path(os.environ.get("FLET_APP_STORAGE_DATA") or (Path.home() / "gestion_pagos_logs"))
try:
    _log_dir.mkdir(parents=True, exist_ok=True)
except Exception:
    _log_dir = Path.home()
logging.basicConfig(
    filename=str(_log_dir / "gestion_pagos.log"),
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
sys.excepthook = lambda ety, eval, etb: logging.error(
    "Excepcion no manejada", exc_info=(ety, eval, etb)
)

import flet as ft
from constants import *
from controls.member_card import MemberCard
from controls.header import Header
from components.modal_conf import crear_modal_conf
from components.modal_nuevo_miembro import crear_modal_nuevo_miembro
from database_orm import Miembro, Cronograma, session as db_session
from database_orm import _estado_semaforo, _generar_status_text


def abrir_conf(page):
    modal = crear_modal_conf(page, db_session)
    page.show_dialog(modal)


def main(page: ft.Page):
    page.title = "RecoverFit"
    page.bgcolor = THEME_BG
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK

    def build_layout():

        header = Header(on_add_member=lambda e: abrir_nuevo_miembro(), on_settings=lambda e: abrir_conf(page))

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
                payment_due = True  # También puede adelantar pagos

            cards.append(
                MemberCard(
                    page=page,
                    name=m.nombre,
                    status_text=_generar_status_text(m, db_session),
                    status_color=color,
                    payment_due=payment_due,
                    miembro_id=m.id,
                    on_guardar=reconstruir,
                    has_routine=db_session.query(Cronograma).filter_by(miembro_id=m.id).count() > 0,
                )
            )

        members_list = ft.Column(
            controls=cards,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        return ft.Column(controls=[header, members_list], expand=True)

    def reconstruir():
        page.controls.clear()
        page.add(build_layout())
        page.update()

    def abrir_nuevo_miembro():
        modal = crear_modal_nuevo_miembro(page, db_session, on_guardar=reconstruir)
        page.show_dialog(modal)

    try:
        layout = build_layout()
        page.add(layout)
    except Exception as ex:
        logging.error("Error al iniciar (build_layout)", exc_info=True)
        page.add(ft.Text(f"Error al iniciar: {ex}", color=ft.Colors.RED))


if __name__ == "__main__":
    ft.run(main)
