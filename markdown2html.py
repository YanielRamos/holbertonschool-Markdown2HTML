#!/usr/bin/python3
"""
Escribe un script markdown2html.py que toma dos argumentos:
El primer argumento es el nombre del archivo Markdown
El segundo argumento es el nombre del archivo de salida
"""

import re  # Módulo de expresiones regulares para manejar patrones en el texto
import hashlib  # Módulo para generar los hash MD5
import sys  # Parámetros y funciones específicos del sistema (para manejar los argumentos y salir del script)
import os  # Proporciona funciones para interactuar con el sistema operativo (por ejemplo, verificar si un archivo existe)

if __name__ == "__main__":  # Verifica si el script se está ejecutando directamente (no importado)
    if len(sys.argv) < 3:  # Verifica si hay menos de 3 argumentos (el nombre del script + 2 argumentos)
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")  # Imprime un mensaje de uso en stderr
        sys.exit(1)  # Sale con el código de estado 1 indicando un error
    
    if not os.path.exists(sys.argv[1]):  # Verifica si el primer argumento (archivo Markdown) existe
        sys.stderr.write(f"Missing {sys.argv[1]}\n")  # Imprime un mensaje de error si el archivo no existe
        sys.exit(1)  # Sale con el código de estado 1 indicando un error

    # Abre el archivo Markdown de entrada (sys.argv[1]) para leer y el archivo HTML de salida (sys.argv[2]) para escribir
    with open(sys.argv[1], 'r') as r, open(sys.argv[2], 'w') as w:
        change_status = False  # Bandera para rastrear si estamos dentro de una lista no ordenada
        ordered_status = False  # Bandera para rastrear si estamos dentro de una lista ordenada
        paragraph = False  # Bandera para rastrear si estamos dentro de un párrafo

        # Itera sobre cada línea en el archivo de entrada
        for line in r:
            # Reemplaza la sintaxis de negrita en markdown (**) con las etiquetas <b> (solo la primera ocurrencia en la línea)
            line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
            # Reemplaza la sintaxis de cursiva en markdown (__) con las etiquetas <em> (solo la primera ocurrencia en la línea)
            line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)

            # Busca la sintaxis personalizada de Markdown [[...]] para obtener el hash MD5
            md5_matches = re.findall(r'\[\[.+?\]\]', line)
            if md5_matches:  # Si se encuentra esta sintaxis
                md5_content = re.findall(r'\[\[(.+?)\]\]', line)[0]  # Extrae el contenido entre [[ y ]]
                # Reemplaza [[contenido]] por su hash MD5
                line = line.replace(md5_matches[0], hashlib.md5(md5_content.encode()).hexdigest())

            # Busca la sintaxis personalizada de Markdown ((...)) para eliminar los caracteres 'C' y 'c'
            delete_c_matches = re.findall(r'\(\(.+?\)\)', line)
            if delete_c_matches:  # Si se encuentra esta sintaxis
                delete_c_content = re.findall(r'\(\((.+?)\)\)', line)[0]  # Extrae el contenido dentro de los paréntesis
                # Elimina los caracteres 'C' y 'c' del contenido
                cleaned_content = ''.join(c for c in delete_c_content if c not in 'Cc')
                # Reemplaza el contenido en ((...)) por el contenido limpiado
                line = line.replace(delete_c_matches[0], cleaned_content)

            length = len(line)  # Calcula la longitud de la línea actual
            # Elimina los caracteres '#' al principio de la línea para verificar si es un encabezado
            headings = line.lstrip('#')
            heading_count = length - len(headings)  # El número de caracteres '#' indica el nivel del encabezado

            # Elimina los caracteres '-' al principio de la línea para verificar si es una lista no ordenada
            unordered = line.lstrip('-')
            unordered_count = length - len(unordered)  # Cuenta el número de caracteres '-'

            # Elimina los caracteres '*' al principio de la línea para verificar si es una lista ordenada
            ordered = line.lstrip('*')
            ordered_count = length - len(ordered)  # Cuenta el número de caracteres '*'

            # Verifica si la línea es un encabezado (de 1 a 6 caracteres '#')
            if 1 <= heading_count <= 6:
                line = f'<h{heading_count}>{headings.strip()}</h{heading_count}>\n'  # Convierte a etiquetas <h1> a <h6>

            # Si la línea es parte de una lista no ordenada
            if unordered_count:
                if not change_status:  # Si no estamos dentro de una lista no ordenada
                    w.write('<ul>\n')  # Escribe la etiqueta <ul> de apertura para la lista no ordenada
                    change_status = True  # Establece la bandera para indicar que estamos dentro de una lista no ordenada
                line = f'<li>{unordered.strip()}</li>\n'  # Envuelve el ítem de la lista en una etiqueta <li>
            # Si la lista no ordenada termina (la siguiente línea no es parte de la lista)
            if change_status and not unordered_count:
                w.write('</ul>\n')  # Escribe la etiqueta </ul> de cierre para la lista no ordenada
                change_status = False  # Restablece la bandera

            # Si la línea es parte de una lista ordenada
            if ordered_count:
                if not ordered_status:  # Si no estamos dentro de una lista ordenada
                    w.write('<ol>\n')  # Escribe la etiqueta <ol> de apertura para la lista ordenada
                    ordered_status = True  # Establece la bandera para indicar que estamos dentro de una lista ordenada
                line = f'<li>{ordered.strip()}</li>\n'  # Envuelve el ítem de la lista en una etiqueta <li>
            # Si la lista ordenada termina (la siguiente línea no es parte de la lista)
            if ordered_status and not ordered_count:
                w.write('</ol>\n')  # Escribe la etiqueta </ol> de cierre para la lista ordenada
                ordered_status = False  # Restablece la bandera

            # Si la línea no es un encabezado, ítem de lista o parte de una lista ordenada/no ordenada
            if not (heading_count or change_status or ordered_status):
                # Si es un nuevo párrafo
                if not paragraph and length > 1:
                    w.write('<p>\n')  # Escribe la etiqueta <p> de apertura para un nuevo párrafo
                    paragraph = True  # Establece la bandera para indicar que estamos dentro de un párrafo
                elif length > 1:  # Si la línea no está vacía, añade un salto de línea
                    w.write('<br/>\n')
                # Si el párrafo termina (línea vacía o fin de párrafo)
                elif paragraph:
                    w.write('</p>\n')  # Escribe la etiqueta </p> de cierre para el párrafo
                    paragraph = False  # Restablece la bandera

            # Escribe la línea procesada en el archivo de salida (solo si no está vacía)
            if length > 1:
                w.write(line)

        # Cierra cualquier etiqueta abierta de lista ordenada o párrafo
        if ordered_status:
            w.write('</ol>\n')
        if paragraph:
            w.write('</p>\n')

    sys.exit(0)  # Sale del script con el código de estado 0 indicando éxito
