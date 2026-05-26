import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la clase(s) del archivo genera_tablas
from genera_tablas import Continente, Pais, Jugador

# se importa información del archivo de configuración
from config import cadena_base_datos

# se genera el enlace al gestor de base de datos
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()


# -------------------------------------------------------
# Configuración general de la página Streamlit
# -------------------------------------------------------
st.set_page_config(
    page_title="Taller 08 - Jugadores de Fútbol",
    layout="wide"
)

st.title("Taller 08 — Integración de datos y ORM")
st.markdown("**Base de datos:** paises.db (SQLite) | **Entidades:** Continente · País · Jugador")
st.divider()


# =======================================================
# TABLA 1
# Todos los jugadores con los campos solicitados:
# nombre, pais_nacimiento, pais_donde_juega, posicion,
# edad, partidos, goles, continente
# Se navega por los relationships para obtener
# los datos de las entidades relacionadas
# =======================================================
st.subheader("Tabla 1 — Jugadores")

# se obtienen todos los jugadores de la base de datos
jugadores = session.query(Jugador).all()

# se construye una lista de diccionarios para la tabla
# por cada jugador se navega por los relationships
# para obtener los datos de Pais y Continente
datos_jugadores = []
for j in jugadores:
    datos_jugadores.append({
        "Nombre"            : j.nombre,
        "País nacimiento"   : j.pais_nacimiento.nombre,
        "País donde juega"  : j.pais_donde_juega.nombre,
        "Posición"          : j.posicion,
        "Edad"              : j.edad,
        "Partidos selección": j.numero_partidos_seleccion,
        "Goles selección"   : j.goles_seleccion,
        "Continente"        : j.pais_nacimiento.continente.nombre
    })

st.dataframe(datos_jugadores, use_container_width=True)
st.caption("Total de jugadores: %d" % len(datos_jugadores))


st.divider()


# =======================================================
# TABLA 2
# Por continente:
# - número de jugadores en la base
# - total de goles de esos jugadores
# Se navega: Continente -> paises -> jugadores_nacidos
# =======================================================
st.subheader("Tabla 2 — Resumen por Continente")

# se obtienen todos los continentes
continentes = session.query(Continente).all()

datos_continentes = []
for c in continentes:
    # se acumulan jugadores y goles
    # recorriendo los países del continente
    total_jugadores = 0
    total_goles     = 0
    # c.paises es la lista de países de este continente
    for p in c.paises:
        # p.jugadores_nacidos es la lista de jugadores
        # nacidos en ese país
        for j in p.jugadores_nacidos:
            total_jugadores += 1
            total_goles     += j.goles_seleccion

    datos_continentes.append({
        "Continente"         : c.nombre,
        "Número de jugadores": total_jugadores,
        "Total de goles"     : total_goles
    })

# se ordena de mayor a menor por número de jugadores
datos_continentes.sort(key=lambda x: x["Número de jugadores"], reverse=True)

st.dataframe(datos_continentes, use_container_width=True)


st.divider()


# =======================================================
# TABLA 3
# Por país:
# - número de jugadores en la base
# - total de goles de esos jugadores
# Se navega: Pais -> jugadores_nacidos
# Solo se muestran países que tienen jugadores
# =======================================================
st.subheader("Tabla 3 — Resumen por País")

# se obtienen todos los países
paises = session.query(Pais).all()

datos_paises = []
for p in paises:
    # p.jugadores_nacidos es el relationship definido en Pais
    total_jugadores = len(p.jugadores_nacidos)
    total_goles     = sum(j.goles_seleccion for j in p.jugadores_nacidos)

    # solo se incluyen países que tienen jugadores en la base
    if total_jugadores > 0:
        datos_paises.append({
            "País"               : p.nombre,
            "Continente"         : p.continente.nombre,
            "Número de jugadores": total_jugadores,
            "Total de goles"     : total_goles
        })

# se ordena de mayor a menor por número de jugadores
datos_paises.sort(key=lambda x: x["Número de jugadores"], reverse=True)

st.dataframe(datos_paises, use_container_width=True)


session.close()