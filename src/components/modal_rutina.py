# python
import flet as ft
import calendar as cal
from datetime import date, datetime
from constants import *
from database_orm import Cronograma

DIAS_CORTOS = ["Lun", "mar", "mie", "jue", "vie", "sab", "dom"]
DIAS_COMPLETOS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def crear_modal_rutina(nombre_miembro: str, page: ft.Page, session, miembro_id: int, on_guardar=None):
    is_mobile = page.width is not None and page.width < 600
    today = date.today()

    # ── Estado mutable ──────────────────────────────────────────
    state = {
        "year": today.year,
        "month": today.month,
        "selected_dates": set(),
        "existing_weekdays": set(),
        "existing_dates": set(),
    }

    # ── Helpers de BD ───────────────────────────────────────────
    def _cargar_rutinas():
        return session.query(Cronograma).filter_by(miembro_id=miembro_id).all()

    for r in _cargar_rutinas():
        if r.repetir_semanal:
            state["existing_weekdays"].add(r.dia_semana)
        elif r.fecha is not None:
            state["existing_dates"].add(r.fecha.date() if isinstance(r.fecha, datetime) else r.fecha)

    # ── Header ───────────────────────────────────────────────────
    header = ft.Container(
        content=ft.Text(
            f"Rutina de {nombre_miembro}",
            size=14, weight="bold",
            color=THEME_TEXT_PRIMARY,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=THEME_HEADER_BG_MODAL,
        padding=ft.Padding(20, 14, 20, 14),
        alignment=ft.Alignment.CENTER,
        border_radius=ft.BorderRadius.only(top_left=12, top_right=12),
    )

    # ── Contenedores mutables ───────────────────────────────────
    cal_container = ft.Container(expand=True)
    rutinas_lista = ft.Container()

    # ── Construir calendario ────────────────────────────────────
    def _construir_calendario():
        year = state["year"]
        month = state["month"]
        selected = state["selected_dates"]
        existing_wd = state["existing_weekdays"]
        existing_dt = state["existing_dates"]

        first_wd, num_days = cal.monthrange(year, month)

        prev_btn = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            icon_color=THEME_TEXT_PRIMARY,
            icon_size=18,
            on_click=lambda e: _cambiar_mes(-1),
        )
        next_btn = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            icon_color=THEME_TEXT_PRIMARY,
            icon_size=18,
            on_click=lambda e: _cambiar_mes(1),
        )
        nav_row = ft.Row(
            controls=[
                prev_btn,
                ft.Text(
                    f"{MESES[month - 1]} {year}",
                    color=THEME_TEXT_PRIMARY,
                    size=15,
                    weight="bold",
                ),
                next_btn,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        cabecera = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        d, color=THEME_TEXT_SECONDARY, size=11,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                )
                for d in DIAS_CORTOS
            ],
        )

        cells = []
        for _ in range(first_wd):
            cells.append(None)
        for day in range(1, num_days + 1):
            cells.append(day)
        while len(cells) % 7 != 0:
            cells.append(None)

        rows = [cells[i:i + 7] for i in range(0, len(cells), 7)]

        cell_size = 34 if is_mobile else 38

        grid_rows = []
        for week in rows:
            week_cells = []
            for day_num in week:
                if day_num is None:
                    week_cells.append(
                        ft.Container(width=cell_size, height=cell_size)
                    )
                    continue

                d = date(year, month, day_num)
                wd = d.weekday()

                is_selected = d in selected
                has_routine = wd in existing_wd or d in existing_dt
                is_today_val = d == today

                if is_selected:
                    bg = THEME_TEAL
                    txt_color = THEME_TEAL_TEXT
                    borde = None
                elif has_routine:
                    bg = THEME_CARD_BG
                    txt_color = THEME_TEAL
                    borde = ft.Border(
                        top=ft.BorderSide(2, THEME_TEAL),
                        bottom=ft.BorderSide(2, THEME_TEAL),
                        left=ft.BorderSide(2, THEME_TEAL),
                        right=ft.BorderSide(2, THEME_TEAL),
                    )
                else:
                    bg = "#3A3D42"
                    txt_color = THEME_TEXT_PRIMARY
                    borde = None

                text_weight = "bold" if is_today_val else "normal"

                def _make_click(date_obj):
                    return lambda e: _toggle_day(date_obj)

                week_cells.append(
                    ft.Container(
                        content=ft.Text(
                            str(day_num),
                            color=txt_color,
                            size=12,
                            weight=text_weight,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        width=cell_size,
                        height=cell_size,
                        border_radius=6,
                        bgcolor=bg,
                        border=borde,
                        alignment=ft.Alignment.CENTER,
                        on_click=_make_click(d),
                    )
                )
            grid_rows.append(
                ft.Row(
                    controls=week_cells,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    spacing=0,
                )
            )

        cal_container.content = ft.Column(
            controls=[nav_row, cabecera] + grid_rows,
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _cambiar_mes(delta):
        new_month = state["month"] + delta
        new_year = state["year"]
        if new_month > 12:
            new_month = 1
            new_year += 1
        elif new_month < 1:
            new_month = 12
            new_year -= 1
        state["year"] = new_year
        state["month"] = new_month
        state["selected_dates"].clear()
        _construir_calendario()
        page.update()

    def _toggle_day(d):
        if d in state["selected_dates"]:
            state["selected_dates"].remove(d)
        else:
            state["selected_dates"].add(d)
        _construir_calendario()
        page.update()

    # ── Lista de rutinas existentes ──────────────────────────────
    def _eliminar_rutina(rutina_id):
        r = session.query(Cronograma).filter_by(id=rutina_id).first()
        if r:
            session.delete(r)
            session.commit()
        _actualizar_rutinas()
        page.update()

    def _construir_lista_rutinas():
        rutinas = _cargar_rutinas()
        if not rutinas:
            return ft.Text(
                "Sin rutinas registradas",
                size=13, color=THEME_TEXT_SECONDARY, italic=True,
            )

        items = []
        for r in rutinas:
            if r.repetir_semanal:
                dia_nombre = DIAS_COMPLETOS[r.dia_semana]
            elif r.fecha is not None:
                fecha_obj = r.fecha.date() if isinstance(r.fecha, datetime) else r.fecha
                dia_nombre = fecha_obj.strftime("%d %b %Y")
            else:
                dia_nombre = DIAS_COMPLETOS[r.dia_semana]
            desc = r.descripcion or "—"
            items.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                f"{dia_nombre}  ·  {desc}",
                                color=THEME_TEXT_PRIMARY,
                                size=13,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=ft.Colors.RED_400,
                                icon_size=16,
                                tooltip="Eliminar rutina",
                                on_click=lambda e, rid=r.id: _eliminar_rutina(rid),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor="#3A3D42",
                    border_radius=8,
                    padding=ft.Padding(10, 8, 4, 8),
                    margin=ft.Margin.only(bottom=4),
                )
            )
        return ft.Column(controls=items, spacing=0, scroll=ft.ScrollMode.AUTO)

    def _actualizar_rutinas():
        state["existing_weekdays"].clear()
        state["existing_dates"].clear()
        for r in _cargar_rutinas():
            if r.repetir_semanal:
                state["existing_weekdays"].add(r.dia_semana)
            elif r.fecha is not None:
                state["existing_dates"].add(r.fecha.date() if isinstance(r.fecha, datetime) else r.fecha)
        rutinas_lista.content = _construir_lista_rutinas()
        _construir_calendario()

    # ── Descripción ──────────────────────────────────────────────
    descripcion_field = ft.TextField(
        label="Descripción",
        border_color=THEME_BORDER_COLOR,
        focused_border_color=THEME_TEAL,
        color=THEME_TEXT_PRIMARY,
        label_style=ft.TextStyle(color=THEME_TEXT_SECONDARY),
        cursor_color=THEME_TEAL,
        max_length=200,
        multiline=True,
        min_lines=1,
        max_lines=3,
        expand=True,
    )

    # ── Checkbox ─────────────────────────────────────────────────
    repetir_check = ft.Checkbox(
        label="Repetir semanalmente",
        value=True,
        fill_color=THEME_TEAL,
        check_color=THEME_TEAL_TEXT,
        label_style=ft.TextStyle(color=THEME_TEXT_PRIMARY, size=13),
    )

    # ── Cerrar ───────────────────────────────────────────────────
    def cerrar_modal(e=None):
        modal_rutina.open = False
        page.update()

    # ── Guardar ──────────────────────────────────────────────────
    def _guardar(e):
        if not state["selected_dates"]:
            return
        descripcion = (descripcion_field.value or "").strip()
        repetir = repetir_check.value

        for d in state["selected_dates"]:
            dia_semana = d.weekday()
            if repetir:
                existente = session.query(Cronograma).filter_by(
                    miembro_id=miembro_id, dia_semana=dia_semana, repetir_semanal=True,
                ).first()
                if existente:
                    existente.descripcion = descripcion
                else:
                    session.add(Cronograma(
                        miembro_id=miembro_id, dia_semana=dia_semana,
                        descripcion=descripcion, repetir_semanal=True,
                    ))
            else:
                fecha_dt = datetime.combine(d, datetime.min.time())
                existente = session.query(Cronograma).filter_by(
                    miembro_id=miembro_id, fecha=fecha_dt, repetir_semanal=False,
                ).first()
                if existente:
                    existente.descripcion = descripcion
                else:
                    session.add(Cronograma(
                        miembro_id=miembro_id, dia_semana=dia_semana,
                        fecha=fecha_dt, descripcion=descripcion, repetir_semanal=False,
                    ))
        session.commit()
        cerrar_modal()
        if on_guardar:
            on_guardar()

    cancelar_btn = ft.OutlinedButton(
        content=ft.Text("Cancelar"),
        style=ft.ButtonStyle(
            color=THEME_TEXT_PRIMARY,
            side=ft.BorderSide(1, THEME_BORDER_COLOR),
            mouse_cursor=ft.MouseCursor.CLICK,
        ),
        on_click=lambda e: cerrar_modal(),
    )

    guardar_btn = ft.FilledButton(
        content=ft.Text("Guardar"),
        bgcolor=THEME_TEAL,
        color=THEME_TEAL_TEXT,
        style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
        on_click=_guardar,
    )

    # ── Construir bloques ────────────────────────────────────────
    _construir_calendario()
    rutinas_lista.content = _construir_lista_rutinas()

    bloque_calendario = ft.Container(
        content=cal_container,
        padding=ft.Padding(12, 8, 12, 8),
        bgcolor=THEME_CARD_BG,
        border_radius=12,
    )

    bloque_central = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Rutinas actuales:", size=13, weight="bold",
                    color=THEME_TEXT_PRIMARY,
                ),
                rutinas_lista,
                ft.Container(
                    content=ft.Column(
                        controls=[descripcion_field, repetir_check],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
            ],
            spacing=8,
        ),
    )

    bloque_botones = ft.Container(
        content=ft.Row(
            controls=[guardar_btn, cancelar_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.Padding.only(top=4),
    )

    contenido_principal = ft.Column(
        controls=[
            header,
            ft.Container(
                content=ft.Column(
                    controls=[bloque_calendario, bloque_central, bloque_botones],
                    spacing=12,
                ),
                padding=ft.Padding(16, 12, 16, 16),
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    ancho_modal = page.width * 0.95 if is_mobile else 800

    modal_rutina = ft.AlertDialog(
        modal=True,
        bgcolor=THEME_CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            content=contenido_principal,
            width=ancho_modal,
        ),
        content_padding=ft.Padding.all(0),
    )

    return modal_rutina
