import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(
    page_title="Sistema de Análisis FES Aragón", 
    page_icon="🎓", 
    layout="wide"
)

# Título principal
st.title("📊 Panel de Control Académico")
st.markdown("---")

# 2. Barra Lateral - Menú Completo
st.sidebar.header("Menú de Reportes")
menu = st.sidebar.radio(
    "Selecciona una opción:",
    ["Vista General", "Lista limpia", "Indice de materias", 
     "Ranking de carreras", "Tendencias por Semestre", "Alumnos en Riesgo"]
)

# --- SECCIÓN: VISTA GENERAL ---
if menu == "Vista General":
    st.subheader("Bienvenido al Portal de Datos")
    st.write("Explora el comportamiento académico de la facultad mediante estos reportes dinámicos.")
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Análisis de Tendencias:** Ahora puedes ver la evolución por año en la sección de materias.")
    with col2:
        st.success("✅ **Estado:** Sistema sincronizado con GitHub.")

# --- SECCIÓN: LISTA LIMPIA ---
elif menu == "Lista limpia":
    st.header("✨ Datos Estandarizados")
    try:
        df_limpio = pd.read_csv('limpieza1.csv')
        st.metric("Total de registros", len(df_limpio))
        st.dataframe(df_limpio, use_container_width=True)
    except FileNotFoundError:
        st.error("❌ No se encontró 'limpieza1.csv'. Ejecuta primero Limpieza1.py")

# --- SECCIÓN: INDICE DE MATERIAS (GRÁFICAS POR AÑO) ---
elif menu == "Indice de materias":
    st.header("📉 Materias con Mayor Índice de Reprobados")
    try:
        df_ind = pd.read_csv('IndiceMaterias.csv')
        
        # 1. Tabla de datos completa
        with st.expander("Ver tabla detallada por año"):
            st.dataframe(df_ind, use_container_width=True)
        
        # 2. Gráficas por Año (en columnas pequeñas)
        st.subheader("Tendencia Individual por Año")
        col_graf1, col_graf2, col_graf3 = st.columns(3)
        
        # Detectamos las columnas de años disponibles (2022, 2023, 2024)
        años_columnas = [col for col in df_ind.columns if col not in ['materia', 'alumnos_reprobados']]
        
        with col_graf1:
            if '2022' in años_columnas:
                st.caption("Año 2022")
                st.bar_chart(data=df_ind, x='materia', y='2022')
        
        with col_graf2:
            if '2023' in años_columnas:
                st.caption("Año 2023")
                st.bar_chart(data=df_ind, x='materia', y='2023')
                
        with col_graf3:
            if '2024' in años_columnas:
                st.caption("Año 2024")
                st.bar_chart(data=df_ind, x='materia', y='2024')

        # 3. Gráfica General (Abajo y más grande)
        st.markdown("---")
        st.subheader("📊 Consolidado Histórico (Todos los años)")
        st.bar_chart(data=df_ind, x='materia', y='alumnos_reprobados', color="#ff4b4b")
        
    except FileNotFoundError:
        st.error("❌ No se encontró 'IndiceMaterias.csv'. Ejecuta IndiceMaterias.py")
# --- SECCIÓN: RANKING DE CARRERAS ---
elif menu == "Ranking de carreras":
    st.header("🏆 Ranking de Carreras por Promedio")
    try:
        df_prom = pd.read_csv('PromedioCarreras.csv')
        # Normalizamos nombres de columna por si acaso
        df_prom.columns = [c.lower() for c in df_prom.columns]
        col_año = 'año' if 'año' in df_prom.columns else 'anio'
        
        años_disponibles = sorted(df_prom[col_año].unique(), reverse=True)
        año_sel = st.selectbox("Selecciona el año:", años_disponibles)
        df_filtrado = df_prom[df_prom[col_año] == año_sel]
        
        col_t, col_g = st.columns([1, 1])
        with col_t:
            st.dataframe(df_filtrado, use_container_width=True)
        with col_g:
            st.bar_chart(data=df_filtrado, x='carrera', y='promedio_calificacion')
    except FileNotFoundError:
        st.error("❌ No se encontró 'PromedioCarreras.csv'")

# --- SECCIÓN: TENDENCIAS POR SEMESTRE ---
elif menu == "Tendencias por Semestre":
    st.header("📈 Evolución Académica por Semestre")
    try:
        df_tend = pd.read_csv('TendenciasSemestre.csv')
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Promedio General", f"{df_tend['Promedio_General'].mean():.2f}")
        col_m2.metric("Total Alumnos", int(df_tend['Total_Alumnos'].sum()))
        
        tab1, tab2 = st.tabs(["📉 Promedio", "👥 Población"])
        with tab1:
            st.line_chart(data=df_tend, x='Semestre', y='Promedio_General')
        with tab2:
            st.area_chart(data=df_tend, x='Semestre', y='Total_Alumnos')
    except FileNotFoundError:
        st.error("❌ No se encontró 'TendenciasSemestre.csv'")

# --- SECCIÓN: ALUMNOS EN RIESGO ---
elif menu == "Alumnos en Riesgo":
    st.header("⚠️ Reporte de Alumnos con Riesgo Académico")
    
    try:
        df_riesgo = pd.read_csv('RiesgoAlumno.csv')
        # Detectamos la columna de año que guardamos
        col_anio = 'año' if 'año' in df_riesgo.columns else 'anio'
        
        # Creamos las pestañas para cada año
        tab2022, tab2023, tab2024 = st.tabs(["📅 2022", "📅 2023", "📅 2024"])
        
        with tab2022:
            st.subheader("Estudiantes en riesgo - Ciclo 2022")
            datos_2022 = df_riesgo[df_riesgo[col_anio] == 2022]
            st.metric("Total Reprobados 2022", len(datos_2022))
            st.dataframe(datos_2022, use_container_width=True)
            
        with tab2023:
            st.subheader("Estudiantes en riesgo - Ciclo 2023")
            datos_2023 = df_riesgo[df_riesgo[col_anio] == 2023]
            st.metric("Total Reprobados 2023", len(datos_2023))
            st.dataframe(datos_2023, use_container_width=True)
            
        with tab2024:
            st.subheader("Estudiantes en riesgo - Ciclo 2024")
            datos_2024 = df_riesgo[df_riesgo[col_anio] == 2024]
            st.metric("Total Reprobados 2024", len(datos_2024))
            st.dataframe(datos_2024, use_container_width=True)

    except FileNotFoundError:
        st.error("❌ No se encontró 'RiesgoAlumno.csv'.")