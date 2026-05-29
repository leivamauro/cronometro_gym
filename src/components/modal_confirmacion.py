# python
import flet as ft
# local
from constants import *
from database_orm import Miembro


def crear_modal_confirmacion(nombre_miembro: str, page: ft.Page, session, miembro_id: int, on_guardar=None):
    """
    Crea un AlertDialog de confirmación antes de eliminar un miembro.
    ---
    Entrada:
        nombre_miembro (str): Nombre del miembro (para mostrar).
        page (ft.Page): Página de Flet.
        session (Session): Sesión activa de SQLAlchemy.
        miembro_id (int): ID del miembro a eliminar.
        on_guardar (callable, opcional): Callback al eliminar (refresca la UI).
    Salida:
        ft.AlertDialog: Modal de confirmación.
    """
    is_mobile = page.width is not None and page.width < 600

    # --- Header del modal (diseño unificado) ---
    header = ft.Container(
        content=ft.Text(
            "Confirmar Eliminación",
            size=14,
            weight="bold",
            color=THEME_TEXT_PRIMARY,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=THEME_HEADER_BG_MODAL,
        padding=ft.Padding(20, 14, 20, 14),
        alignment=ft.Alignment.CENTER,
        border_radius=ft.BorderRadius.only(top_left=12, top_right=12),
    )

    # --- Acción cerrar ---
    def cerrar_modal(e):
        modal_confirmacion.open = False
        page.update()

    # --- Cuerpo: mensaje de advertencia ---
    mensaje = ft.Text(
        f"¿Está seguro de que desea eliminar a {nombre_miembro}?\n\n"
        "Se eliminarán todos sus datos, incluyendo el historial de pagos.\nEsta acción no se puede deshacer.",
        color=THEME_TEXT_PRIMARY,
        size=15,
    )

    # --- Botones ---
    def eliminar(e):
        """Elimina el miembro de la base de datos y cierra el modal."""
        miembro = session.query(Miembro).filter_by(id=miembro_id).first()
        if miembro:
            session.delete(miembro)
            session.commit()
        cerrar_modal(e)
        if on_guardar:
            on_guardar()

    eliminar_btn = ft.FilledButton(
        content=ft.Text("Eliminar"),
        bgcolor=ft.Colors.RED,
        color=THEME_TEXT_PRIMARY,
        style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
        on_click=eliminar,
    )

    cancelar_btn = ft.OutlinedButton(
        content=ft.Text("Cancelar"),
        style=ft.ButtonStyle(
            color=THEME_TEXT_PRIMARY,
            side=ft.BorderSide(1, THEME_BORDER_COLOR),
            mouse_cursor=ft.MouseCursor.CLICK,
        ),
        on_click=cerrar_modal,
    )

    # --- Ensamblado ---
    cuerpo = ft.Column(
        controls=[
            mensaje,
            ft.Container(expand=True),
            ft.Row(
                controls=[eliminar_btn, cancelar_btn],
                alignment=ft.MainAxisAlignment.END,
            ),
        ],
        expand=True,
    )

    contenido = ft.Column(
        controls=[
            header,
            ft.Container(
                content=cuerpo,
                padding=ft.Padding(20, 20, 20, 20),
                expand=True,
            ),
        ],
    )

    modal_confirmacion = ft.AlertDialog(
        modal=True,
        bgcolor=THEME_CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            content=contenido,
            width=page.width * 0.9 if is_mobile else 450,
            height=None if is_mobile else 280,
        ),
        content_padding=ft.Padding.all(0),
    )

    return modal_confirmacion
