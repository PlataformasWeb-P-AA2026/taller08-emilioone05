# este módulo será usado para posibles configuraciones
#
# cadena conector a la base de datos
#
# -------------------------------------------------------
# OPCIÓN 1: SQLite
# No requiere instalación de servidor
# La base de datos se crea automáticamente como archivo
# -------------------------------------------------------
# cadena_base_datos = 'sqlite:///paises.db'

# -------------------------------------------------------
# OPCIÓN 2: MySQL / MariaDB
# Para activar:
#   1. Comentar la línea de SQLite de arriba
#   2. Descomentar la línea de abajo
#   3. Cambiar "tu_clave" por la contraseña de root
# La base de datos "paises" se crea automáticamente
# Requisito: pip install pymysql
# -------------------------------------------------------
cadena_base_datos = 'mysql+pymysql://root:emiliojosepe777@localhost/paises'