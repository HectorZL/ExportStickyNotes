import sqlite3
import os
import zipfile

# Conectar a la base de datos SQLite
conexion = sqlite3.connect('plum.sqlite')
cursor = conexion.cursor()

# Seleccionar solo las columnas 'Id' y 'Text' de la tabla NOTE
cursor.execute("SELECT Id, Text FROM NOTE;")
filas = cursor.fetchall()

# Cerrar la conexión
conexion.close()

# Directorio para guardar archivos Markdown individuales
directorio_salida = 'notas_individuales'
os.makedirs(directorio_salida, exist_ok=True)

# Guardar archivos Markdown individuales y añadirlos al archivo ZIP
nombre_archivo_zip = 'output_notes.zip'
with zipfile.ZipFile(nombre_archivo_zip, 'w') as zip_file:
    for idx, fila in enumerate(filas, start=1):
        _, texto_nota = fila

        # Eliminar los códigos específicos seguidos de un espacio
        lineas = [linea.split(' ', 1)[1] if len(linea.split(' ', 1)) > 1 else linea for linea in texto_nota.split('\n')]

        # Crear un nombre de archivo incremental
        nombre_archivo_md = f'nota_{idx}.md'
        ruta_archivo_md = os.path.join(directorio_salida, nombre_archivo_md)

        # Escribir el archivo Markdown individual
        with open(ruta_archivo_md, 'w', encoding='utf-8') as archivo_md:
            archivo_md.write('\n'.join(lineas))

        # Añadir el archivo Markdown al archivo ZIP
        zip_file.write(ruta_archivo_md, nombre_archivo_md)

        # Eliminar el archivo Markdown individual después de agregarlo al ZIP
        os.remove(ruta_archivo_md)

# Imprimir mensaje cuando se ha completado la operación
print(f"\nSe han guardado los archivos individuales en formato Markdown en el archivo ZIP: {nombre_archivo_zip}")
