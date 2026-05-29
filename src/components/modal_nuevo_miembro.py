# python
from datetime import datetime
import flet as ft
# local
from constants import *
from database_orm import Miembro, _leer_configuracion


def crear_modal_nuevo_miembro(page: ft.Page, session, on_guardar=None):
    """
    Crea y retorna un AlertDialog para inscribir un nuevo miembro.
    ---
    Entrada:
        page (ft.Page): Página de Flet.
        session (Session): Sesión activa de SQLAlchemy.
        on_guardar (callable, opcional): Callback al guardar (para refrescar la UI).
    Salida:
        ft.AlertDialog: Modal de nuevo miembro.
    """
    is_mobile = page.width is not None and page.width < 600

    # --- Header del modal (unificado) ---
    header = ft.Container(
        content=ft.Text(
            "Nuevo Miembro",
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
        modal_nuevo.open = False
        page.update()

    # --- Validación: permite solo números enteros ---
    def _validar_entero(e):
        limpio = ''.join(c for c in e.control.value if c.isdigit())
        if limpio != e.control.value:
            e.control.value = limpio
            e.control.update()

    # --- Campos de entrada ---
    nombre_field = ft.TextField(
        label="Nombre del miembro",
        border_color=THEME_BORDER_COLOR,
        focused_border_color=THEME_TEAL,
        color=THEME_TEXT_PRIMARY,
    )

    prueba_field = ft.TextField(
        label="Tiempo de prueba (días)",
        value=_leer_configuracion("tiempo_prueba_dias", session, "7"),
        border_color=THEME_BORDER_COLOR,
        focused_border_color=THEME_TEAL,
        color=THEME_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*$", replacement_string=""),
        on_change=_validar_entero,
    )

    # --- Botones ---
    def guardar(e):
        nombre = nombre_field.value.strip()
        if not nombre:
            return

        m = Miembro(
            nombre=nombre,
            fecha_registro=datetime.now(),
            es_prueba=True,
            tiempo_prueba_dias=int(prueba_field.value or 0),
        )
        session.add(m)
        session.commit()
        cerrar_modal(e)
        if on_guardar:
            on_guardar()

    guardar_btn = ft.FilledButton(
        content=ft.Text("Guardar"),
        bgcolor=THEME_TEAL,
        color=THEME_TEAL_TEXT,
        style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
        on_click=guardar,
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

    # --- Cuerpo del modal ---
    campos = ft.Column(
        controls=[
            nombre_field,
            ft.Container(height=15),
            prueba_field,
            ft.Container(expand=True),
            ft.Row(
                controls=[guardar_btn, cancelar_btn],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        expand=True,
    )

    contenido = ft.Column(
        controls=[
            header,
            ft.Container(
                content=campos,
                padding=ft.Padding(20, 20, 20, 20),
                expand=True,
            ),
        ],
    )

    modal_nuevo = ft.AlertDialog(
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

    return modal_nuevo
