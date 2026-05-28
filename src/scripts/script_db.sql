-- 1. Tabla de Configuración Global(Llave-Valor)
CREATE TABLE configuracion(
    clave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
)

-- 2. Tabla de Miembros(Modificada)
CREATE TABLE miembros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    fecha_registro DATE NOT NULL,      -- Crucial para calcular el fin de la prueba
    fecha_vencimiento DATE,             -- Se actualiza con cada pago
    es_prueba INTEGER DEFAULT 1 -- 1=En prueba, 0=Socio Activo
)

-- 3. Tabla de Historial de Pagos
CREATE TABLE historial_pagos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    miembro_id INTEGER NOT NULL,
    fecha_pago DATE NOT NULL,
    monto REAL NOT NULL,
    meses_abonados INTEGER DEFAULT 1,
    FOREIGN KEY(miembro_id) REFERENCES miembros(id)
);