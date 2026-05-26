# Taller 08 — Integración de datos y ORM

## Descripción
Integración de datos desde un archivo CSV hacia una base de datos
relacional (SQLite o MySQL) usando SQLAlchemy ORM en Python,
con visualización en Streamlit.

---

## Estructura del proyecto

```
data/
├── jugadores_futbol.csv   # fuente de datos
├── config.py              # configuración de la base de datos
├── genera_tablas.py       # define las entidades y crea las tablas
├── poblar_bd.py           # migra los datos del CSV a la BD
├── app.py                 # frontend Streamlit
├── requirements.txt       # dependencias
└── README.md
```

---

## Entidades creadas

### Continente
| Campo  | Tipo        |
|--------|-------------|
| id     | Integer PK  |
| nombre | String(100) |

### Pais
| Campo         | Tipo               |
|---------------|--------------------|
| id            | Integer PK         |
| nombre        | String(100)        |
| continente_id | FK → continente.id |

### Jugador
| Campo                     | Tipo             |
|---------------------------|------------------|
| id                        | Integer PK       |
| nombre                    | String(200)      |
| posicion                  | String(100)      |
| edad                      | Integer          |
| numero_partidos_seleccion | Integer          |
| goles_seleccion           | Integer          |
| pais_nacimiento_id        | FK → pais.id     |
| pais_donde_juega_id       | FK → pais.id     |

---

## Instalación de dependencias

```powershell
pip install -r requirements.txt
```

---

## Configuración de la base de datos (`config.py`)

El único archivo que cambia según el gestor es `config.py`.
Los demás scripts funcionan igual sin modificación.

### Opción 1 — SQLite (activo por defecto)
No requiere servidor. La base de datos se crea automáticamente
como archivo `paises.db` en la misma carpeta.

```python
cadena_base_datos = 'sqlite:///paises.db'
# cadena_base_datos = 'mysql+pymysql://emiliojosepe777@localhost/paises'
```

### Opción 2 — MySQL
Requiere MySQL Server instalado. La base de datos `paises`
se crea automáticamente al correr `genera_tablas.py`.

```python
# cadena_base_datos = 'sqlite:///paises.db'
cadena_base_datos = 'mysql+pymysql://root:emiliojosepe777@localhost/paises'
```

---

## Orden de ejecución

```powershell
python genera_tablas.py   # crea las tablas en la base de datos
python poblar_bd.py       # migra los 1000 jugadores del CSV
streamlit run app.py      # lanza el frontend en localhost:8501
```

---

## Frontend (Streamlit)

La app presenta 3 tablas:

**Tabla 1 — Jugadores**
Muestra todos los jugadores con: nombre, país de nacimiento,
país donde juega, posición, edad, partidos selección,
goles selección y continente.

**Tabla 2 — Resumen por Continente**
Por cada continente: número de jugadores y total de goles.

**Tabla 3 — Resumen por País**
Por cada país: continente, número de jugadores y total de goles.

---

## Evidencias

### SQLite — DB Browser
Base de datos `paises.db` con 1000 jugadores cargados,
visualizada en DB Browser for SQLite.

<img width="1790" height="1149" alt="image" src="https://github.com/user-attachments/assets/3732d82d-01c9-4760-a625-4c34ad0df9d9" />

### MySQL — Terminal
Base de datos `paises` creada automáticamente en MySQL Server,
con las 3 tablas: `continente`, `pais`, `jugador`.

<img width="1698" height="1108" alt="image" src="https://github.com/user-attachments/assets/8789e8c7-84b4-4a2f-80e3-4c1248eed4cf" />

### Frontend Streamlit
App corriendo en `localhost:8501` con las 3 tablas solicitadas.

<img width="1859" height="1129" alt="image" src="https://github.com/user-attachments/assets/1e144003-31dc-43db-b994-f93c06519492" />

---

## Datos cargados

| Entidad    | Registros |
|------------|-----------|
| Continente | 5         |
| País       | 15        |
| Jugador    | 1000      |

### Continentes
- América (Ecuador, Brasil, Argentina, México, Estados Unidos)
- Europa (España, Portugal, Francia, Alemania, Inglaterra)
- Asia (Japón)
- Oceanía (Australia)
- África (Marruecos, Senegal, Nigeria)
