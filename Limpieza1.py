import pandas as pd
import unicodedata

def eliminar_acentos(texto):
    if isinstance(texto, str):
        # Normaliza y elimina tildes/acentos
        texto = unicodedata.normalize('NFD', texto)
        texto = texto.encode('ascii', 'ignore').decode("utf-8")
    return texto

# 1. Cargar tus datos originales
try:
    df = pd.read_csv('datos.csv')
except FileNotFoundError:
    print("Error: No se encontró 'datos.csv'. Asegúrate de que el archivo esté en la carpeta.")
    exit()

# 2. Limpieza de Acentos en todo el DataFrame
# Aplicamos la función a las columnas de texto para evitar errores de codificación
df['carrera'] = df['carrera'].apply(eliminar_acentos)
df['materia'] = df['materia'].apply(eliminar_acentos)

# 3. Estandarización de Carreras (Unificación)
# Quitamos espacios accidentales y unimos palabras de las carreras
df['carrera'] = df['carrera'].str.strip().str.replace(' ', '')

# 4. NUEVA MODIFICACIÓN: Unir palabras de las Materias
# Esto convierte "Calculo Diferencial" en "CalculoDiferencial"
df['materia'] = df['materia'].str.strip().str.replace(r'\s+', '', regex=True)

# 5. Limpieza de columnas adicionales
# Aseguramos que los IDs y semestres no tengan espacios
df['id_estudiante'] = df['id_estudiante'].astype(str).str.strip()

# 6. Sobreescribir el archivo de salida
# Al usar index=False, el archivo queda limpio para que Streamlit lo lea directo
df.to_csv('limpieza1.csv', index=False)

print("--- Proceso de Limpieza Completado ---")
print(f"Total de registros procesados: {len(df)}")
print("Archivo 'limpieza1.csv' actualizado con materias unificadas.")