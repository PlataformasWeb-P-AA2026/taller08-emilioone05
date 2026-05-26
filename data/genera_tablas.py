from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text

# se importa información del archivo de configuración
from config import cadena_base_datos

# -------------------------------------------------------
# Creación automática de la base de datos
# Si se usa MySQL/MariaDB, se conecta primero sin
# especificar la base de datos y la crea si no existe.
# Si se usa SQLite, no aplica porque SQLite
# crea el archivo automáticamente.
# -------------------------------------------------------
if 'mysql' in cadena_base_datos:
    cadena_sin_bd = cadena_base_datos.rsplit('/', 1)[0]
    nombre_bd     = cadena_base_datos.rsplit('/', 1)[1]
    engine_temp   = create_engine(cadena_sin_bd)
    with engine_temp.connect() as conexion:
        conexion.execute(
            text("CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8mb4" % nombre_bd)
        )
    print("Base de datos '%s' verificada/creada en MySQL." % nombre_bd)

# se genera el enlace al gestor de base de datos
engine = create_engine(cadena_base_datos)

Base = declarative_base()


# Entidad 1: Continente
# Un continente tiene muchos países asociados (One to Many)
class Continente(Base):
    __tablename__ = 'continente'
    id     = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    paises = relationship('Pais', back_populates='continente')

    def __repr__(self):
        return "Continente: id=%d nombre=%s" % (self.id, self.nombre)


# Entidad 2: Pais
# Un país pertenece a un continente
# Un país puede tener muchos jugadores (nacidos ahí o que juegan ahí)
class Pais(Base):
    __tablename__ = 'pais'
    id            = Column(Integer, primary_key=True)
    nombre        = Column(String(100))
    continente_id = Column(Integer, ForeignKey('continente.id'))
    continente    = relationship('Continente', back_populates='paises')
    # se distinguen dos relaciones con Jugador
    # porque un jugador tiene DOS llaves foráneas hacia Pais
    jugadores_nacidos = relationship(
        'Jugador',
        foreign_keys='Jugador.pais_nacimiento_id',
        back_populates='pais_nacimiento'
    )
    jugadores_activos = relationship(
        'Jugador',
        foreign_keys='Jugador.pais_donde_juega_id',
        back_populates='pais_donde_juega'
    )

    def __repr__(self):
        return "Pais: id=%d nombre=%s continente=%s" % (
            self.id, self.nombre, self.continente.nombre
        )


# Entidad 3: Jugador
# Un jugador nació en un país y juega en otro (pueden coincidir)
class Jugador(Base):
    __tablename__ = 'jugador'
    id                        = Column(Integer, primary_key=True)
    nombre                    = Column(String(200))
    posicion                  = Column(String(100))
    edad                      = Column(Integer)
    numero_partidos_seleccion = Column(Integer)
    goles_seleccion           = Column(Integer)
    # un jugador tiene dos llaves foráneas hacia Pais
    pais_nacimiento_id  = Column(Integer, ForeignKey('pais.id'))
    pais_donde_juega_id = Column(Integer, ForeignKey('pais.id'))
    pais_nacimiento  = relationship(
        'Pais',
        foreign_keys=[pais_nacimiento_id],
        back_populates='jugadores_nacidos'
    )
    pais_donde_juega = relationship(
        'Pais',
        foreign_keys=[pais_donde_juega_id],
        back_populates='jugadores_activos'
    )

    def __repr__(self):
        return "Jugador: nombre=%s posicion=%s edad=%d goles=%d" % (
            self.nombre, self.posicion, self.edad, self.goles_seleccion
        )


# se crean las tablas en la base de datos
# si las tablas ya existen no las sobreescribe
Base.metadata.create_all(engine)