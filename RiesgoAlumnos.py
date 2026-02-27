import pandas as pd

# 1. Cargar el archivo limpieza1.csv
try:
    df = pd.read_csv('limpieza1.csv')
    # Normalizamos nombres de columnas para evitar errores de mayúsculas/minúsculas
    df.columns = [col.lower() for col in df.columns]
except FileNotFoundError:
    print("Error: No se encontró 'limpieza1.csv'.")
    exit()

print("--- Generando Reporte Unificado de Riesgo ---")

# 2. Filtrar alumnos en riesgo (calificación < 6.0)
df_riesgo = df[df['calificacion'] < 6.0].copy()

# 3. Detectar la columna de año (por si es 'año' o 'anio')
col_anio = 'año' if 'año' in df_riesgo.columns else 'anio'

# 4. Seleccionar las columnas solicitadas INCLUYENDO el año para poder filtrar después
columnas_reporte = ['id_estudiante', 'carrera', 'materia', 'calificacion', 'semestre', col_anio]

# 5. Guardar todo en un solo archivo CSV
df_final = df_riesgo[columnas_reporte]
df_final.to_csv('RiesgoAlumno.csv', index=False)

print(f"✅ Éxito: Se guardaron {len(df_final)} registros en 'RiesgoAlumno.csv'.")
print(f"Años incluidos: {df_final[col_anio].unique()}")