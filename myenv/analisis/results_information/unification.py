import os
import glob
from pybtex.database import parse_file, BibliographyData

# 📂 Definir la carpeta donde están los archivos BibTeX
carpeta = os.path.abspath("../extract_information/conections/archivos_csv")

# 📌 Buscar archivos .bib en la carpeta
archivos_bib = glob.glob(os.path.join(carpeta, "*.bib"))

if not archivos_bib:
    print(f"❌ No se encontraron archivos .bib en {carpeta}.")
    exit()

print(f"📂 Archivos encontrados: {archivos_bib}")

# 📌 Archivos de salida
archivo_final = os.path.join(carpeta, "unificado.bib")
archivo_repetidos = os.path.join(carpeta, "repetido.bib")

# 📌 Diccionarios para referencias únicas y repetidas
referencias = {}
repetidos = {}

# 📌 Leer cada archivo BibTeX y procesarlo
for archivo in archivos_bib:
    try:
        bib_data = parse_file(archivo)
        
        for key, entry in bib_data.entries.items():
            titulo = entry.fields.get("title", "Unknown Title")  # Obtener el título, o 'Unknown Title' si no existe
            
            if titulo in referencias:
                repetidos[titulo] = entry  # Guardar si ya existía
            else:
                referencias[titulo] = entry  # Agregar si es nuevo
                
    except Exception as e:
        print(f"⚠️ Error al procesar {archivo}: {e}")

# 📌 Guardar el archivo unificado (sin duplicados)
try:
    bib_final = BibliographyData(referencias)
    with open(archivo_final, "w", encoding="utf-8") as f:
        f.write(bib_final.to_string("bibtex"))
except IOError as e:
    print(f"❌ Error al escribir {archivo_final}: {e}")

# 📌 Guardar los repetidos
try:
    bib_repetidos = BibliographyData(repetidos)
    with open(archivo_repetidos, "w", encoding="utf-8") as f:
        f.write(bib_repetidos.to_string("bibtex"))
except IOError as e:
    print(f"❌ Error al escribir {archivo_repetidos}: {e}")

print(f"✅ Archivos generados:\n - {archivo_final} (sin duplicados)\n - {archivo_repetidos} (duplicados)")
