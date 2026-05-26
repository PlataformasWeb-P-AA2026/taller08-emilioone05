import csv
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

mapa_continente = {
    'Ecuador'       : 'América',
    'Brasil'        : 'América',
    'Argentina'     : 'América',
    'México'        : 'América',
    'Estados Unidos': 'América',
    'España'        : 'Europa',
    'Portugal'      : 'Europa',
    'Francia'       : 'Europa',
    'Alemania'      : 'Europa',
    'Inglaterra'    : 'Europa',
    'Japón'         : 'Asia',
    'Australia'     : 'Oceanía',
    'Marruecos'     : 'África',
    'Senegal'       : 'África',
    'Nigeria'       : 'África',
}



print("Creando continentes...")

# diccionario auxiliar nombre_continente -> objeto Continente
# para reutilizarlo cuando se creen los países
continentes_dict = {}

nombres_continentes = set(mapa_continente.values())
for nombre in sorted(nombres_continentes):
    obj_continente = Continente(nombre=nombre)
    session.add(obj_continente)
    continentes_dict[nombre] = obj_continente

# se confirman las inserciones para que los objetos
# reciban su id autogenerado por la base de datos
session.commit()

print("Continentes creados: %d" % len(continentes_dict))


# -------------------------------------------------------
# Paso 2: crear los objetos Pais
# se lee el CSV para extraer todos los países únicos
# que aparecen (tanto en nacimiento como donde juegan)
# -------------------------------------------------------
print("Creando países...")

# se recopilan los nombres únicos de país del CSV
nombres_paises = set()
with open('jugadores_futbol.csv', encoding='utf-8-sig') as f:
    lector = csv.DictReader(f)
    for fila in lector:
        nombres_paises.add(fila['pais_nacimiento'].strip())
        nombres_paises.add(fila['pais_donde_juega'].strip())

# diccionario auxiliar nombre_pais -> objeto Pais
paises_dict = {}

for nombre in sorted(nombres_paises):
    # se obtiene el nombre del continente para este país
    nombre_continente = mapa_continente[nombre]
    # se recupera el objeto Continente ya creado
    obj_continente = continentes_dict[nombre_continente]
    # se crea el objeto Pais vinculado a su Continente
    obj_pais = Pais(nombre=nombre, continente=obj_continente)
    session.add(obj_pais)
    paises_dict[nombre] = obj_pais

# se confirman las inserciones para que los países
# reciban su id autogenerado
session.commit()

print("Países creados: %d" % len(paises_dict))


# -------------------------------------------------------
# Paso 3: crear los objetos Jugador
# se lee el CSV nuevamente y por cada fila
# se crea un objeto Jugador vinculado a sus dos países
# -------------------------------------------------------
print("Creando jugadores...")

contador = 0
with open('jugadores_futbol.csv', encoding='utf-8-sig') as f:
    lector = csv.DictReader(f)
    for fila in lector:
        # se recuperan los objetos Pais ya creados
        # usando el diccionario auxiliar
        obj_pais_nac   = paises_dict[fila['pais_nacimiento'].strip()]
        obj_pais_juega = paises_dict[fila['pais_donde_juega'].strip()]

        # se crea el objeto Jugador con sus relaciones
        obj_jugador = Jugador(
            nombre                    = fila['nombre_jugador'].strip(),
            posicion                  = fila['posicion'].strip(),
            edad                      = int(fila['edad']),
            numero_partidos_seleccion = int(fila['numero_partidos_seleccion']),
            goles_seleccion           = int(fila['goles_seleccion']),
            pais_nacimiento           = obj_pais_nac,
            pais_donde_juega          = obj_pais_juega
        )
        session.add(obj_jugador)
        contador += 1

# se confirman todas las inserciones de jugadores
session.commit()
session.close()

print("Jugadores creados: %d" % contador)
print("Base de datos poblada correctamente.")