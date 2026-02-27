import pandas as pd

# 1. Cargar el archivo limpieza1.csv
try:
    df = pd.read_csv('limpieza1.csv')
    
    # --- DEPURACIÓN: Asegurar nombres de columnas ---
    # Convertimos todos los nombres a minúsculas para evitar errores de 'Año' vs 'año'
    df.columns = [col.lower() for col in df.columns]
    
    # Identificamos cómo se llama la columna de año ahora
    col_año = 'año' if 'año' in df.columns else 'anio' # Por si acaso se guardó sin la ñ
    
except FileNotFoundError:
    print("Error: No se encontró 'limpieza1.csv'.")
    exit()

print(f"--- Generando Índice de Materias usando la columna: {col_año} ---")

# 2. Filtrar reprobados
reprobados = df[df['calificacion'] < 6].copy()

# 3. Agrupar por materia y la columna de año detectada
conteo_temporal = reprobados.groupby(['materia', col_año]).size().reset_index(name='conteo')

# 4. Transformar los años en columnas (Pivot)
resumen_años = conteo_temporal.pivot(index='materia', columns=col_año, values='conteo').reset_index()

# 5. Limpieza y relleno de ceros
resumen_años = resumen_años.fillna(0)

# Aseguramos que las columnas de los años sean enteros
columnas_años = [col for col in resumen_años.columns if col != 'materia']
resumen_años[columnas_años] = resumen_años[columnas_años].astype(int)

# 6. Calcular el Total General
resumen_años['alumnos_reprobados'] = resumen_años[columnas_años].sum(axis=1)

# 7. Ordenar y Guardar
resumen_años = resumen_años.sort_values(by='alumnos_reprobados', ascending=False)
resumen_años.to_csv('IndiceMaterias.csv', index=False)

print("\n--- ¡Archivo IndiceMaterias.csv actualizado con éxito! ---")