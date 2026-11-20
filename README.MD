# La Estancia — Sistema de Gestión

Sistema de gestión para una casa de asistencia al adulto mayor
El proyecto tiene como objetivo proporcionar una interfaz gráfica para gestionar información relacionada con:

- Residentes
- Historial clínico
- Suministros e insumos
- Movimientos de inventario
- Consultas
- Inicio de sesión

El sistema está desarrollado en Python utilizando Tkinter para la interfaz gráfica y cuenta con una base de datos diseñada en MySQL.

---

### INTEGRANTES

| N° | Nombre completo | Rol | Usuario de GitHub |
|---|---|---|---|
| 1 | Deivid Jesep Mallea | product owner/developer | josepmallea62 |
| 2 | Pablo Mateo Camacho Gonzales | lider de documento/developer| thmtx |
| 3 | Diego Cutilli Condori | scrum master/developer| dcutilli123456789 |
| 4 | Jhanio Raul Suxo | developer | jhanniorm0104 |

# 🛠️ Tecnologías utilizadas

| Tecnología | Versión / información |
|---|---|
| Python | **3.14** |
| Tkinter | Incluido con Python |
| MySQL | Base de datos utilizada |
| Git | Control de versiones |
| GitHub | Repositorio del proyecto |

> La versión de Python utilizada en el proyecto corresponde a **Python 3.14**. El archivo `__pycache__/login.cpython-314.pyc` confirma el entorno CPython 3.14 utilizado.

---

# Requerimientos

Antes de ejecutar el proyecto es necesario tener instalado:

### Software

- **Python 3.14**
- **MySQL**
- **Git**
- **GitHub** para acceder al repositorio

### Comprobar Python

Abrir CMD o una terminal y ejecutar:

```bash
python --version
```

Debe aparecer una versión correspondiente a:

```text
Python 3.14
```

### Comprobar Git

```bash
git --version
```

### Comprobar MySQL

```bash
mysql --version
```

> El proyecto utiliza MySQL Workbench 8.0.47.

---

# Copiar el repositorio

## 1. Instalar Git

Si Git todavía no está instalado, instalarlo desde su sitio oficial.

Después de instalarlo, abrir **CMD**, PowerShell o Git Bash.

## 2. Clonar el repositorio

Utilizar el comando:

```bash
git clone https://github.com/dcutili123456789-debug/LOS-SIX-SEVEN
```

## 3. Entrar a la carpeta del proyecto

```bash
cd LOS-SIX-SEVEN
```

También se puede comprobar que los archivos fueron copiados correctamente con:

```bash
dir
```

En la carpeta del proyecto deben encontrarse los archivos de Python, entre ellos:

```text
consultas.py
historial.py
laestacion.py
login.py
movimiento.py
residentes .py
suministros.py
```

---

# Preparación de Python

El proyecto utiliza principalmente módulos incluidos en Python, por lo que no se requiere instalar mediante `pip` una biblioteca adicional para la interfaz.

El módulo utilizado para la interfaz gráfica es:

```python
import tkinter as tk
```

También se utiliza:

```python
from tkinter import ttk
```

Tkinter forma parte de la instalación estándar de Python.

Para comprobar que Tkinter está disponible:

```bash
python -m tkinter
```

Si la instalación es correcta, se abrirá una ventana de prueba de Tkinter.

---

# Instalación de la base de datos

La base de datos del proyecto se encuentra en la carpeta:

```text
Base_de_datos
```

Contiene tres archivos principales:

```text
Integridad de la base de datos
Primera versión_de_la_base_de_datos
Segunda_version_base_de_datos
```

Estos archivos deben ejecutarse **en orden**.

---

## 1. Crear la base de datos

Primero abrir MySQL.

Desde MySQL:

```bash
mysql -u root -p
```

Después ejecutar el contenido de:

```text
Primera versión_de_la_base_de_datos
```

Este archivo crea la base:

```sql
CREATE DATABASE gestion_tercera_edad;
```

y posteriormente crea las tablas iniciales.

La estructura incluye tablas como:

- `Residente`
- `Historial`
- `Categoria`
- `Proveedor`
- `Insumo`
- `Medicamento`
- `Lote`
- `Prescripcion`
- `Movimiento`

---

# 2. Aplicar la segunda versión

Una vez creada la estructura inicial, ejecutar el archivo:

```text
Segunda_version_base_de_datos
```

Este archivo modifica y amplía la estructura existente.

Entre los cambios realizados se encuentran:

- Creación de la tabla `Usuario`.
- Incorporación del CI del residente.
- Incorporación de apellidos.
- Incorporación del sexo.
- Incorporación de la fecha de ingreso.
- Incorporación del contacto familiar.
- Incorporación del responsable en el historial.
- Incorporación de frecuencia en las prescripciones.
- Incorporación de descripción para los insumos.
- Incorporación del número de lote.
- Incorporación de observaciones en los movimientos.
- Incorporación de restricciones `UNIQUE`.
- Incorporación de restricciones `CHECK`.
- Incorporación de relaciones mediante claves foráneas.

---

# 3. Aplicar las reglas de integridad

Finalmente ejecutar:

```text
Integridad de la base de datos
```

Este archivo agrega restricciones para garantizar la consistencia de los datos.

Por ejemplo:

- Validación de fechas de nacimiento.
- Validación de fechas de ingreso.
- Validación de nombres.
- Validación del CI.
- Validación del responsable del historial.
- Validación de usuarios.
- Validación de contraseñas almacenadas como hash de 64 caracteres.
- Validación de proveedores.
- Validación del stock mínimo.
- Validación de nombres de insumos.
- Restricciones para evitar duplicados.

---

# Orden de instalación de la base de datos

Es importante respetar este orden:

```text
Primera versión_de_la_base_de_datos
                ↓
Segunda_version_base_de_datos
                ↓
Integridad de la base de datos
```

No se recomienda ejecutar los archivos en un orden diferente porque la segunda versión y las reglas de integridad dependen de la estructura creada anteriormente.

---

# Estructura principal de la base de datos

La base de datos utilizada por el proyecto se denomina:

```text
gestion_tercera_edad
```

Su estructura contiene diferentes entidades relacionadas:

```text
Residente
   │
   ├── Historial
   │
   └── Prescripcion
          │
          └── Medicamento
                 │
                 └── Insumo
                        │
                        └── Lote
                               │
                               └── Movimiento

Insumo ─── Categoria

Lote ─── Proveedor
```

Estas relaciones permiten organizar la información de los residentes, su historial clínico y la gestión de insumos y movimientos.

---

# Ejecución del programa

Después de clonar el repositorio, abrir una terminal dentro de la carpeta donde se encuentra `laestacion.py`.

Ejecutar:

```bash
python laestacion.py
```

El programa inicia la aplicación:

```text
La Estancia - Sistema de gestión
```

y muestra la pantalla de inicio de sesión.

---

# Inicio de sesión

La aplicación contiene una pantalla inicial de inicio de sesión.

Permite ingresar:

- Usuario
- Contraseña

La interfaz cuenta con un botón:

```text
Ingresar
```

Actualmente, la función de ingreso obtiene los datos introducidos mediante:

```python
usuario = entrada_usuario.get()
contrasena = entrada_contrasena.get()
```

La validación contra la base de datos está preparada como una funcionalidad pendiente.

---

# Módulos del sistema

## Residentes

Permite introducir información relacionada con los residentes.

Los campos implementados son:

| Campo | Descripción |
|---|---|
| CI | Cédula de identidad |
| Nombre(s) | Nombre del residente |
| Apellido(s) | Apellidos |
| Fecha de nacimiento | Fecha de nacimiento |
| Sexo | Femenino / Masculino |
| Fecha de ingreso | Fecha de ingreso a la institución |
| Contacto familiar | Nombre y teléfono del contacto |

Cuenta con las opciones:

```text
Registrar
Consultar
```

---

## Historial clínico

Permite registrar información relacionada con el historial médico del residente.

Los campos implementados son:

| Campo | Descripción |
|---|---|
| Residente (CI) | CI del residente |
| Fecha de registro | Fecha del registro |
| Patología | Patología registrada |
| Evolución | Evolución del paciente |
| Medicamento | Medicamento utilizado |
| Dosis | Dosis indicada |
| Frecuencia | Frecuencia de administración |
| Responsable | Médico o enfermero/a responsable |

Cuenta con:

```text
Registrar
Consultar
```

---

## Suministros

Permite gestionar información relacionada con medicamentos e insumos.

Los campos implementados son:

| Campo | Descripción |
|---|---|
| Insumo / medicamento | Nombre del insumo |
| Descripción | Presentación, concentración o uso |
| Categoría | Categoría del producto |
| Proveedor | Proveedor |
| N.º de lote | Número de lote |
| Cantidad | Cantidad disponible |
| Fecha de vencimiento | Fecha de vencimiento |
| Stock mínimo | Cantidad mínima permitida |

Cuenta con:

```text
Registrar
Consultar
```

---

## Movimiento

Permite registrar movimientos de inventario.

Los campos implementados son:

| Campo | Descripción |
|---|---|
| Tipo | Entrada o salida |
| Insumo / medicamento | Producto involucrado |
| Lote | Lote correspondiente |
| Cantidad | Cantidad movilizada |
| Residente CI | CI del residente en caso de salida |
| Fecha | Fecha del movimiento |
| Observación / motivo | Información adicional |

Cuenta con:

```text
Registrar
Consultar
```

El tipo de movimiento está definido en la base de datos como:

```text
entrada
salida
```

---

## Consultas

El módulo de consultas permite seleccionar el área donde realizar la búsqueda:

```text
Residentes
Historial
Insumos
Movimientos
```

También dispone de un campo de búsqueda para criterios como:

```text
CI
Nombre
Lote
Fecha
```

Los resultados están preparados para mostrarse mediante una tabla.

Las columnas implementadas son:

| Columna |
|---|
| Nombre / Insumo |
| CI / Lote |
| Detalle |
| Tipo |
| Cantidad |
| Fecha |

---

# Estado de la programación

La siguiente tabla muestra el estado de las partes programadas actualmente:

| Parte | Estado | Descripción |
|---|---|---|
| Interfaz de inicio de sesión | 🟢 Implementado | Ventana con usuario, contraseña y botón de ingreso |
| Módulo Residentes | 🟢 Implementado | Formulario para registrar y consultar residentes |
| Módulo Historial | 🟢 Implementado | Formulario para registrar y consultar historial clínico |
| Módulo Suministros | 🟢 Implementado | Formulario para gestionar insumos y medicamentos |
| Módulo Movimiento | 🟢 Implementado | Formulario para registrar entradas y salidas |
| Módulo Consultas | 🟢 Implementado | Interfaz para seleccionar el área y realizar búsquedas |
| Navegación entre módulos | 🟢 Implementado | Integrada en `laestacion.py` mediante Tkinter |
| Cerrar sesión | 🟢 Implementado | Permite volver a la pantalla de inicio |
| Base de datos | 🟢 Diseñada | Estructura SQL desarrollada |
| Integridad de datos | 🟢 Implementado en SQL | Restricciones `CHECK`, `UNIQUE`, índices y claves foráneas |
| `INSERT` desde Python | 🟡 Pendiente | Los formularios indican dónde incorporar las operaciones INSERT |
| `SELECT` desde Python | 🟡 Pendiente | Las consultas indican dónde incorporar las operaciones SELECT |
| Conexión Python ↔ MySQL | 🟡 Pendiente | No se encuentra implementada en los archivos Python entregados |
| Validación del login contra MySQL | 🟡 Pendiente | Actualmente se obtienen los datos introducidos y se imprimen |
| CRUD completo | 🟡 Pendiente | La interfaz está preparada, pero falta conectar las operaciones con la base |

---

# Archivos principales del programa

| Archivo | Función |
|---|---|
| `laestacion.py` | Archivo principal e integración de los módulos |
| `login.py` | Interfaz de inicio de sesión |
| `residentes .py` | Módulo de registro y consulta de residentes |
| `historial.py` | Módulo de historial clínico |
| `suministros.py` | Módulo de suministros |
| `movimiento.py` | Módulo de movimientos |
| `consultas.py` | Módulo de consultas |

---

# Integración del sistema

La estructura principal del programa se encuentra en:

```text
laestacion.py
```

Este archivo importa los diferentes módulos:

```python
from residentes import Residentes
from historial import Historial
from suministros import Suministros
from movimiento import Movimiento
from consultas import Consultas
```

Posteriormente los módulos son integrados en una única aplicación mediante Tkinter.

La navegación se realiza mediante una barra lateral:

```text
┌─────────────────────┐
│     La Estancia     │
│  Sistema de gestión │
│                     │
│    Residentes       │
│    Historial        │
│    Suministros      │
│    Movimiento       │
│    Consultas        │
│                     │
│    Cerrar sesión    │
└─────────────────────┘
```

---

# Estado actual del proyecto

El proyecto cuenta con una interfaz gráfica funcional y una estructura de base de datos definidA.

La interfaz contiene los formularios correspondientes a los principales módulos del sistema y la base de datos contiene las tablas, relaciones y restricciones necesarias para almacenar la información.

La siguiente etapa consiste en conectar los formularios de Python con MySQL, sustituyendo las funciones actualmente preparadas con comentarios como:

```python
# aquí va el INSERT
```

y:

```python
# aquí va el SELECT
```

por las operaciones correspondientes de la base de datos.

---