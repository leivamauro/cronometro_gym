# python
from datetime import datetime
import flet as ft
# locales
from constants import *
from database_orm import (
    Miembro, HistorialPago,
    _estado_semaforo, _ultimo_pago,
    _calcular_vencimiento, _dias_restantes, _dias_pasados,
    _leer_configuracion,
)


def crear_modal_detalles(nombre_miembro: str, page: ft.Page, session, miembro_id: int):
    """
    Crea un AlertDialog con los detalles reales del miembro desde la BD.
    ---
    Entrada:
        nombre_miembro (str): Nombre del miembro.
        page (ft.Page): Página de Flet.
        session (Session): Sesión activa de SQLAlchemy.
        miembro_id (int): ID del miembro en la BD.
    Salida:
        ft.AlertDialog: Modal de detalles del miembro.
    """
    is_mobile = page.width is not None and page.width < 600

    # Cargar datos reales del miembro desde la BD
    miembro = session.query(Miembro).filter_by(id=miembro_id).first()
    if miembro is None:
        return None

    estado = _estado_semaforo(miembro, session)
    ultimo_pago = _ultimo_pago(miembro_id, session)
    precio = float(_leer_configuracion("precio_mensual", session, "3000"))

    # --- Header del modal (unificado) ---
    header = ft.Container(
        content=ft.Text(
            f"Detalles del Miembro - {nombre_miembro}",
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
        modal_detalles.open = False
        page.update()

    cancelar_btn = ft.OutlinedButton(
        content=ft.Text("Cancelar"),
        style=ft.ButtonStyle(
            color=THEME_TEXT_PRIMARY,
            side=ft.BorderSide(1, THEME_BORDER_COLOR),
            mouse_cursor=ft.MouseCursor.CLICK,
        ),
        on_click=cerrar_modal,
    )

    # --- Texto de estado y colores ---
    if estado == "vencido":
        texto_estado = "Vencido (Rojo)"
        color_estado = ft.Colors.RED
    elif estado == "en_prueba":
        texto_estado = "En período de prueba (Amarillo)"
        color_estado = ft.Colors.YELLOW
    else:
        texto_estado = "Al día (Verde)"
        color_estado = ft.Colors.GREEN

    # --- Último pago formateado ---
    if ultimo_pago:
        texto_ultimo_pago = (
            f"Último Pago: {ultimo_pago.fecha_pago.strftime('%d/%m/%Y')} "
            f"(${ultimo_pago.monto:.0f})"
        )
    else:
        texto_ultimo_pago = "Último Pago: Sin pagos"

    # --- Líneas dinámicas de deuda / días ---
    lineas_deuda = []
    if estado == "vencido":
        meses = _calcular_vencimiento(miembro, session)
        deuda = meses * precio
        dias = _dias_pasados(miembro, session)
        lineas_deuda.append(
            ft.Text(f"Debe {meses} meses (${deuda:.0f})", color=ft.Colors.RED, size=14)
        )
        lineas_deuda.append(
            ft.Text(f"Vencido hace {dias} días", color=ft.Colors.RED, size=14)
        )
    else:
        dias = _dias_restantes(miembro, session)
        lineas_deuda.append(
            ft.Text(f"Vence en {dias} días", color=color_estado, size=14)
        )

    # --- Columna Izquierda: Información Detallada ---
    columna_izquierda = ft.Column(
        controls=[
            ft.Text("Información Detallada", size=18, color=THEME_TEXT_PRIMARY),
            ft.Container(height=5),
            ft.Text(f"Nombre: {nombre_miembro}", color=THEME_TEXT_PRIMARY, size=15),
            ft.Text(
                f"Fecha Registro: {miembro.fecha_registro.strftime('%d/%m/%Y')}",
                color=THEME_TEXT_PRIMARY, size=15,
            ),
            ft.Text(texto_ultimo_pago, color=THEME_TEXT_PRIMARY, size=15),
            ft.Row(
                controls=[
                    ft.Container(
                        width=14, height=14, border_radius=7,
                        bgcolor=color_estado,
                    ),
                    ft.Text(f"Estado actual: {texto_estado}",
                            color=THEME_TEXT_PRIMARY, size=15),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            *lineas_deuda,
        ],
        spacing=8,
    )

    # --- Columna Derecha: Últimos 12 pagos desde la BD ---
    pagos = (
        session.query(HistorialPago)
        .filter_by(miembro_id=miembro_id)
        .order_by(HistorialPago.fecha_pago.desc())
        .limit(12)
        .all()
    )

    tabla_cabecera = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Fecha", weight="bold", color=THEME_TEXT_PRIMARY, width=80, text_align="center"),
                ft.Text("|", color=THEME_BORDER_COLOR),
                ft.Text("Monto", weight="bold", color=THEME_TEXT_PRIMARY, width=70, text_align="center"),
                ft.Text("|", color=THEME_BORDER_COLOR),
                ft.Text("Meses", weight="bold", color=THEME_TEXT_PRIMARY, width=50, text_align="center"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border=ft.Border.only(bottom=ft.BorderSide(1, THEME_BORDER_COLOR)),
        padding=ft.Padding.only(bottom=10),
    )

    filas_historial = []
    for pago in pagos:
        monto_texto = f"${pago.monto:.0f}" if pago.monto == int(pago.monto) else f"${pago.monto:.2f}"
        fila = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(pago.fecha_pago.strftime('%d/%m/%Y'),
                            color=THEME_TEXT_PRIMARY, width=80, text_align="center"),
                    ft.Text("|", color=THEME_BORDER_COLOR),
                    ft.Text(monto_texto, color=THEME_TEXT_PRIMARY, width=70, text_align="center"),
                    ft.Text("|", color=THEME_BORDER_COLOR),
                    ft.Text(f"{pago.meses_abonados} {'mes' if pago.meses_abonados == 1 else 'meses'}",
                            color=THEME_TEXT_PRIMARY, width=50, text_align="center"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            border=ft.Border.only(bottom=ft.BorderSide(1, THEME_BORDER_COLOR)),
            padding=ft.Padding.symmetric(vertical=10),
        )
        filas_historial.append(fila)

    # Si no hay pagos, mostrar mensaje en lugar de tabla vacía
    if not filas_historial:
        filas_historial.append(
            ft.Container(
                content=ft.Text("Sin historial de pagos",
                                color=THEME_TEXT_SECONDARY, size=14, italic=True),
                padding=ft.Padding.symmetric(vertical=20),
                alignment=ft.Alignment.CENTER,
            )
        )

    if is_mobile:
        columna_derecha = ft.Column(
            controls=[
                ft.Text("Historial de Pagos", size=18, color=THEME_TEXT_PRIMARY),
                ft.Container(height=5),
                tabla_cabecera,
                ft.Column(controls=filas_historial, scroll=ft.ScrollMode.AUTO, spacing=0),
                ft.Container(expand=True),
                ft.Row(controls=[ft.Container(expand=True), cancelar_btn]),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=8,
        )

        ancho_modal = page.width * 0.9 if page.width else None

        contenido = ft.Column(
            controls=[
                header,
                ft.Container(content=columna_izquierda, padding=ft.Padding(20, 20, 20, 10)),
                ft.Container(content=columna_derecha, padding=ft.Padding(20, 10, 20, 20)),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    else:
        columna_derecha = ft.Column(
            controls=[
                ft.Text("Historial de Pagos", size=18, color=THEME_TEXT_PRIMARY),
                ft.Container(height=5),
                tabla_cabecera,
                ft.Column(controls=filas_historial, scroll=ft.ScrollMode.AUTO, expand=True, spacing=0),
                ft.Row(controls=[ft.Container(expand=True), cancelar_btn]),
            ],
            spacing=8,
        )

        contenido = ft.Column(
            controls=[
                header,
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(content=columna_izquierda,
                                         padding=ft.Padding(20, 20, 20, 20),
                                         expand=True),
                            ft.VerticalDivider(width=1, color=THEME_BORDER_COLOR),
                            ft.Container(content=columna_derecha,
                                         padding=ft.Padding(20, 20, 20, 20),
                                         expand=True),
                        ],
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
        )

    modal_detalles = ft.AlertDialog(
        modal=True,
        bgcolor=THEME_CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            content=contenido,
            width=ancho_modal if is_mobile else 700,
            height=None if is_mobile else 380,
        ),
        content_padding=ft.Padding.all(0),
    )

    return modal_detalles
