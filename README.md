# 🏨 Hotel Pacific Reef – Sistema de Reservas (Django)

Aplicación web desarrollada en **Django** para gestionar **búsqueda de disponibilidad**, **reservas con persistencia en BD (SQLite)**, **cálculo de total y anticipo (30%)**, **pago simulado** y **panel de gestión para staff**.

---

## 🚀 Versión 1.0 – Prototipo funcional
Primera entrega operativa enfocada en cubrir la **rúbrica de prototipo**: flujo completo integrado a BD y evidencias básicas.

### 📋 Inclusiones clave
- 🔎 **Catálogo** por fechas/huéspedes con verificación de **disponibilidad**.
- 🛏️ **Detalle** de habitación con imágenes.
- 🧾 **Checkout** con validaciones (fechas, capacidad, disponibilidad).
- 💰 **Cálculo de total** (`noches × tarifa`) y **anticipo 30%** en confirmación.
- 💳 **Pago simulado**: cambia estado de la reserva a `paid`.
- 🗂️ **Panel Staff** con listado de reservas, montos y estado.
- 💾 **Persistencia real** en `db.sqlite3` (SQLite).
- 🇨🇱 Formato CLP con `django.contrib.humanize`.

---

## 🛠️ Tecnologías utilizadas
- **Python 3.10+**
- **Django 4.x**
- **SQLite** (por defecto)
- **Pillow** (imágenes)
- **django.contrib.humanize** (formato miles CLP)
- HTML/CSS con templates de Django

---

## ✨ Características principales
- **Disponibilidad sin traslapes** para la misma habitación.
- **Capacidad** respetada por tipo de habitación.
- **Cálculo de negocio en el modelo** (propiedades útiles como `nights`, `deposit_30`).
- **Autenticación Staff** (protección del panel interno).
- **Estructura limpia**: modelos simples, vistas claras, templates ordenados.

---

## 📱 Páginas incluidas
- **Home**: buscador de fechas y huéspedes.
- **Catálogo**: habitaciones disponibles según rango/huéspedes.
- **Detalle**: información e imágenes; CTA reservar.
- **Checkout**: formulario titular + resumen (noches, total estimado).
- **Confirmación**: total + anticipo 30%; acceso a pago simulado.
- **Pago**: marca la reserva como `paid`.
- **Panel Staff**: reservas recientes con montos y estado.

---

## 🗄️ Modelo de datos 
**Room**  
`name`, `category`, `capacity`, `price_per_night`, `description`, `is_active`  
Métodos: `is_available(check_in, check_out)`

**RoomImage**  
`room(FK)`, `image` *(opcional)*, `image_url` *(opcional)*

**Reservation**  
`room(FK)`, `check_in`, `check_out`, `guests`, `holder_name`, `holder_email`,  
`total_amount`, `payment_status (pending|paid|cancelled)`, `created_at`  
Props: `nights`, `deposit_30 (= total_amount * 0.30)`

---

## ⚖️ Reglas de negocio
- **Disponibilidad**: no se permite reservar si existen traslapes.
- **Total**: `noches × price_per_night` → persistido en `total_amount`.
- **Anticipo 30%**: visible en confirmación (no altera el total).
- **Capacidad**: `guests ≤ room.capacity`.
- **Pago simulado**: actualiza `payment_status = 'paid'`.

---

## ▶️ Cómo correr el proyecto (local)
```bash
# 1) entorno y dependencias
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# 2) migraciones y usuario admin
python manage.py migrate
python manage.py createsuperuser

# 3) ejecutar
python manage.py runserver



## 👥 Créditos

Duoc UC – PRY3211 Ingeniería de Software
Equipo: Fabrizio J. Bugedo (+ coequipo). Uso educativo.
