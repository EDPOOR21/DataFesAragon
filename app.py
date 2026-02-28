import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(
    page_title="Sistema de Análisis FES Aragón",
    layout="wide"
)

# --- INYECCIÓN DE ESTILOS CSS (ESTILO ODYSSEY / FUTURISTA) ---
st.markdown("""
    <style>
        /* Importación de fuentes */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Space+Mono&display=swap');

        /* Variables de color basadas en la referencia visual */
        :root {
            --bg-base: #050508;
            --neon-purple: #8b5cf6;
            --neon-green: #10b981;
            --text-muted: #94a3b8;
            --text-light: #f8fafc;
        }

        /* Estilo global de la aplicación */
        .stApp {
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(139, 92, 246, 0.08), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(16, 185, 129, 0.08), transparent 25%);
            color: var(--text-light);
            font-family: 'Space Mono', monospace;
        }

        /* Ocultar elementos predeterminados (Sidebar y Header nativo) */
        [data-testid="stSidebar"] { display: none; }
        header { display: none !important; }

        /* Contenedor principal centrado con márgenes (evita que vaya de lado a lado) */
        .block-container {
            max-width: 1100px !important;
            margin: 40px auto;
            padding: 40px 50px !important;
            background: rgba(15, 10, 25, 0.85);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 40px;
            box-shadow: inset 0 0 20px rgba(139, 92, 246, 0.1), 0 0 30px rgba(0,0,0,0.5);
        }

        /* Header / Título Principal */
        .header-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 900;
            text-align: center;
            color: transparent;
            -webkit-text-stroke: 1px var(--neon-purple);
            background: linear-gradient(to bottom, var(--text-light), var(--text-muted));
            -webkit-background-clip: text;
            letter-spacing: 4px;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        .header-subtitle {
            font-family: 'Space Mono', monospace;
            color: var(--neon-green);
            text-align: center;
            font-size: 1rem;
            letter-spacing: 6px;
            margin-bottom: 40px;
            text-transform: uppercase;
        }

        /* Menú de navegación horizontal (Radio buttons modificados) */
        .stRadio > div[role="radiogroup"] {
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
            padding-bottom: 30px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 30px;
        }
        .stRadio > div[role="radiogroup"] > label {
            background: transparent !important;
            border: 1px solid rgba(139, 92, 246, 0.5);
            border-radius: 30px;
            padding: 10px 25px;
            color: var(--text-muted) !important;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        .stRadio > div[role="radiogroup"] > label:hover {
            border-color: var(--neon-green);
            color: var(--neon-green) !important;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
        }
        .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
            background: rgba(139, 92, 246, 0.1) !important;
            border-color: var(--neon-purple);
            color: var(--neon-purple) !important;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
        }

        /* Títulos secundarios */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            color: var(--text-light) !important;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        h2 { border-left: 4px solid var(--neon-purple); padding-left: 15px; }

        /* Tarjetas de Métricas */
        [data-testid="stMetric"] {
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 20px;
            padding: 20px;
            text-align: center;
        }
        [data-testid="stMetricLabel"] { 
            color: var(--text-muted) !important; 
            font-family: 'Space Mono', monospace; 
            font-size: 0.9rem;
        }
        [data-testid="stMetricValue"] {
            color: var(--neon-green) !important;
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
        }

        /* Tablas de Datos */
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 15px;
            background: rgba(0,0,0,0.5);
            padding: 10px;
        }

        /* Pestañas (Tabs) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 15px;
            background: transparent;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Orbitron', sans-serif;
            color: var(--text-muted);
            border: none;
            background: transparent;
            padding-bottom: 10px;
        }
        .stTabs [aria-selected="true"] {
            color: var(--neon-purple) !important;
            border-bottom: 2px solid var(--neon-purple) !important;
        }
        
        /* Alertas de sistema */
        .stAlert { background: rgba(0,0,0,0.6); border-radius: 15px; border: 1px solid; }
        .stAlert[data-baseweb="alert-info"] { border-color: #3b82f6; }
        .stAlert[data-baseweb="alert-success"] { border-color: var(--neon-green); }
        .stAlert[data-baseweb="alert-error"] { border-color: #ef4444; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SUPERIOR ---
st.markdown("""
    <div class="header-title">ANÁLISIS DE DATOS</div>
    <div class="header-subtitle">FES ARAGÓN // SISTEMA CENTRAL</div>
""", unsafe_allow_html=True)

# --- MENÚ DE NAVEGACIÓN ---
opciones_menu = ["Vista General", "Lista Limpia", "Indice de Materias", "Ranking de Carreras", "Tendencias Semestre", "Riesgo Academico"]
menu = st.radio("Navegación", opciones_menu, horizontal=True, label_visibility="collapsed")

# --- SECCIÓN: VISTA GENERAL ---
if menu == "Vista General":
    st.subheader("PORTAL DE DATOS")
    st.write("Explora el comportamiento académico de la facultad. Reportes dinámicos generados a partir de los registros del sistema central.")
    col1, col2 = st.columns(2)
    with col1:
        st.info("ANALISIS DE TENDENCIAS: Modulo de evolucion historica activo.")
    with col2:
        st.success("ESTADO DEL SISTEMA: Sincronizado. Conexión estable.")

# --- SECCIÓN: LISTA LIMPIA ---
elif menu == "Lista Limpia":
    st.header("DATOS ESTANDARIZADOS")
    try:
        df_limpio = pd.read_csv('limpieza1.csv')
        st.metric("TOTAL DE REGISTROS", len(df_limpio))
        st.dataframe(df_limpio, use_container_width=True)
    except FileNotFoundError:
        st.error("ARCHIVO NO ENCONTRADO: limpieza1.csv. Ejecute Limpieza1.py")

# --- SECCIÓN: INDICE DE MATERIAS (GRÁFICAS POR AÑO) ---
elif menu == "Indice de Materias":
    st.header("INDICE DE REPROBACION")
    try:
        df_ind = pd.read_csv('IndiceMaterias.csv')
        
        with st.expander("VER MATRIZ DE DATOS"):
            st.dataframe(df_ind, use_container_width=True)
        
        st.subheader("TENDENCIA ANUAL")
        col_graf1, col_graf2, col_graf3 = st.columns(3)
        
        años_columnas = [col for col in df_ind.columns if col not in ['materia', 'alumnos_reprobados']]
        
        with col_graf1:
            if '2022' in años_columnas:
                st.caption("CICLO 2022")
                st.bar_chart(data=df_ind, x='materia', y='2022', color="#8b5cf6")
        
        with col_graf2:
            if '2023' in años_columnas:
                st.caption("CICLO 2023")
                st.bar_chart(data=df_ind, x='materia', y='2023', color="#8b5cf6")
                
        with col_graf3:
            if '2024' in años_columnas:
                st.caption("CICLO 2024")
                st.bar_chart(data=df_ind, x='materia', y='2024', color="#8b5cf6")

        st.markdown("---")
        st.subheader("CONSOLIDADO HISTORICO")
        st.bar_chart(data=df_ind, x='materia', y='alumnos_reprobados', color="#10b981")
        
    except FileNotFoundError:
        st.error("ARCHIVO NO ENCONTRADO: IndiceMaterias.csv")

# --- SECCIÓN: RANKING DE CARRERAS ---
elif menu == "Ranking de Carreras":
    st.header("RENDIMIENTO POR CARRERA")
    try:
        df_prom = pd.read_csv('PromedioCarreras.csv')
        df_prom.columns = [c.lower() for c in df_prom.columns]
        col_año = 'año' if 'año' in df_prom.columns else 'anio'
        
        años_disponibles = sorted(df_prom[col_año].unique(), reverse=True)
        año_sel = st.selectbox("SELECCIONAR CICLO:", años_disponibles)
        df_filtrado = df_prom[df_prom[col_año] == año_sel]
        
        col_t, col_g = st.columns([1, 1])
        with col_t:
            st.dataframe(df_filtrado, use_container_width=True)
        with col_g:
            st.bar_chart(data=df_filtrado, x='carrera', y='promedio_calificacion', color="#8b5cf6")
    except FileNotFoundError:
        st.error("ARCHIVO NO ENCONTRADO: PromedioCarreras.csv")

# --- SECCIÓN: TENDENCIAS POR SEMESTRE ---
elif menu == "Tendencias Semestre":
    st.header("EVOLUCION ACADEMICA")
    try:
        df_tend = pd.read_csv('TendenciasSemestre.csv')
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("PROMEDIO GLOBAL", f"{df_tend['Promedio_General'].mean():.2f}")
        col_m2.metric("POBLACION ACTIVA", int(df_tend['Total_Alumnos'].sum()))
        
        tab1, tab2 = st.tabs(["PROMEDIO", "POBLACION"])
        with tab1:
            st.line_chart(data=df_tend, x='Semestre', y='Promedio_General', color="#8b5cf6")
        with tab2:
            st.area_chart(data=df_tend, x='Semestre', y='Total_Alumnos', color="#10b981")
    except FileNotFoundError:
        st.error("ARCHIVO NO ENCONTRADO: TendenciasSemestre.csv")

# --- SECCIÓN: ALUMNOS EN RIESGO ---
elif menu == "Riesgo Academico":
    st.header("ALERTA DE RENDIMIENTO")
    
    try:
        df_riesgo = pd.read_csv('RiesgoAlumno.csv')
        col_anio = 'año' if 'año' in df_riesgo.columns else 'anio'
        
        tab2022, tab2023, tab2024 = st.tabs(["CICLO 2022", "CICLO 2023", "CICLO 2024"])
        
        with tab2022:
            st.subheader("REGISTROS 2022")
            datos_2022 = df_riesgo[df_riesgo[col_anio] == 2022]
            st.metric("CASOS DETECTADOS", len(datos_2022))
            st.dataframe(datos_2022, use_container_width=True)
            
        with tab2023:
            st.subheader("REGISTROS 2023")
            datos_2023 = df_riesgo[df_riesgo[col_anio] == 2023]
            st.metric("CASOS DETECTADOS", len(datos_2023))
            st.dataframe(datos_2023, use_container_width=True)
            
        with tab2024:
            st.subheader("REGISTROS 2024")
            datos_2024 = df_riesgo[df_riesgo[col_anio] == 2024]
            st.metric("CASOS DETECTADOS", len(datos_2024))
            st.dataframe(datos_2024, use_container_width=True)

    except FileNotFoundError:
        st.error("ARCHIVO NO ENCONTRADO: RiesgoAlumno.csv")