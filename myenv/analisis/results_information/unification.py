# Importar la librería necesaria
from pybtex.database import BibliographyData, Entry, parse_string
import pandas as pd
import glob

#Title,Link,Authors,Conference,Year


def unificar():
    #busca todos los archivos csv en el directorio
    print()
    archivos_csv = glob.glob("analisispy/myenv/analisis/extract_information/conections/*.csv") 
    print(f"Se encontraron {len(archivos_csv)} archivos CSV.")

    #los une en un datagrama
    df = pd.concat([pd.read_csv(archivo) for archivo in archivos_csv], ignore_index=True)

    # identificamos duplicados
    duplicados = df[df.duplicated(subset=["Title","Link", "Authors", "Conference", "Year"], keep=False)]  # Encuentra duplicados
    df_sin_duplicados = df.drop_duplicates(subset=["Title","Link", "Authors", "Conference", "Year"], keep="first")  # Mantiene solo una versión

    # Guardar los resultados en archivos CSV
    df_sin_duplicados.to_csv("analisispy/myenv/analisis/results_information/archivo_final.csv", index=False)  # CSV sin duplicados
    duplicados.to_csv("analisispy/myenv/analisis/results_information/duplicados.csv", index=False)  # CSV con duplicados

    print("csv guardados exitosamente")

    csv_a_bibtex("analisispy/myenv/analisis/results_information/archivo_final.csv","analisispy/myenv/analisis/results_information/biptext_sd.bib")
    csv_a_bibtex("analisispy/myenv/analisis/results_information/duplicados.csv","analisispy/myenv/analisis/results_information/biptext_cd.bib")



def csv_a_bibtex(csv_file, bibtex_file):
    # Cargar el archivo CSV
    df = pd.read_csv(csv_file)

    # Crear un diccionario para almacenar las referencias en BibTeX
    entries = {}

    for i, row in df.iterrows():
        key = f"ref{i+1}"  # Clave única para cada referencia
        fields = {}

        # Agregamos campos según las columnas
        if pd.notna(row["Title"]):
            fields["title"] = row["Title"]
        if pd.notna(row["Link"]):
            fields["Link"]=row["Link"]
        if pd.notna(row["Authors"]):
            fields["author"] = row["Authors"]
        if pd.notna(row["Conference"]):
            fields["Conference"] = row["Conference"]  
        if pd.notna(row["Year"]):
            fields["year"] = str(row["Year"])


        # Crear la entrada BibTeX si tiene título y autor
        if "title" in fields and "author" in fields:
            entries[key] = Entry("inproceedings", fields=fields)  # "inproceedings" es para conferencias

    # Guardar en archivo BibTeX
    bib_data = BibliographyData(entries)
    with open(bibtex_file, "w", encoding="utf-8") as f:
        f.write(bib_data.to_string("bibtex"))

    print(f"Archivo BibTeX guardado como {bibtex_file}")

