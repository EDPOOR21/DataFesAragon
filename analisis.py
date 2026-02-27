import pandas as pd

# 1. Cargar el archivo limpieza1.csv
try:
    df = pd.read_csv('limpieza1.csv')
except FileNotFoundError:
    print("Error: No se encontró 'limpieza1.csv'.")
    exit()

print("--- Calculando tendencias por semestre ---")

# 2. Agrupar por semestre y calcular promedio y cantidad de alumnos
# Usamos .agg para hacer dos operaciones distintas al mismo tiempo
tendencias = df.groupby('semestre').agg({
    'calificacion': 'mean',        # Promedio de notas
    'id_estudiante': 'nunique'     # Cantidad de alumnos únicos
}).reset_index()

# 3. Renombrar columnas para que sean claras
tendencias.columns = ['Semestre', 'Promedio_General', 'Total_Alumnos']

# 4. Ordenar por semestre (del 1 al 10)
tendencias = tendencias.sort_values(by='Semestre')

# 5. Mostrar resumen en terminal
print("\n--- Resumen de Tendencias ---")
print(tendencias)

# 6. Guardar el nuevo archivo solicitado
nombre_salida = "TendenciasSemestre.csv"
tendencias.to_csv(nombre_salida, index=False)

print(f"\n¡Listo! El archivo '{nombre_salida}' ha sido generado con éxito.")