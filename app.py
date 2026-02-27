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

# 2. Barra Lateral - Menú Completo con 6 secciones
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
        st.info("💡 **Análisis de Riesgo:** La nueva sección permite identificar alumnos con promedio menor a 6.")
    with col2:
        st.success("✅ **Estado:** Sistema completo y operativo.")

# --- SECCIÓN: LISTA LIMPIA ---
elif menu == "Lista limpia":
    st.header("✨ Datos Estandarizados")
    try:
        df_limpio = pd.read_csv('limpieza1.csv')
        st.metric("Total de registros", len(df_limpio))
        st.dataframe(df_limpio, use_container_width=True)
    except FileNotFoundError:
        st.error("❌ No se encontró 'limpieza1.csv'")

# --- SECCIÓN: INDICE DE MATERIAS ---
elif menu == "Indice de materias":
    st.header("📉 Materias con Mayor Índice de Reprobados")
    try:
        df_ind = pd.read_csv('IndiceMaterias.csv')
        col_t, col_g = st.columns([1, 1])
        with col_t:
            st.dataframe(df_ind, use_container_width=True)
        with col_g:
            st.bar_chart(data=df_ind, x='materia', y='alumnos_reprobados')
    except FileNotFoundError:
        st.error("❌ No se encontró 'IndiceMaterias.csv'")

# --- SECCIÓN: RANKING DE CARRERAS ---
elif menu == "Ranking de carreras":
    st.header("🏆 Ranking de Carreras por Promedio")
    try:
        df_prom = pd.read_csv('PromedioCarreras.csv')
        años_disponibles = sorted(df_prom['Año'].unique(), reverse=True)
        año_sel = st.selectbox("Selecciona el año:", años_disponibles)
        df_filtrado = df_prom[df_prom['Año'] == año_sel]
        col_t, col_g = st.columns([1, 1])
        with col_t:
            st.dataframe(df_filtrado[['Carrera', 'Promedio_Calificacion']], use_container_width=True)
        with col_g:
            st.bar_chart(data=df_filtrado, x='Carrera', y='Promedio_Calificacion')
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

# --- SECCIÓN: ALUMNOS EN RIESGO (NUEVA) ---
elif menu == "Alumnos en Riesgo":
    st.header("⚠️ Alerta de Alumnos con Riesgo ALTO")
    st.write("Listado de estudiantes cuyo promedio general es inferior a 6.")
    
    try:
        df_riesgo = pd.read_csv('RiesgoAlumno.csv')
        
        # Métrica de impacto
        total_alumnos_riesgo = df_riesgo['id_id_estudiante'].nunique() if 'id_id_estudiante' in df_riesgo.columns else df_riesgo['id_estudiante'].nunique()
        st.error(f"Se han identificado **{total_alumnos_riesgo}** alumnos en situación crítica.")
        
        # Buscador interactivo
        st.subheader("🔍 Buscador de Estudiante")
        busqueda = st.text_input("Ingresa el ID del estudiante para verificar su situación:", "")
        
        if busqueda:
            # Filtramos por ID (convertimos a string para asegurar coincidencia)
            col_id = 'id_estudiante' if 'id_estudiante' in df_riesgo.columns else 'id_id_estudiante'
            resultado = df_riesgo[df_riesgo[col_id].astype(str).str.contains(busqueda)]
            
            if not resultado.empty:
                st.success(f"Resultados para el ID: {busqueda}")
                st.dataframe(resultado, use_container_width=True)
            else:
                st.warning("No se encontró ningún alumno con ese ID en la lista de riesgo.")
        else:
            # Si no hay búsqueda, mostramos toda la tabla
            st.dataframe(df_riesgo, use_container_width=True)
            
    except FileNotFoundError:
        st.error("❌ Error: No se encontró el archivo 'RiesgoAlumno.csv'.")
        st.info("Asegúrate de ejecutar tu script 'RiesgoAlumnos' primero.")