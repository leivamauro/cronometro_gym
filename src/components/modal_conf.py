# python
import flet as ft
# local
from constants import *
from database_orm import _leer_configuracion, _guardar_configuracion


def crear_modal_conf(page: ft.Page, session):
    is_mobile = page.width is not None and page.width < 600

    # --- Header del modal (unificado con modal_pago) ---
    header = ft.Container(
        content=ft.Text(
            "Configuración",
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
        modal_conf.open = False
        page.update()

    # --- Validación: permite solo dígitos y un punto decimal (máx 2 decimales) ---
    def _validar_decimal(e):
        valor = e.control.value
        # Conservar solo números y el primer punto
        limpio = ''.join(c for c in valor if c.isdigit() or c == '.')
        if limpio.count('.') > 1:
            partes = limpio.split('.')
            limpio = partes[0] + '.' + ''.join(partes[1:])
        # Máximo 2 decimales
        if '.' in limpio:
            entero, decimal = limpio.split('.')
            limpio = entero + '.' + decimal[:2]
        if limpio != valor:
            e.control.value = limpio
            e.control.update()

    # --- Campos de entrada (precargados desde la BD) ---
    precio_field = ft.TextField(
        label="Precio mensual",
        value=_leer_configuracion("precio_mensual", session, "3000"),
        border_color=THEME_BORDER_COLOR,
        focused_border_color=THEME_TEAL,
        color=THEME_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d{0,2}$", replacement_string=""),
        on_change=_validar_decimal,
    )

    # --- Validación: permite solo números enteros ---
    def _validar_entero(e):
        limpio = ''.join(c for c in e.control.value if c.isdigit())
        if limpio != e.control.value:
            e.control.value = limpio
            e.control.update()

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
    def guardar_config(e):
        _guardar_configuracion("precio_mensual", precio_field.value, session)
        _guardar_configuracion("tiempo_prueba_dias", prueba_field.value, session)
        cerrar_modal(e)

    guardar_btn = ft.FilledButton(
        content=ft.Text("Guardar"),
        bgcolor=THEME_TEAL,
        color=THEME_TEAL_TEXT,
        style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
        on_click=guardar_config,
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
            precio_field,
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

    modal_conf = ft.AlertDialog(
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

    return modal_conf
