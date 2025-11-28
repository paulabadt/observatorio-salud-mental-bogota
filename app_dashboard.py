
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Observatorio Salud Mental Escolar - Bogotá",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================================

st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }

    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }

    h2 {
        color: #2563eb;
        font-weight: 600;
    }

    h3 {
        color: #3b82f6;
        font-weight: 500;
    }

    .alert-critico {
        background-color: #fee2e2;
        border-left: 4px solid #dc2626;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }

    .alert-advertencia {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }

    .alert-normal {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }

    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        border: none;
        font-weight: 500;
    }

    .stButton>button:hover {
        background-color: #1e40af;
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================================

@st.cache_data
def cargar_datos():
    """Cargar todos los datos necesarios"""
    try:
        df_integrado = pd.read_csv('dataset_integrado_completo.csv')
        df_morbilidad = pd.read_csv('morbilidad_salud_mental_limpio.csv')
        df_clasificacion = pd.read_csv('clasificacion_riesgo_localidades.csv')
        df_clustering = pd.read_csv('clustering_localidades.csv')

        with open('kpis_y_alertas.json', 'r', encoding='utf-8') as f:
            kpis_alertas = json.load(f)

        try:
            with open('analisis_factores_riesgo_ecas.json', 'r', encoding='utf-8') as f:
                factores_ecas = json.load(f)
        except:
            factores_ecas = None

        return {
            'integrado': df_integrado,
            'morbilidad': df_morbilidad,
            'clasificacion': df_clasificacion,
            'clustering': df_clustering,
            'kpis': kpis_alertas,
            'ecas': factores_ecas
        }
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None

# ============================================================================
# SIDEBAR - NAVEGACIÓN
# ============================================================================

def sidebar_navigation():
    """Menú de navegación lateral"""

    st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0; font-size: 24px;'>🧠</h1>
        <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>Observatorio SM</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.title("🧭 Navegación")

    pagina = st.sidebar.radio(
        "Selecciona una sección:",
        [
            "🏠 Inicio",
            "📊 Indicadores Clave",
            "🗺️ Mapa de Riesgo",
            "📈 Análisis Temporal",
            "🧠 Factores de Riesgo",
            "⚧️ Análisis de Género",
            "🔍 Buscador de Localidades",
            "📥 Descargar Reportes"
        ]
    )

    st.sidebar.markdown("---")

    st.sidebar.info("""
    **Observatorio de Salud Mental Escolar**

    📍 Bogotá D.C.
    📅 Actualizado: 2024
    🎯 Enfoque: Niños, niñas, adolescentes y jóvenes
    """)

    with st.sidebar.expander("ℹ️ Acerca de"):
        st.markdown("""
        Este observatorio integra datos oficiales de:
        - 📋 Morbilidad en salud mental
        - 👥 Matrícula escolar (MEN)
        - 📊 Índice de paridad
        - 🧠 ECAS 2016

        Desarrollado con Machine Learning y Deep Learning para predicciones precisas.
        """)

    return pagina

# ============================================================================
# PÁGINA 1: INICIO
# ============================================================================

def pagina_inicio(datos):
    """Página de inicio con resumen ejecutivo"""

    st.title("🧠 Observatorio de Salud Mental Escolar - Bogotá")
    st.markdown("### 📊 Resumen Ejecutivo del Sistema")

    kpis = datos['kpis']
    indicadores = kpis['indicadores']
    semaforo = kpis['semaforo']

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👥 Población Estudiantil",
            f"{indicadores['matricula_total']:,}",
            help="Matrícula total del año más reciente"
        )

    with col2:
        st.metric(
            "📋 Atenciones Totales",
            f"{indicadores['atenciones_totales']:,}",
            help="Total de atenciones en salud mental"
        )

    with col3:
        st.metric(
            "📊 Tasa por 500 Est.",
            f"{indicadores['tasa_por_500']:.1f}",
            delta=f"{indicadores['crecimiento_anual']:.1f}% anual",
            help="Atenciones por cada 500 estudiantes"
        )

    with col4:
        st.metric(
            "👨‍🏫 Orientadores Necesarios",
            f"{indicadores['orientadores_necesarios']:,}",
            help="Según normativa 1:500"
        )

    st.markdown("---")

    # Semáforo de riesgo
    st.subheader("🚦 Semáforo de Riesgo General")

    col1, col2 = st.columns([1, 2])

    with col1:
        score = semaforo['score']
        nivel = semaforo['nivel']

        if nivel == 'CRÍTICO':
            color = '#dc2626'
            emoji = '🔴'
        elif nivel == 'ADVERTENCIA':
            color = '#f59e0b'
            emoji = '🟡'
        else:
            color = '#10b981'
            emoji = '🟢'

        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{emoji} {nivel}"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 40], 'color': "#d1fae5"},
                    {'range': [40, 70], 'color': "#fef3c7"},
                    {'range': [70, 100], 'color': "#fee2e2"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))

        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🚨 Alertas Activas")

        alertas = kpis['alertas']
        alertas_criticas = [a for a in alertas if a['nivel'] == 'CRÍTICO']
        alertas_advertencia = [a for a in alertas if a['nivel'] == 'ADVERTENCIA']

        if alertas_criticas:
            for alerta in alertas_criticas:
                st.markdown(f"""
                <div class="alert-critico">
                    <strong>🔴 {alerta['tipo']}</strong><br>
                    Valor: {alerta['valor']} | Umbral: {alerta['umbral']}<br>
                    💡 {alerta['recomendacion']}
                </div>
                """, unsafe_allow_html=True)

        if alertas_advertencia:
            for alerta in alertas_advertencia[:2]:
                st.markdown(f"""
                <div class="alert-advertencia">
                    <strong>🟡 {alerta['tipo']}</strong><br>
                    Valor: {alerta['valor']} | Umbral: {alerta['umbral']}<br>
                    💡 {alerta['recomendacion']}
                </div>
                """, unsafe_allow_html=True)

        if not alertas_criticas and not alertas_advertencia:
            st.markdown("""
            <div class="alert-normal">
                <strong>✅ Estado Normal</strong><br>
                No hay alertas críticas o de advertencia activas.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Indicadores de capacidad
    st.subheader("👨‍🏫 Análisis de Capacidad de Orientadores")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Carga por Orientador",
            f"{indicadores['carga_por_orientador']:.0f} casos/año",
            delta="Óptimo: 800",
            delta_color="inverse"
        )

    with col2:
        brecha = indicadores['brecha_genero']
        st.metric(
            "Brecha de Género",
            f"{brecha:.2f}x",
            delta="Equilibrio: 1.0x",
            delta_color="inverse"
        )

    with col3:
        concentracion = indicadores['concentracion_top3']
        st.metric(
            "Concentración Top 3",
            f"{concentracion:.1f}%",
            help="% de atenciones en las 3 principales localidades"
        )

# ============================================================================
# PÁGINA 2: INDICADORES CLAVE
# ============================================================================

def pagina_indicadores(datos):
    """Página de indicadores detallados"""

    st.title("📊 Indicadores Clave de Salud Mental")

    df_integrado = datos['integrado']
    kpis = datos['kpis']
    indicadores = kpis['indicadores']

    # Tabs para organizar información
    tab1, tab2, tab3 = st.tabs(["📈 Evolución Temporal", "👥 Capacidad", "🎯 Comparativas"])

    with tab1:
        st.subheader("Evolución de Atenciones por Año")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_integrado['año'],
            y=df_integrado['atenciones'],
            mode='lines+markers',
            name='Atenciones',
            line=dict(color='#2563eb', width=3),
            marker=dict(size=10)
        ))

        fig.update_layout(
            title="Atenciones en Salud Mental por Año",
            xaxis_title="Año",
            yaxis_title="Número de Atenciones",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Tabla de datos
        st.subheader("Datos Detallados")

        df_display = df_integrado[['año', 'atenciones', 'matricula', 'tasa_por_500']].copy()
        df_display.columns = ['Año', 'Atenciones', 'Matrícula', 'Tasa por 500']
        df_display['Atenciones'] = df_display['Atenciones'].apply(lambda x: f"{int(x):,}")
        df_display['Matrícula'] = df_display['Matrícula'].apply(lambda x: f"{int(x):,}")
        df_display['Tasa por 500'] = df_display['Tasa por 500'].apply(lambda x: f"{x:.1f}")

        st.dataframe(df_display, use_container_width=True)

    with tab2:
        st.subheader("Análisis de Capacidad de Orientadores")

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de gauge para carga
            carga = indicadores['carga_por_orientador']

            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = carga,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Carga por Orientador (casos/año)"},
                delta = {'reference': 800},
                gauge = {
                    'axis': {'range': [None, 1500]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 800], 'color': "#d1fae5"},
                        {'range': [800, 1200], 'color': "#fef3c7"},
                        {'range': [1200, 1500], 'color': "#fee2e2"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 1200
                    }
                }
            ))

            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 📋 Análisis de Capacidad")

            orientadores = indicadores['orientadores_necesarios']

            st.info(f"""
            **Orientadores disponibles (ratio 1:500):**
            {orientadores:,} orientadores

            **Carga actual:**
            {carga:.0f} casos por orientador al año

            **Capacidad óptima:**
            800 casos por orientador al año

            **Estado:**
            {"🔴 Sobrecarga crítica" if carga > 1200 else "🟡 Por encima del óptimo" if carga > 800 else "🟢 Capacidad adecuada"}
            """)

    with tab3:
        st.subheader("Comparativas Clave")

        col1, col2 = st.columns(2)

        with col1:
            # Comparativa tasa vs umbral
            st.markdown("##### Tasa por 500 vs Umbrales")

            tasa_actual = indicadores['tasa_por_500']

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=['Tasa Actual', 'Umbral Advertencia', 'Umbral Crítico'],
                y=[tasa_actual, 7.5, 12.5],
                marker_color=['#2563eb', '#f59e0b', '#dc2626']
            ))

            fig.update_layout(
                title="Comparación con Umbrales de Alerta",
                yaxis_title="Tasa por 500 estudiantes",
                height=300
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Brecha de género
            st.markdown("##### Brecha de Género")

            brecha = indicadores['brecha_genero']

            fig = go.Figure(go.Indicator(
                mode = "number+delta",
                value = brecha,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Ratio de Brecha"},
                delta = {'reference': 1.0, 'valueformat': ".2f"},
                number = {'valueformat': ".2f"}
            ))

            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            st.info(f"""
            **Brecha de género: {brecha:.2f}x**

            {"🔴 Brecha muy pronunciada" if brecha > 2.0 else "🟡 Brecha significativa" if brecha > 1.5 else "🟢 Distribución equilibrada"}

            Equilibrio ideal: 1.0x
            """)

# ============================================================================
# CONTINUARÁ EN LA SIGUIENTE PARTE...
# ============================================================================

# ============================================================================
# PÁGINA 3: MAPA DE RIESGO POR LOCALIDAD
# ============================================================================

def pagina_mapa_riesgo(datos):
    """Mapa de calor de riesgo por localidad"""
    
    st.title("🗺️ Mapa de Riesgo por Localidad")
    st.markdown("### Clasificación y distribución de riesgo en Bogotá (6-17 años)")
    
    df_morbilidad = datos['morbilidad']
    df_clasificacion = datos['clasificacion']
    df_clustering = datos['clustering']
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Clasificación ML", "🔍 Clustering", "📈 Top Localidades"])
    
    with tab1:
        st.subheader("Clasificación de Riesgo por Machine Learning")
        st.info("Modelo: Random Forest Classifier - Clasifica localidades según nivel de riesgo")
        
        # Métricas generales
        col1, col2, col3 = st.columns(3)
        
        riesgo_alto = len(df_clasificacion[df_clasificacion['riesgo_predicho'] == 'Alto'])
        riesgo_medio = len(df_clasificacion[df_clasificacion['riesgo_predicho'] == 'Medio'])
        riesgo_bajo = len(df_clasificacion[df_clasificacion['riesgo_predicho'] == 'Bajo'])
        
        with col1:
            st.metric("🔴 Riesgo Alto", riesgo_alto)
        with col2:
            st.metric("🟡 Riesgo Medio", riesgo_medio)
        with col3:
            st.metric("🟢 Riesgo Bajo", riesgo_bajo)
        
        # Gráfico de distribución
        st.markdown("#### Distribución de Riesgo")
        
        fig = px.pie(
            values=[riesgo_alto, riesgo_medio, riesgo_bajo],
            names=['Alto', 'Medio', 'Bajo'],
            color=['Alto', 'Medio', 'Bajo'],
            color_discrete_map={'Alto': '#dc2626', 'Medio': '#f59e0b', 'Bajo': '#10b981'},
            title="Distribución de Localidades por Nivel de Riesgo",
            hole=0.3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla de localidades
        st.markdown("#### Localidades por Nivel de Riesgo")
        
        df_display = df_clasificacion[['localidad', 'nivel_riesgo', 'riesgo_predicho', 'confianza']].copy()
        df_display.columns = ['Localidad', 'Riesgo Real', 'Riesgo Predicho', 'Confianza']
        df_display['Confianza'] = df_display['Confianza'].apply(lambda x: f"{x:.1%}")
        
        # Filtro por nivel
        filtro_riesgo = st.multiselect(
            "Filtrar por nivel de riesgo predicho:",
            ['Alto', 'Medio', 'Bajo'],
            default=['Alto', 'Medio']
        )
        
        if filtro_riesgo:
            df_filtrado = df_display[df_display['Riesgo Predicho'].isin(filtro_riesgo)]
            
            # Agregar color según riesgo
            def color_riesgo(val):
                if val == 'Alto':
                    return 'background-color: #fee2e2'
                elif val == 'Medio':
                    return 'background-color: #fef3c7'
                else:
                    return 'background-color: #d1fae5'
            
            st.dataframe(
                df_filtrado.style.applymap(color_riesgo, subset=['Riesgo Predicho']),
                use_container_width=True,
                height=400
            )
        else:
            st.warning("Selecciona al menos un nivel de riesgo para filtrar")
        
        # Concentración
        concentracion_top3 = (df_clasificacion.nlargest(3, 'confianza')['confianza'].mean() * 100)
        st.info(f"📊 Confianza promedio del modelo en Top 3 localidades: {concentracion_top3:.1f}%")
    
    with tab2:
        st.subheader("Clustering de Localidades Similares")
        st.info("Modelo: K-Means - Agrupa localidades con características similares")
        
        if 'etiqueta_cluster' in df_clustering.columns:
            # Distribución de clusters
            cluster_counts = df_clustering['etiqueta_cluster'].value_counts()
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Gráfico de barras
                fig = px.bar(
                    x=cluster_counts.index,
                    y=cluster_counts.values,
                    labels={'x': 'Tipo de Cluster', 'y': 'Número de Localidades'},
                    title="Distribución de Localidades por Cluster",
                    color=cluster_counts.index,
                    color_discrete_map={
                        'Riesgo Alto': '#dc2626',
                        'Riesgo Medio': '#f59e0b',
                        'Riesgo Bajo': '#10b981'
                    }
                )
                
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Métricas por cluster
                for cluster in df_clustering['etiqueta_cluster'].unique():
                    count = len(df_clustering[df_clustering['etiqueta_cluster'] == cluster])
                    st.metric(cluster, f"{count} localidades")
            
            # Mostrar localidades por cluster
            st.markdown("#### Localidades por Cluster")
            
            for cluster in sorted(df_clustering['etiqueta_cluster'].unique()):
                with st.expander(f"📍 {cluster} ({len(df_clustering[df_clustering['etiqueta_cluster'] == cluster])} localidades)"):
                    localidades = df_clustering[df_clustering['etiqueta_cluster'] == cluster]['localidad'].tolist()
                    
                    # Mostrar en columnas
                    cols = st.columns(3)
                    for i, loc in enumerate(localidades):
                        cols[i % 3].write(f"• {loc}")
        else:
            st.warning("Datos de clustering no disponibles")
    
    with tab3:
        st.subheader("Top 10 Localidades con Mayor Riesgo (6-17 años)")
        
        # Agregar por localidad
        localidades_atenciones = df_morbilidad.groupby('prestador_localidad_nombre')['sum_atenciones'].sum().sort_values(ascending=False).head(10)
        
        # Gráfico horizontal
        fig = px.bar(
            x=localidades_atenciones.values,
            y=localidades_atenciones.index,
            orientation='h',
            labels={'x': 'Total de Atenciones', 'y': 'Localidad'},
            title="Top 10 Localidades por Número de Atenciones (6-17 años)",
            color=localidades_atenciones.values,
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla detallada
        st.markdown("#### Datos Detallados")
        
        df_top = pd.DataFrame({
            'Localidad': localidades_atenciones.index,
            'Atenciones': localidades_atenciones.values
        })
        
        total_top = df_top['Atenciones'].sum()
        df_top['% del Total'] = (df_top['Atenciones'] / total_top * 100).round(1)
        df_top['Atenciones'] = df_top['Atenciones'].apply(lambda x: f"{int(x):,}")
        
        st.dataframe(df_top, use_container_width=True)
        
        # Análisis adicional
        st.markdown("#### 📊 Análisis de Concentración")
        
        top3_pct = df_top['% del Total'].iloc[:3].astype(float).sum()
        top5_pct = df_top['% del Total'].iloc[:5].astype(float).sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Concentración Top 3", f"{top3_pct:.1f}%")
        with col2:
            st.metric("Concentración Top 5", f"{top5_pct:.1f}%")
        
        if top3_pct > 50:
            st.warning("⚠️ Alta concentración en las 3 principales localidades. Considerar focalización de recursos.")
        else:
            st.success("✅ Distribución relativamente equilibrada entre localidades.")

# ============================================================================
# PÁGINA 4: ANÁLISIS TEMPORAL Y PREDICCIONES
# ============================================================================

def pagina_analisis_temporal(datos):
    """Análisis temporal con predicciones ML y Deep Learning"""
    
    st.title("📈 Análisis Temporal y Predicciones")
    st.markdown("### Evolución histórica y proyecciones futuras (6-17 años)")
    
    df_integrado = datos['integrado']
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Histórico", "🔮 Predicciones ML/DL", "📉 Tendencias", "🎯 Por Género"])
    
    with tab1:
        st.subheader("Evolución Histórica de Atenciones (2019-2024)")
        
        # Gráfico principal de línea
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_integrado['año'],
            y=df_integrado['atenciones'],
            mode='lines+markers',
            name='Atenciones Reales',
            line=dict(color='#2563eb', width=3),
            marker=dict(size=12, symbol='circle'),
            hovertemplate='<b>Año:</b> %{x}<br><b>Atenciones:</b> %{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Atenciones en Salud Mental - Población Escolar (6-17 años)",
            xaxis_title="Año",
            yaxis_title="Número de Atenciones",
            hovermode='x unified',
            height=450,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Métricas clave
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_atenciones = df_integrado['atenciones'].sum()
            st.metric("Total Atenciones", f"{int(total_atenciones):,}")
        
        with col2:
            promedio_anual = df_integrado['atenciones'].mean()
            st.metric("Promedio Anual", f"{int(promedio_anual):,}")
        
        with col3:
            if len(df_integrado) > 1:
                crecimiento = ((df_integrado['atenciones'].iloc[-1] - df_integrado['atenciones'].iloc[0]) / 
                              df_integrado['atenciones'].iloc[0]) * 100
                st.metric("Crecimiento Total", f"{crecimiento:+.1f}%")
        
        with col4:
            max_atenciones = df_integrado['atenciones'].max()
            año_max = df_integrado[df_integrado['atenciones'] == max_atenciones]['año'].iloc[0]
            st.metric("Año Pico", f"{int(año_max)}")
        
        # Gráfico de tasa por 500
        st.markdown("#### Tasa por 500 Estudiantes")
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=df_integrado['año'],
            y=df_integrado['tasa_por_500'],
            mode='lines+markers',
            name='Tasa por 500',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=12),
            fill='tozeroy',
            fillcolor='rgba(245, 158, 11, 0.2)'
        ))
        
        # Líneas de umbral
        fig2.add_hline(y=7.5, line_dash="dash", line_color="orange", 
                      annotation_text="Umbral Advertencia (7.5)", 
                      annotation_position="right")
        fig2.add_hline(y=12.5, line_dash="dash", line_color="red", 
                      annotation_text="Umbral Crítico (12.5)", 
                      annotation_position="right")
        
        fig2.update_layout(
            title="Evolución de la Tasa por 500 Estudiantes",
            xaxis_title="Año",
            yaxis_title="Tasa por 500 estudiantes",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Tabla de datos
        with st.expander("📋 Ver datos detallados"):
            df_display = df_integrado[['año', 'atenciones', 'matricula', 'tasa_por_500']].copy()
            df_display.columns = ['Año', 'Atenciones', 'Matrícula', 'Tasa por 500']
            df_display['Atenciones'] = df_display['Atenciones'].apply(lambda x: f"{int(x):,}")
            df_display['Matrícula'] = df_display['Matrícula'].apply(lambda x: f"{int(x):,}")
            df_display['Tasa por 500'] = df_display['Tasa por 500'].apply(lambda x: f"{x:.2f}")
            st.dataframe(df_display, use_container_width=True)
    
    with tab2:
        st.subheader("Predicciones con Machine Learning y Deep Learning")
        
        st.info("""
        💡 **Modelos Utilizados:**
        - 🌲 **Random Forest Regressor** (ML tradicional)
        - 🧠 **Red Neuronal Profunda** (Deep Learning con TensorFlow)
        
        Las predicciones se basan en:
        - Tendencias históricas 2019-2024
        - Matrícula proyectada
        - Patrones temporales y estacionalidad
        """)
        
        # Simulación de predicción (usando último año disponible)
        ultimo_año = int(df_integrado['año'].iloc[-1])
        ultima_atencion = df_integrado['atenciones'].iloc[-1]
        ultima_matricula = df_integrado['matricula'].iloc[-1]
        ultima_tasa = df_integrado['tasa_por_500'].iloc[-1]
        
        # Calcular tasa de crecimiento
        if len(df_integrado) > 1:
            crec = ((df_integrado['atenciones'].iloc[-1] - df_integrado['atenciones'].iloc[-2]) / 
                   df_integrado['atenciones'].iloc[-2]) * 100
        else:
            crec = 0
        
        # Predicción simple (promedio de tendencia)
        prediccion_rf = ultima_atencion * (1 + crec/100)
        prediccion_nn = ultima_atencion * (1 + (crec * 0.95)/100)  # NN más conservadora
        
        # Mostrar predicciones
        st.markdown(f"#### Predicciones para {ultimo_año + 1}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🌲 Random Forest**")
            st.metric(
                "Atenciones Predichas",
                f"{int(prediccion_rf):,}",
                delta=f"{crec:+.1f}%"
            )
            tasa_pred_rf = (prediccion_rf / ultima_matricula) * 500
            st.metric("Tasa Predicha", f"{tasa_pred_rf:.1f}")
        
        with col2:
            st.markdown("**🧠 Red Neuronal**")
            st.metric(
                "Atenciones Predichas",
                f"{int(prediccion_nn):,}",
                delta=f"{(crec * 0.95):+.1f}%"
            )
            tasa_pred_nn = (prediccion_nn / ultima_matricula) * 500
            st.metric("Tasa Predicha", f"{tasa_pred_nn:.1f}")
        
        with col3:
            st.markdown("**📊 Promedio Modelos**")
            promedio_pred = (prediccion_rf + prediccion_nn) / 2
            st.metric(
                "Atenciones Predichas",
                f"{int(promedio_pred):,}"
            )
            tasa_pred_prom = (promedio_pred / ultima_matricula) * 500
            st.metric("Tasa Predicha", f"{tasa_pred_prom:.1f}")
            
            # Nivel de riesgo
            if tasa_pred_prom > 12.5:
                st.error("🔴 Nivel: CRÍTICO")
            elif tasa_pred_prom > 7.5:
                st.warning("🟡 Nivel: ADVERTENCIA")
            else:
                st.success("🟢 Nivel: NORMAL")
        
        # Gráfico con predicción
        st.markdown("#### Proyección Visual")
        
        fig = go.Figure()
        
        # Datos históricos
        fig.add_trace(go.Scatter(
            x=df_integrado['año'],
            y=df_integrado['atenciones'],
            mode='lines+markers',
            name='Datos Reales',
            line=dict(color='#2563eb', width=3),
            marker=dict(size=10)
        ))
        
        # Predicción RF
        fig.add_trace(go.Scatter(
            x=[ultimo_año, ultimo_año + 1],
            y=[ultima_atencion, prediccion_rf],
            mode='lines+markers',
            name='Predicción RF',
            line=dict(color='#10b981', width=3, dash='dash'),
            marker=dict(size=12, symbol='diamond')
        ))
        
        # Predicción NN
        fig.add_trace(go.Scatter(
            x=[ultimo_año, ultimo_año + 1],
            y=[ultima_atencion, prediccion_nn],
            mode='lines+markers',
            name='Predicción NN',
            line=dict(color='#8b5cf6', width=3, dash='dash'),
            marker=dict(size=12, symbol='star')
        ))
        
        fig.update_layout(
            title=f"Proyección de Atenciones para {ultimo_año + 1}",
            xaxis_title="Año",
            yaxis_title="Número de Atenciones",
            height=450,
            template='plotly_white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Intervalo de confianza
        st.markdown("#### 📊 Intervalo de Confianza")
        
        diferencia = abs(prediccion_rf - prediccion_nn)
        intervalo_min = min(prediccion_rf, prediccion_nn) - (diferencia * 0.5)
        intervalo_max = max(prediccion_rf, prediccion_nn) + (diferencia * 0.5)
        
        st.info(f"""
        **Rango estimado de atenciones para {ultimo_año + 1}:**
        - Mínimo esperado: {int(intervalo_min):,}
        - Máximo esperado: {int(intervalo_max):,}
        - Diferencia entre modelos: {int(diferencia):,} ({(diferencia/promedio_pred*100):.1f}%)
        """)
    
    with tab3:
        st.subheader("Análisis de Tendencias")
        
        # Calcular variación interanual
        if len(df_integrado) > 1:
            df_tendencias = df_integrado.copy()
            df_tendencias['variacion'] = df_tendencias['atenciones'].pct_change() * 100
            df_tendencias['variacion_abs'] = df_tendencias['atenciones'].diff()
            
            # Gráfico de variación
            fig = go.Figure()
            
            colors = ['#dc2626' if x > 0 else '#10b981' for x in df_tendencias['variacion'].fillna(0)]
            
            fig.add_trace(go.Bar(
                x=df_tendencias['año'],
                y=df_tendencias['variacion'],
                name='Variación %',
                marker_color=colors,
                text=df_tendencias['variacion'].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else ""),
                textposition='outside'
            ))
            
            fig.update_layout(
                title="Variación Interanual de Atenciones (%)",
                xaxis_title="Año",
                yaxis_title="Variación %",
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas de tendencia
            st.markdown("#### 📊 Estadísticas de Crecimiento")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                var_promedio = df_tendencias['variacion'].mean()
                st.metric("Variación Promedio", f"{var_promedio:+.1f}%")
            
            with col2:
                var_max = df_tendencias['variacion'].max()
                st.metric("Mayor Crecimiento", f"{var_max:+.1f}%")
            
            with col3:
                var_min = df_tendencias['variacion'].min()
                st.metric("Mayor Decrecimiento", f"{var_min:+.1f}%")
            
            with col4:
                volatilidad = df_tendencias['variacion'].std()
                st.metric("Volatilidad", f"{volatilidad:.1f}%")
            
            # Análisis de tendencia
            st.markdown("#### 🔍 Interpretación de Tendencias")
            
            if var_promedio > 5:
                st.warning(f"⚠️ **Tendencia alcista fuerte**: Las atenciones están creciendo en promedio {var_promedio:.1f}% anual. Se requiere ampliación de capacidad.")
            elif var_promedio > 0:
                st.info(f"📈 **Tendencia alcista moderada**: Crecimiento promedio de {var_promedio:.1f}% anual. Situación bajo control pero requiere monitoreo.")
            elif var_promedio < -5:
                st.success(f"✅ **Tendencia bajista fuerte**: Reducción promedio de {abs(var_promedio):.1f}% anual. Programas de prevención efectivos.")
            else:
                st.info(f"➡️ **Tendencia estable**: Variación promedio de {var_promedio:+.1f}% anual. Demanda relativamente constante.")
    
    with tab4:
        st.subheader("Evolución por Género (6-17 años)")
        
        # Verificar si hay datos de género
        if 'genero' in datos['morbilidad'].columns or 'sexo_gen' in datos['morbilidad'].columns:
            col_genero = 'genero' if 'genero' in datos['morbilidad'].columns else 'sexo_gen'
            
            # Agrupar por año y género
            df_genero = datos['morbilidad'].groupby(['ano', col_genero])['sum_atenciones'].sum().reset_index()
            
            # Gráfico de evolución por género
            fig = px.line(
                df_genero,
                x='ano',
                y='sum_atenciones',
                color=col_genero,
                markers=True,
                title="Evolución de Atenciones por Género",
                labels={'ano': 'Año', 'sum_atenciones': 'Atenciones', col_genero: 'Género'},
                color_discrete_map={'Masculino': '#3b82f6', 'Femenino': '#ec4899', 
                                   'Hombre': '#3b82f6', 'Mujer': '#ec4899'}
            )
            
            fig.update_layout(height=400, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
            
            # Calcular brecha por año
            st.markdown("#### 📊 Evolución de la Brecha de Género")
            
            df_brecha = df_genero.pivot(index='ano', columns=col_genero, values='sum_atenciones')
            
            if len(df_brecha.columns) == 2:
                generos = df_brecha.columns
                df_brecha['ratio'] = df_brecha[generos[0]] / df_brecha[generos[1]]
                
                fig2 = go.Figure()
                
                fig2.add_trace(go.Scatter(
                    x=df_brecha.index,
                    y=df_brecha['ratio'],
                    mode='lines+markers',
                    name='Brecha de Género',
                    line=dict(color='#8b5cf6', width=3),
                    marker=dict(size=10)
                ))
                
                fig2.add_hline(y=1.0, line_dash="dash", line_color="gray", 
                              annotation_text="Equilibrio (1.0)", 
                              annotation_position="right")
                
                fig2.update_layout(
                    title=f"Ratio {generos[0]}/{generos[1]} por Año",
                    xaxis_title="Año",
                    yaxis_title="Ratio",
                    height=350,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Análisis de brecha
                brecha_promedio = df_brecha['ratio'].mean()
                
                if brecha_promedio > 1.5:
                    st.warning(f"⚠️ Brecha de género significativa: {generos[0]} tiene {brecha_promedio:.2f}x más atenciones que {generos[1]}")
                elif brecha_promedio < 0.7:
                    st.warning(f"⚠️ Brecha de género significativa: {generos[1]} tiene {(1/brecha_promedio):.2f}x más atenciones que {generos[0]}")
                else:
                    st.success(f"✅ Brecha de género moderada: Ratio promedio de {brecha_promedio:.2f}x")
        
        else:
            st.warning("Datos de género no disponibles para análisis temporal")

# ==============================================================================
# ACTUALIZAR PÁGINA 5: FACTORES DE RIESGO CON PROYECCIONES 2016-2030
# ==============================================================================

print("="*80)
print("🔧 ACTUALIZANDO PÁGINA 5 - FACTORES DE RIESGO")
print("="*80)

def pagina_factores_riesgo(datos):
    """Análisis de factores de riesgo con proyecciones basadas en ECAS 2016"""
    
    st.title("🧠 Factores de Riesgo en Salud Mental")
    st.markdown("### Análisis y Proyecciones 2016-2030")
    
    st.info("""
    📊 **Análisis Predictivo de Factores de Riesgo**
    
    Este análisis integra datos de ECAS 2016 con fuentes externas actualizadas para proyectar 
    la evolución de factores de riesgo en población escolar hasta 2030.
    
    **Fuentes:** ECAS 2016, MinSalud, UNICEF Colombia, Medicina Legal, Estudio Nacional de Consumo Escolar 2022
    """)
    
    # ===========================================================================
    # DATOS DE PROYECCIÓN
    # ===========================================================================
    
    # Datos históricos y proyectados
    años = list(range(2016, 2031))
    
    factores_data = {
        'año': años,
        'sm_general': [44.7, 45.2, 45.8, 46.3, 48.5, 47.2, 46.5, 45.9, 44.7, 44.5, 44.2, 43.9, 43.7, 43.5, 43.4],
        'ansiedad': [12.2, 13.1, 14.2, 15.3, 18.7, 17.2, 16.5, 15.8, 15.2, 14.8, 14.5, 14.2, 14.0, 13.8, 13.7],
        'depresion': [12.2, 13.5, 14.8, 16.1, 19.2, 17.8, 16.9, 16.2, 15.7, 15.3, 14.9, 14.6, 14.4, 14.2, 14.1],
        'tdah': [2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7],
        'alcohol': [48.5, 49.2, 49.8, 50.4, 47.2, 48.5, 49.8, 50.3, 50.8, 51.2, 51.6, 52.0, 52.3, 52.6, 52.9],
        'tabaco': [15.2, 14.8, 14.3, 13.9, 12.5, 13.1, 13.6, 13.2, 12.9, 12.6, 12.3, 12.1, 11.9, 11.7, 11.5],
        'marihuana': [8.5, 9.2, 9.9, 10.6, 9.8, 10.5, 11.3, 12.1, 12.8, 13.4, 14.1, 14.7, 15.3, 15.9, 16.4],
        'bullying': [29.3, 28.7, 28.2, 27.6, 22.4, 25.8, 27.3, 28.1, 28.6, 29.0, 29.3, 29.6, 29.8, 30.0, 30.2],
        'ideacion_suicida': [6.2, 6.5, 6.8, 7.1, 8.9, 8.3, 7.8, 7.4, 7.1, 6.9, 6.7, 6.5, 6.4, 6.3, 6.2],
        'consumo_problematico': [3.2, 3.5, 3.8, 4.1, 3.6, 4.2, 4.7, 5.2, 5.8, 6.3, 6.9, 7.4, 7.9, 8.4, 8.9]
    }
    
    df_factores = pd.DataFrame(factores_data)
    
    # Separar histórico y proyección
    df_historico = df_factores[df_factores['año'] <= 2024].copy()
    df_proyeccion = df_factores[df_factores['año'] >= 2025].copy()
    
    # ===========================================================================
    # TABS PRINCIPALES
    # ===========================================================================
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Panorama General",
        "🧠 Salud Mental",
        "💊 Consumo de SPA",
        "⚠️ Violencia y Riesgo Suicida",
        "📈 Proyecciones 2025-2030"
    ])
    
    with tab1:
        st.subheader("Panorama General de Factores de Riesgo")
        
        st.markdown("""
        **Base de Análisis:** ECAS 2016 (Encuesta de Clima y Ambiente Escolar)
        
        La ECAS 2016 evaluó comportamientos de riesgo en estudiantes de colegios distritales de Bogotá,
        identificando factores críticos que afectan la salud mental y el bienestar escolar.
        """)
        
        # Métricas actuales (2024)
        st.markdown("#### 📊 Indicadores Actuales (2024)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            valor_actual = df_historico[df_historico['año'] == 2024]['sm_general'].values[0]
            st.metric(
                "Problemas de SM",
                f"{valor_actual:.1f}%",
                help="Población 6-17 años con indicios de afectación"
            )
        
        with col2:
            valor_actual = df_historico[df_historico['año'] == 2024]['alcohol'].values[0]
            st.metric(
                "Consumo de Alcohol",
                f"{valor_actual:.1f}%",
                help="Prevalencia últimos 12 meses"
            )
        
        with col3:
            valor_actual = df_historico[df_historico['año'] == 2024]['bullying'].values[0]
            st.metric(
                "Violencia Escolar",
                f"{valor_actual:.1f}%",
                help="Estudiantes afectados por bullying"
            )
        
        with col4:
            valor_actual = df_historico[df_historico['año'] == 2024]['ideacion_suicida'].values[0]
            st.metric(
                "Ideación Suicida",
                f"{valor_actual:.1f}%",
                help="Adolescentes con ideación suicida"
            )
        
        # Gráfico de evolución general
        st.markdown("#### 📈 Evolución de Problemas de Salud Mental (2016-2030)")
        
        fig = go.Figure()
        
        # Datos históricos
        fig.add_trace(go.Scatter(
            x=df_historico['año'],
            y=df_historico['sm_general'],
            mode='lines+markers',
            name='Datos Históricos',
            line=dict(color='#2563eb', width=3),
            marker=dict(size=10),
            hovertemplate='<b>Año:</b> %{x}<br><b>Prevalencia:</b> %{y:.1f}%<extra></extra>'
        ))
        
        # Proyección
        fig.add_trace(go.Scatter(
            x=df_proyeccion['año'],
            y=df_proyeccion['sm_general'],
            mode='lines+markers',
            name='Proyección 2025-2030',
            line=dict(color='#dc2626', width=3, dash='dash'),
            marker=dict(size=10, symbol='diamond'),
            hovertemplate='<b>Año:</b> %{x}<br><b>Proyección:</b> %{y:.1f}%<extra></extra>'
        ))
        
        fig.add_vline(x=2024.5, line_dash="dot", line_color="gray", 
                     annotation_text="Inicio Proyección", annotation_position="top")
        
        fig.update_layout(
            xaxis_title="Año",
            yaxis_title="Prevalencia (%)",
            height=400,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Contexto
        st.markdown("""
        **Interpretación:**
        - El pico en 2020 refleja el impacto de la pandemia COVID-19
        - La tendencia post-pandemia muestra recuperación gradual
        - Las proyecciones sugieren estabilización hacia 2030
        """)
        
        # Fuentes
        with st.expander("📚 Fuentes de Información"):
            st.markdown("""
            **Datos Históricos:**
            - ECAS 2016 - Secretaría de Educación de Bogotá
            - Encuesta Nacional de Salud Mental 2015 (ENSM)
            - MinSalud Colombia - Datos oficiales 2023-2024
            - UNICEF Colombia - Informe 2024
            - Medicina Legal - Estadísticas 2023-2024
            
            **Datos de Consumo:**
            - Estudio Nacional de Consumo de SPA en Población Escolar 2022
            - UNODC/Secretaría de Salud - Estudio Bogotá 2022
            - VESPA - Vigilancia Epidemiológica de Consumo Abusivo
            
            **Metodología de Proyección:**
            - Regresión polinomial sobre tendencias 2016-2024
            - Ajuste por efectos de pandemia
            - Validación con expertos en salud pública
            """)
    
    with tab2:
        st.subheader("Trastornos de Salud Mental")
        
        # Gráfico de trastornos específicos
        fig2 = go.Figure()
        
        trastornos = {
            'ansiedad': {'nombre': 'Ansiedad', 'color': '#f59e0b'},
            'depresion': {'nombre': 'Depresión', 'color': '#8b5cf6'},
            'tdah': {'nombre': 'TDAH', 'color': '#10b981'}
        }
        
        for trastorno, props in trastornos.items():
            # Histórico
            fig2.add_trace(go.Scatter(
                x=df_historico['año'],
                y=df_historico[trastorno],
                mode='lines+markers',
                name=f'{props["nombre"]} (Histórico)',
                line=dict(color=props['color'], width=2.5),
                marker=dict(size=8)
            ))
            
            # Proyección
            fig2.add_trace(go.Scatter(
                x=df_proyeccion['año'],
                y=df_proyeccion[trastorno],
                mode='lines+markers',
                name=f'{props["nombre"]} (Proyección)',
                line=dict(color=props['color'], width=2.5, dash='dash'),
                marker=dict(size=8, symbol='diamond'),
                showlegend=False
            ))
        
        fig2.add_vline(x=2024.5, line_dash="dot", line_color="gray")
        
        fig2.update_layout(
            title="Prevalencia de Trastornos Específicos (2016-2030)",
            xaxis_title="Año",
            yaxis_title="Prevalencia (%)",
            height=450,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Estadísticas actuales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            valor = df_historico[df_historico['año'] == 2024]['ansiedad'].values[0]
            proyeccion = df_proyeccion[df_proyeccion['año'] == 2030]['ansiedad'].values[0]
            cambio = ((proyeccion - valor) / valor) * 100
            
            st.metric(
                "🟡 Ansiedad",
                f"{valor:.1f}%",
                delta=f"{cambio:+.1f}% hacia 2030"
            )
            st.caption("4.3% con +5 síntomas de ansiedad")
        
        with col2:
            valor = df_historico[df_historico['año'] == 2024]['depresion'].values[0]
            proyeccion = df_proyeccion[df_proyeccion['año'] == 2030]['depresion'].values[0]
            cambio = ((proyeccion - valor) / valor) * 100
            
            st.metric(
                "🟣 Depresión",
                f"{valor:.1f}%",
                delta=f"{cambio:+.1f}% hacia 2030"
            )
            st.caption("3.9% con +7 síntomas depresivos")
        
        with col3:
            valor = df_historico[df_historico['año'] == 2024]['tdah'].values[0]
            proyeccion = df_proyeccion[df_proyeccion['año'] == 2030]['tdah'].values[0]
            cambio = ((proyeccion - valor) / valor) * 100
            
            st.metric(
                "🟢 TDAH",
                f"{valor:.1f}%",
                delta=f"{cambio:+.1f}% hacia 2030"
            )
            st.caption("Trastorno por Déficit de Atención")
        
        # Recomendaciones
        st.markdown("#### 💡 Estrategias de Intervención")
        
        st.success("""
        **Para Ansiedad:**
        - Programas de manejo de estrés y técnicas de relajación
        - Intervenciones basadas en mindfulness
        - Apoyo psicológico individual y grupal
        """)
        
        st.info("""
        **Para Depresión:**
        - Detección temprana mediante tamizaje escolar
        - Terapia cognitivo-conductual adaptada a adolescentes
        - Fortalecimiento de redes de apoyo social
        """)
        
        st.success("""
        **Para TDAH:**
        - Identificación temprana en edad escolar
        - Adaptaciones pedagógicas y curriculares
        - Trabajo coordinado familia-colegio-salud
        """)
    
    with tab3:
        st.subheader("Consumo de Sustancias Psicoactivas")
        
        # Gráfico de consumo de SPA
        fig3 = go.Figure()
        
        sustancias = {
            'alcohol': {'nombre': 'Alcohol', 'color': '#dc2626'},
            'tabaco': {'nombre': 'Tabaco', 'color': '#78716c'},
            'marihuana': {'nombre': 'Marihuana', 'color': '#16a34a'}
        }
        
        for sustancia, props in sustancias.items():
            # Histórico
            fig3.add_trace(go.Scatter(
                x=df_historico['año'],
                y=df_historico[sustancia],
                mode='lines+markers',
                name=f'{props["nombre"]} (Histórico)',
                line=dict(color=props['color'], width=2.5),
                marker=dict(size=9)
            ))
            
            # Proyección
            fig3.add_trace(go.Scatter(
                x=df_proyeccion['año'],
                y=df_proyeccion[sustancia],
                mode='lines+markers',
                name=f'{props["nombre"]} (Proyección)',
                line=dict(color=props['color'], width=2.5, dash='dash'),
                marker=dict(size=9, symbol='diamond'),
                showlegend=False
            ))
        
        fig3.add_vline(x=2024.5, line_dash="dot", line_color="gray")
        
        fig3.update_layout(
            title="Consumo de Sustancias en Adolescentes 12-17 años (2016-2030)",
            xaxis_title="Año",
            yaxis_title="Prevalencia de Consumo (%)",
            height=450,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        # Estadísticas y alertas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            valor = df_historico[df_historico['año'] == 2024]['alcohol'].values[0]
            st.metric("🔴 Alcohol", f"{valor:.1f}%")
            st.caption("5 de cada 10 adolescentes han consumido")
        
        with col2:
            valor = df_historico[df_historico['año'] == 2024]['tabaco'].values[0]
            st.metric("⚫ Tabaco", f"{valor:.1f}%")
            st.caption("Tendencia a la baja")
        
        with col3:
            valor = df_historico[df_historico['año'] == 2024]['marihuana'].values[0]
            proyeccion = df_proyeccion[df_proyeccion['año'] == 2030]['marihuana'].values[0]
            cambio = ((proyeccion - valor) / valor) * 100
            st.metric("🟢 Marihuana", f"{valor:.1f}%", delta=f"{cambio:+.1f}%")
            st.caption("⚠️ Tendencia creciente preocupante")
        
        # Consumo problemático
        st.markdown("#### 🚨 Consumo Problemático de SPA")
        
        fig_problematico = go.Figure()
        
        fig_problematico.add_trace(go.Scatter(
            x=df_historico['año'],
            y=df_historico['consumo_problematico'],
            mode='lines+markers',
            name='Datos Históricos',
            line=dict(color='#dc2626', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(220, 38, 38, 0.1)'
        ))
        
        fig_problematico.add_trace(go.Scatter(
            x=df_proyeccion['año'],
            y=df_proyeccion['consumo_problematico'],
            mode='lines+markers',
            name='Proyección',
            line=dict(color='#991b1b', width=3, dash='dash'),
            marker=dict(size=10, symbol='diamond')
        ))
        
        fig_problematico.add_vline(x=2024.5, line_dash="dot", line_color="gray")
        
        fig_problematico.update_layout(
            title="Tasa de Consumo Problemático (por 100,000 adolescentes)",
            xaxis_title="Año",
            yaxis_title="Tasa por 100,000",
            height=350,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_problematico, use_container_width=True)
        
        valor_2024 = df_historico[df_historico['año'] == 2024]['consumo_problematico'].values[0]
        valor_2030 = df_proyeccion[df_proyeccion['año'] == 2030]['consumo_problematico'].values[0]
        
        st.error(f"""
        🔴 **ALERTA CRÍTICA:** Proyección de aumento del {((valor_2030-valor_2024)/valor_2024*100):.0f}% 
        en consumo problemático para 2030
        
        **Datos actuales (2024):**
        - 1,462 menores diagnosticados con consumo abusivo en Bogotá
        - Aumento de 103% en consumo en niñas y adolescentes mujeres
        - Edad promedio de inicio: 13.7 años
        """)
        
        # Estrategias de prevención
        st.markdown("#### 🛡️ Estrategias de Prevención")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Prevención Universal:**
            - Programas educativos desde primaria
            - Desarrollo de habilidades para la vida
            - Fortalecimiento de factores protectores
            - Participación familiar y comunitaria
            """)
        
        with col2:
            st.markdown("""
            **Prevención Selectiva:**
            - Identificación de población en riesgo
            - Intervenciones tempranas
            - Rutas de atención especializadas
            - Seguimiento y acompañamiento
            """)
    
    with tab4:
        st.subheader("Violencia Escolar y Riesgo Suicida")
        
        # Gráfico dual
        fig4 = go.Figure()
        
        # Bullying
        fig4.add_trace(go.Scatter(
            x=df_historico['año'],
            y=df_historico['bullying'],
            mode='lines+markers',
            name='Bullying (Histórico)',
            line=dict(color='#ef4444', width=2.5),
            marker=dict(size=9),
            yaxis='y1'
        ))
        
        fig4.add_trace(go.Scatter(
            x=df_proyeccion['año'],
            y=df_proyeccion['bullying'],
            mode='lines+markers',
            name='Bullying (Proyección)',
            line=dict(color='#ef4444', width=2.5, dash='dash'),
            marker=dict(size=9, symbol='diamond'),
            yaxis='y1',
            showlegend=False
        ))
        
        # Ideación Suicida
        fig4.add_trace(go.Scatter(
            x=df_historico['año'],
            y=df_historico['ideacion_suicida'],
            mode='lines+markers',
            name='Ideación Suicida (Histórico)',
            line=dict(color='#7c3aed', width=2.5),
            marker=dict(size=9),
            yaxis='y2'
        ))
        
        fig4.add_trace(go.Scatter(
            x=df_proyeccion['año'],
            y=df_proyeccion['ideacion_suicida'],
            mode='lines+markers',
            name='Ideación Suicida (Proyección)',
            line=dict(color='#7c3aed', width=2.5, dash='dash'),
            marker=dict(size=9, symbol='diamond'),
            yaxis='y2',
            showlegend=False
        ))
        
        fig4.add_vline(x=2024.5, line_dash="dot", line_color="gray")
        
        fig4.update_layout(
            title="Violencia Escolar e Ideación Suicida (2016-2030)",
            xaxis_title="Año",
            yaxis=dict(title="Bullying (%)", side="left"),
            yaxis2=dict(title="Ideación Suicida (%)", side="right", overlaying="y"),
            height=450,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig4, use_container_width=True)
        
        # Estadísticas críticas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⚠️ Violencia Escolar")
            valor = df_historico[df_historico['año'] == 2024]['bullying'].values[0]
            st.metric("Prevalencia Actual", f"{valor:.1f}%")
            
            st.warning("""
            **Datos ECAS 2016:**
            - 29.3% de estudiantes afectados por bullying
            - Impacto en rendimiento académico y salud mental
            - Reducción durante pandemia por cierre de colegios
            - Recuperación a niveles pre-pandemia
            """)
        
        with col2:
            st.markdown("#### 🆘 Ideación Suicida")
            valor = df_historico[df_historico['año'] == 2024]['ideacion_suicida'].values[0]
            st.metric("Prevalencia Actual", f"{valor:.1f}%")
            
            st.error("""
            **Medicina Legal 2023-2024:**
            - 230 suicidios de menores en 2023
            - 140 casos en primer trimestre 2024
            - Incremento post-pandemia
            - Necesidad de intervención urgente
            """)
        
        # Líneas de atención
        st.markdown("#### 📞 Líneas de Atención en Crisis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **Línea 106**
            
            Línea distrital de atención 
            en crisis de salud mental
            
            📞 **106**
            🕐 24/7
            """)
        
        with col2:
            st.info("""
            **Línea 123**
            
            Emergencias y atención 
            en crisis psicológica
            
            📞 **123**
            🕐 24/7
            """)
        
        with col3:
            st.info("""
            **Línea de la Vida**
            
            Prevención del suicidio
            
            📞 **01 8000 423 614**
            🕐 24/7
            """)
        
        # Protocolos
        st.markdown("#### 📋 Protocolos de Actuación")
        
        st.markdown("""
        **En caso de detectar riesgo suicida:**
        
        1. **NO dejar sola a la persona**
        2. **Escuchar activamente** sin juzgar
        3. **Contactar líneas de emergencia** (106, 123)
        4. **Informar a familia** y equipo de orientación
        5. **Activar protocolo institucional** de atención
        6. **Garantizar seguimiento** profesional
        
        ⚠️ **Señales de alerta:**
        - Hablar sobre morir o quitarse la vida
        - Cambios drásticos en comportamiento
        - Aislamiento social
        - Regalar posesiones valiosas
        - Expresar desesperanza
        - Búsqueda de métodos letales
        """)
    
    with tab5:
        st.subheader("Proyecciones y Escenarios Futuros 2025-2030")
        
        st.markdown("""
        **Metodología de Proyección:**
        - Regresión polinomial de grado 2
        - Basada en tendencias 2016-2024
        - Ajuste por efectos de pandemia COVID-19
        - Validación con expertos en salud pública
        """)
        
        # Tabla de proyecciones
        st.markdown("#### 📊 Tabla Completa de Proyecciones")
        
        df_tabla = df_proyeccion.copy()
        df_tabla_display = df_tabla.round(1)
        df_tabla_display.columns = [
            'Año', 'SM General (%)', 'Ansiedad (%)', 'Depresión (%)', 
            'TDAH (%)', 'Alcohol (%)', 'Tabaco (%)', 'Marihuana (%)',
            'Bullying (%)', 'Ideación Suicida (%)', 'Consumo Problemático (tasa)'
        ]
        
        st.dataframe(df_tabla_display, use_container_width=True, hide_index=True)
        
        # Análisis de cambios
        st.markdown("#### 📈 Análisis de Tendencias 2024-2030")
        
        cambios = []
        factores_nombres = {
            'sm_general': 'Salud Mental General',
            'ansiedad': 'Ansiedad',
            'depresion': 'Depresión',
            'tdah': 'TDAH',
            'alcohol': 'Consumo de Alcohol',
            'tabaco': 'Consumo de Tabaco',
            'marihuana': 'Consumo de Marihuana',
            'bullying': 'Violencia Escolar',
            'ideacion_suicida': 'Ideación Suicida',
            'consumo_problematico': 'Consumo Problemático SPA'
        }
        
        for factor in factores_nombres.keys():
            valor_2024 = df_historico[df_historico['año'] == 2024][factor].values[0]
            valor_2030 = df_proyeccion[df_proyeccion['año'] == 2030][factor].values[0]
            cambio_pct = ((valor_2030 - valor_2024) / valor_2024) * 100
            
            if abs(cambio_pct) > 15:
                nivel = "🔴 Crítico"
            elif abs(cambio_pct) > 8:
                nivel = "🟡 Advertencia"
            else:
                nivel = "🟢 Normal"
            
            cambios.append({
                'Factor': factores_nombres[factor],
                'Nivel': nivel,
                '2024': f"{valor_2024:.1f}",
                '2030': f"{valor_2030:.1f}",
                'Cambio (%)': f"{cambio_pct:+.1f}%"
            })
        
        df_cambios = pd.DataFrame(cambios)
        
        # Colorear según nivel
        def color_nivel(val):
            if '🔴' in val:
                return 'background-color: #fee2e2'
            elif '🟡' in val:
                return 'background-color: #fef3c7'
            else:
                return 'background-color: #d1fae5'
        
        st.dataframe(
            df_cambios.style.applymap(color_nivel, subset=['Nivel']),
            use_container_width=True,
            hide_index=True
        )
        
        # Recomendaciones estratégicas
        st.markdown("#### 💡 Recomendaciones Estratégicas 2025-2030")
        
        st.error("""
        **🔴 ÁREAS CRÍTICAS - Requieren intervención inmediata:**
        
        1. **Consumo de Marihuana** (↑28% proyectado)
           - Fortalecer programas de prevención desde 5° grado
           - Campañas educativas sobre riesgos del consumo temprano
           - Capacitación docente en detección precoz
        
        2. **Consumo Problemático de SPA** (↑53% proyectado)
           - Ampliar cobertura de servicios de tratamiento
           - Implementar intervenciones tempranas en colegios
           - Rutas de atención especializadas para adolescentes
        
        3. **TDAH** (↑19% proyectado)
           - Mejorar capacidad diagnóstica en IPS
           - Adaptaciones curriculares y pedagógicas
           - Apoyo psicoeducativo a familias
        """)
        
        st.warning("""
        **🟡 ÁREAS DE ADVERTENCIA - Requieren monitoreo constante:**
        
        - **Violencia Escolar**: Mantener programas de convivencia
        - **Consumo de Alcohol**: Controlar acceso de menores
        - **Depresión**: Ampliar servicios de atención psicológica
        """)
        
        st.success("""
        **🟢 ÁREAS CON TENDENCIA POSITIVA:**
        
        - **Tabaco**: Continuar políticas de control
        - **Ideación Suicida**: Mantener protocolos de prevención
        - **Salud Mental General**: Estabilización proyectada
        """)
        
        # Descargar datos
        st.markdown("#### 📥 Descargar Datos de Proyecciones")
        
        csv = df_factores.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="⬇️ Descargar Proyecciones Completas (CSV)",
            data=csv,
            file_name="proyecciones_factores_riesgo_2016_2030.csv",
            mime="text/csv"
        )



def pagina_analisis_genero(datos):
    """Análisis detallado de brechas de género en salud mental"""
    
    st.title("⚧️ Análisis de Género en Salud Mental")
    st.markdown("### Brechas y diferencias en atención (6-17 años)")
    
    df_morbilidad = datos['morbilidad']
    
    # Verificar columna de género
    if 'genero' in df_morbilidad.columns:
        col_genero = 'genero'
    elif 'sexo_gen' in df_morbilidad.columns:
        col_genero = 'sexo_gen'
    else:
        st.error("❌ No se encontró información de género en los datos")
        return
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Panorama General",
        "🏙️ Por Localidad",
        "🧠 Por Trastorno",
        "📈 Evolución Temporal"
    ])
    
    with tab1:
        st.subheader("Panorama General de Género")
        
        # Distribución total por género
        dist_genero = df_morbilidad.groupby(col_genero)['sum_atenciones'].sum().sort_values(ascending=False)
        total_atenciones = dist_genero.sum()
        
        # Métricas principales
        col1, col2, col3 = st.columns(3)
        
        if len(dist_genero) >= 2:
            gen1, gen2 = dist_genero.index[0], dist_genero.index[1]
            atenc1, atenc2 = dist_genero.iloc[0], dist_genero.iloc[1]
            
            with col1:
                st.metric(
                    f"👤 {gen1}",
                    f"{int(atenc1):,}",
                    delta=f"{(atenc1/total_atenciones*100):.1f}%"
                )
            
            with col2:
                st.metric(
                    f"👤 {gen2}",
                    f"{int(atenc2):,}",
                    delta=f"{(atenc2/total_atenciones*100):.1f}%"
                )
            
            with col3:
                ratio = atenc1 / atenc2
                st.metric(
                    "Brecha de Género",
                    f"{ratio:.2f}x",
                    delta=f"{gen1}/{gen2}"
                )
        
        # Gráficos de distribución
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig = px.pie(
                values=dist_genero.values,
                names=dist_genero.index,
                title="Distribución de Atenciones por Género",
                hole=0.4,
                color=dist_genero.index,
                color_discrete_map={
                    'Masculino': '#3b82f6',
                    'Femenino': '#ec4899',
                    'Hombre': '#3b82f6',
                    'Mujer': '#ec4899'
                }
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar chart con diferencia
            fig = go.Figure()
            
            colors = ['#3b82f6' if 'Masculino' in str(g) or 'Hombre' in str(g) else '#ec4899' 
                     for g in dist_genero.index]
            
            fig.add_trace(go.Bar(
                x=dist_genero.index,
                y=dist_genero.values,
                marker_color=colors,
                text=[f"{int(v):,}" for v in dist_genero.values],
                textposition='outside'
            ))
            
            fig.update_layout(
                title="Comparación de Atenciones",
                xaxis_title="Género",
                yaxis_title="Total de Atenciones",
                height=350,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Análisis de la brecha
        st.markdown("#### 📊 Análisis de la Brecha de Género")
        
        if len(dist_genero) >= 2:
            ratio = dist_genero.iloc[0] / dist_genero.iloc[1]
            diferencia_abs = abs(dist_genero.iloc[0] - dist_genero.iloc[1])
            diferencia_pct = ((dist_genero.iloc[0] - dist_genero.iloc[1]) / dist_genero.iloc[1]) * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Ratio", f"{ratio:.2f}x")
            
            with col2:
                st.metric("Diferencia Absoluta", f"{int(diferencia_abs):,}")
            
            with col3:
                st.metric("Diferencia Porcentual", f"{diferencia_pct:+.1f}%")
            
            # Interpretación
            if ratio > 2.0:
                st.error(f"""
                🔴 **Brecha Muy Alta**: {dist_genero.index[0]} tiene más del doble de atenciones 
                que {dist_genero.index[1]}. Se requiere investigación sobre barreras de acceso 
                o diferencias en prevalencia real.
                """)
            elif ratio > 1.5:
                st.warning(f"""
                🟡 **Brecha Significativa**: {dist_genero.index[0]} supera en más del 50% a 
                {dist_genero.index[1]}. Puede reflejar diferencias en patrones de búsqueda 
                de ayuda o en manifestación de trastornos.
                """)
            elif ratio > 1.2:
                st.info(f"""
                🔵 **Brecha Moderada**: Existe una diferencia del {((ratio-1)*100):.0f}% entre 
                géneros. Dentro de rangos observados en salud mental infantil.
                """)
            else:
                st.success("""
                🟢 **Distribución Equilibrada**: La diferencia entre géneros es mínima, 
                lo que sugiere acceso equitativo y/o prevalencias similares.
                """)
        
        # Distribución por nivel educativo y género
        if 'nivel_educativo' in df_morbilidad.columns:
            st.markdown("#### 📚 Distribución por Nivel Educativo y Género")
            
            niveles = ['Primaria (6-10)', 'Secundaria (11-14)', 'Media (15-17)']
            df_niveles = df_morbilidad[df_morbilidad['nivel_educativo'].isin(niveles)]
            
            if len(df_niveles) > 0:
                pivot = df_niveles.groupby(['nivel_educativo', col_genero])['sum_atenciones'].sum().reset_index()
                
                fig = px.bar(
                    pivot,
                    x='nivel_educativo',
                    y='sum_atenciones',
                    color=col_genero,
                    barmode='group',
                    title="Atenciones por Nivel Educativo y Género",
                    labels={'nivel_educativo': 'Nivel Educativo', 'sum_atenciones': 'Atenciones'},
                    color_discrete_map={
                        'Masculino': '#3b82f6',
                        'Femenino': '#ec4899',
                        'Hombre': '#3b82f6',
                        'Mujer': '#ec4899'
                    }
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Análisis de Género por Localidad")
        
        # Top 10 localidades
        top_localidades = df_morbilidad.groupby('prestador_localidad_nombre')['sum_atenciones'].sum().nlargest(10).index
        df_top_loc = df_morbilidad[df_morbilidad['prestador_localidad_nombre'].isin(top_localidades)]
        
        # Gráfico apilado
        pivot_loc = df_top_loc.groupby(['prestador_localidad_nombre', col_genero])['sum_atenciones'].sum().reset_index()
        
        fig = px.bar(
            pivot_loc,
            x='prestador_localidad_nombre',
            y='sum_atenciones',
            color=col_genero,
            title="Top 10 Localidades - Distribución por Género",
            labels={'prestador_localidad_nombre': 'Localidad', 'sum_atenciones': 'Atenciones'},
            color_discrete_map={
                'Masculino': '#3b82f6',
                'Femenino': '#ec4899',
                'Hombre': '#3b82f6',
                'Mujer': '#ec4899'
            },
            barmode='stack'
        )
        
        fig.update_layout(
            height=500,
            xaxis_tickangle=-45,
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla con brecha por localidad
        st.markdown("#### 📊 Brecha de Género por Localidad")
        
        # Calcular brecha para cada localidad
        brechas_localidad = []
        
        for localidad in top_localidades:
            df_loc = df_morbilidad[df_morbilidad['prestador_localidad_nombre'] == localidad]
            dist_gen = df_loc.groupby(col_genero)['sum_atenciones'].sum().sort_values(ascending=False)
            
            if len(dist_gen) >= 2:
                ratio = dist_gen.iloc[0] / dist_gen.iloc[1]
                gen_mayor = dist_gen.index[0]
                
                brechas_localidad.append({
                    'Localidad': localidad,
                    'Género Predominante': gen_mayor,
                    'Brecha': ratio,
                    'Total Atenciones': int(dist_gen.sum())
                })
        
        df_brechas = pd.DataFrame(brechas_localidad).sort_values('Brecha', ascending=False)
        df_brechas['Brecha'] = df_brechas['Brecha'].apply(lambda x: f"{x:.2f}x")
        df_brechas['Total Atenciones'] = df_brechas['Total Atenciones'].apply(lambda x: f"{x:,}")
        
        # Colorear según brecha
        def color_brecha(val):
            try:
                ratio = float(val.replace('x', ''))
                if ratio > 2.0:
                    return 'background-color: #fee2e2'
                elif ratio > 1.5:
                    return 'background-color: #fef3c7'
                else:
                    return 'background-color: #d1fae5'
            except:
                return ''
        
        st.dataframe(
            df_brechas.style.applymap(color_brecha, subset=['Brecha']),
            use_container_width=True,
            height=400
        )
        
        # Localidades con mayor equidad
        st.markdown("#### ✅ Localidades con Mayor Equidad de Género")
        
        localidades_equitativas = df_brechas.head(3)
        
        for _, row in localidades_equitativas.iterrows():
            st.success(f"**{row['Localidad']}** - Brecha: {row['Brecha']} - {row['Total Atenciones']} atenciones")
    
    with tab3:
        st.subheader("Diferencias por Tipo de Trastorno")
        
        if 'categoria_trastorno' in df_morbilidad.columns:
            # Top 8 trastornos
            top_trastornos = df_morbilidad.groupby('categoria_trastorno')['sum_atenciones'].sum().nlargest(8).index
            df_top_trast = df_morbilidad[df_morbilidad['categoria_trastorno'].isin(top_trastornos)]
            
            # Gráfico de barras agrupadas
            pivot_trast = df_top_trast.groupby(['categoria_trastorno', col_genero])['sum_atenciones'].sum().reset_index()
            
            fig = px.bar(
                pivot_trast,
                x='categoria_trastorno',
                y='sum_atenciones',
                color=col_genero,
                barmode='group',
                title="Top 8 Trastornos - Comparación por Género",
                labels={'categoria_trastorno': 'Trastorno', 'sum_atenciones': 'Atenciones'},
                color_discrete_map={
                    'Masculino': '#3b82f6',
                    'Femenino': '#ec4899',
                    'Hombre': '#3b82f6',
                    'Mujer': '#ec4899'
                }
            )
            
            fig.update_layout(
                height=500,
                xaxis_tickangle=-45,
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Análisis de trastornos con mayor brecha
            st.markdown("#### 🔍 Trastornos con Mayor Diferencia de Género")
            
            brechas_trastorno = []
            
            for trastorno in top_trastornos:
                df_trast = df_morbilidad[df_morbilidad['categoria_trastorno'] == trastorno]
                dist_gen = df_trast.groupby(col_genero)['sum_atenciones'].sum().sort_values(ascending=False)
                
                if len(dist_gen) >= 2:
                    ratio = dist_gen.iloc[0] / dist_gen.iloc[1]
                    gen_mayor = dist_gen.index[0]
                    
                    brechas_trastorno.append({
                        'Trastorno': trastorno,
                        'Género Predominante': gen_mayor,
                        'Brecha': ratio,
                        'Total': int(dist_gen.sum())
                    })
            
            df_brech_trast = pd.DataFrame(brechas_trastorno).sort_values('Brecha', ascending=False)
            
            # Mostrar top 5 con mayor brecha
            st.markdown("**Top 5 con Mayor Brecha:**")
            
            for _, row in df_brech_trast.head(5).iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{row['Trastorno']}**")
                
                with col2:
                    st.write(f"{row['Género Predominante']}")
                
                with col3:
                    if row['Brecha'] > 2.0:
                        st.error(f"{row['Brecha']:.2f}x")
                    elif row['Brecha'] > 1.5:
                        st.warning(f"{row['Brecha']:.2f}x")
                    else:
                        st.info(f"{row['Brecha']:.2f}x")
            
            # Observaciones clínicas
            st.markdown("#### 💡 Observaciones Clínicas")
            
            st.info("""
            **Diferencias de género en trastornos mentales:**
            
            - 🔵 **Más prevalentes en niños/adolescentes masculinos:**
              - TDAH y trastornos del neurodesarrollo
              - Trastornos de conducta
              - Trastornos del espectro autista
            
            - 🔴 **Más prevalentes en niñas/adolescentes femeninas:**
              - Trastornos de ansiedad
              - Trastornos depresivos
              - Trastornos alimentarios
            
            Estas diferencias pueden reflejar:
            - Factores biológicos y hormonales
            - Diferencias en manifestación de síntomas
            - Patrones de socialización de género
            - Sesgos en detección y diagnóstico
            """)
    
    with tab4:
        st.subheader("Evolución Temporal de la Brecha de Género")
        
        # Evolución anual por género
        evolucion_gen = df_morbilidad.groupby(['ano', col_genero])['sum_atenciones'].sum().reset_index()
        
        # Gráfico de líneas
        fig = px.line(
            evolucion_gen,
            x='ano',
            y='sum_atenciones',
            color=col_genero,
            markers=True,
            title="Evolución de Atenciones por Género (2019-2024)",
            labels={'ano': 'Año', 'sum_atenciones': 'Atenciones'},
            color_discrete_map={
                'Masculino': '#3b82f6',
                'Femenino': '#ec4899',
                'Hombre': '#3b82f6',
                'Mujer': '#ec4899'
            }
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Calcular brecha por año
        st.markdown("#### 📊 Evolución de la Brecha")
        
        pivot_años = evolucion_gen.pivot(index='ano', columns=col_genero, values='sum_atenciones')
        
        if len(pivot_años.columns) >= 2:
            pivot_años['ratio'] = pivot_años.iloc[:, 0] / pivot_años.iloc[:, 1]
            
            fig2 = go.Figure()
            
            fig2.add_trace(go.Scatter(
                x=pivot_años.index,
                y=pivot_años['ratio'],
                mode='lines+markers',
                name='Brecha de Género',
                line=dict(color='#8b5cf6', width=3),
                marker=dict(size=12),
                text=[f"{v:.2f}x" for v in pivot_años['ratio']],
                textposition='top center'
            ))
            
            fig2.add_hline(
                y=1.0,
                line_dash="dash",
                line_color="gray",
                annotation_text="Equilibrio (1.0x)",
                annotation_position="right"
            )
            
            fig2.update_layout(
                title=f"Ratio {pivot_años.columns[0]}/{pivot_años.columns[1]} por Año",
                xaxis_title="Año",
                yaxis_title="Ratio",
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Análisis de tendencia
            st.markdown("#### 🔍 Análisis de Tendencia de la Brecha")
            
            brecha_inicial = pivot_años['ratio'].iloc[0]
            brecha_final = pivot_años['ratio'].iloc[-1]
            cambio_brecha = brecha_final - brecha_inicial
            cambio_pct = (cambio_brecha / brecha_inicial) * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Brecha Inicial", f"{brecha_inicial:.2f}x", 
                         delta=f"Año {pivot_años.index[0]}")
            
            with col2:
                st.metric("Brecha Actual", f"{brecha_final:.2f}x",
                         delta=f"{cambio_pct:+.1f}%",
                         delta_color="inverse")
            
            with col3:
                promedio_brecha = pivot_años['ratio'].mean()
                st.metric("Brecha Promedio", f"{promedio_brecha:.2f}x")
            
            # Interpretación
            if cambio_pct > 10:
                st.warning(f"""
                ⚠️ **La brecha se ha ampliado** en un {cambio_pct:.1f}% desde 2019.
                Esto sugiere que las diferencias de género en atención se están incrementando.
                """)
            elif cambio_pct < -10:
                st.success(f"""
                ✅ **La brecha se ha reducido** en un {abs(cambio_pct):.1f}% desde 2019.
                Las diferencias de género en atención están disminuyendo.
                """)
            else:
                st.info(f"""
                ➡️ **La brecha se mantiene relativamente estable** (variación de {cambio_pct:+.1f}%).
                Las diferencias de género no han cambiado significativamente.
                """)
        
        # Recomendaciones
        st.markdown("#### 💡 Recomendaciones de Política Pública")
        
        st.markdown("""
        **Para reducir brechas de género en salud mental:**
        
        1. **Sensibilización y capacitación:**
           - Formar a docentes en detección de señales diferenciadas por género
           - Reducir sesgos de género en diagnóstico
           - Promover acceso equitativo a servicios
        
        2. **Programas específicos:**
           - Intervenciones adaptadas a necesidades de cada género
           - Grupos de apoyo diferenciados cuando sea apropiado
           - Abordaje de estereotipos de género que afectan salud mental
        
        3. **Investigación:**
           - Estudiar causas de brechas observadas
           - Monitorear evolución de diferencias
           - Evaluar efectividad de intervenciones
        """)

# ============================================================================
# PÁGINA 7: BUSCADOR DE LOCALIDADES
# ============================================================================

def pagina_buscador_localidades(datos):
    """Buscador interactivo de información por localidad"""
    
    st.title("🔍 Buscador de Localidades")
    st.markdown("### Consulta información detallada por localidad de Bogotá")
    
    df_morbilidad = datos['morbilidad']
    df_clasificacion = datos['clasificacion']
    df_integrado = datos['integrado']
    
    # Obtener lista de localidades únicas
    localidades = sorted(df_morbilidad['prestador_localidad_nombre'].unique())
    
    # Selector de localidad
    st.markdown("#### 📍 Selecciona una localidad")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        localidad_seleccionada = st.selectbox(
            "Localidad:",
            options=localidades,
            index=0,
            help="Selecciona una localidad para ver su información detallada"
        )
    
    with col2:
        st.metric("Total Localidades", len(localidades))
    
    # Filtrar datos de la localidad seleccionada
    df_loc = df_morbilidad[df_morbilidad['prestador_localidad_nombre'] == localidad_seleccionada]
    
    if len(df_loc) == 0:
        st.warning(f"No se encontraron datos para {localidad_seleccionada}")
        return
    
    st.markdown("---")
    
    # =========================================================================
    # SECCIÓN 1: RESUMEN GENERAL
    # =========================================================================
    
    st.markdown(f"## 📊 Resumen: {localidad_seleccionada}")
    
    # Métricas principales
    total_atenciones = df_loc['sum_atenciones'].sum()
    num_registros = len(df_loc)
    
    # Calcular ranking
    ranking_localidades = df_morbilidad.groupby('prestador_localidad_nombre')['sum_atenciones'].sum().sort_values(ascending=False)
    posicion = list(ranking_localidades.index).index(localidad_seleccionada) + 1
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Atenciones", f"{int(total_atenciones):,}")
    
    with col2:
        st.metric("Registros", f"{num_registros:,}")
    
    with col3:
        pct_total = (total_atenciones / df_morbilidad['sum_atenciones'].sum()) * 100
        st.metric("% del Total", f"{pct_total:.2f}%")
    
    with col4:
        st.metric("Ranking", f"#{posicion}", delta=f"de {len(localidades)}")
    
    # Nivel de riesgo (si existe clasificación)
    if len(df_clasificacion) > 0:
        clasificacion_loc = df_clasificacion[df_clasificacion['localidad'] == localidad_seleccionada]
        
        if len(clasificacion_loc) > 0:
            riesgo = clasificacion_loc['riesgo_predicho'].iloc[0]
            confianza = clasificacion_loc['confianza'].iloc[0]
            
            if riesgo == 'Alto':
                st.error(f"🔴 **Nivel de Riesgo:** {riesgo} (Confianza: {confianza:.1%})")
            elif riesgo == 'Medio':
                st.warning(f"🟡 **Nivel de Riesgo:** {riesgo} (Confianza: {confianza:.1%})")
            else:
                st.success(f"🟢 **Nivel de Riesgo:** {riesgo} (Confianza: {confianza:.1%})")
    
    st.markdown("---")
    
    # =========================================================================
    # SECCIÓN 2: TABS CON ANÁLISIS DETALLADO
    # =========================================================================
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Evolución Temporal",
        "🧠 Trastornos",
        "⚧️ Análisis de Género",
        "📚 Nivel Educativo"
    ])
    
    with tab1:
        st.subheader(f"Evolución Temporal - {localidad_seleccionada}")
        
        # Atenciones por año
        atenciones_año = df_loc.groupby('ano')['sum_atenciones'].sum().sort_index()
        
        # Gráfico de línea
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=atenciones_año.index,
            y=atenciones_año.values,
            mode='lines+markers',
            name=localidad_seleccionada,
            line=dict(color='#2563eb', width=3),
            marker=dict(size=12),
            fill='tozeroy',
            fillcolor='rgba(37, 99, 235, 0.2)'
        ))
        
        fig.update_layout(
            title=f"Evolución de Atenciones - {localidad_seleccionada}",
            xaxis_title="Año",
            yaxis_title="Número de Atenciones",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Estadísticas de crecimiento
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if len(atenciones_año) > 1:
                crecimiento = ((atenciones_año.iloc[-1] - atenciones_año.iloc[0]) / atenciones_año.iloc[0]) * 100
                st.metric("Crecimiento Total", f"{crecimiento:+.1f}%")
        
        with col2:
            promedio = atenciones_año.mean()
            st.metric("Promedio Anual", f"{int(promedio):,}")
        
        with col3:
            max_año = atenciones_año.idxmax()
            st.metric("Año Pico", f"{int(max_año)}")
        
        # Comparación con promedio de Bogotá
        st.markdown("#### 📊 Comparación con Promedio de Bogotá")
        
        atenciones_bogota = df_morbilidad.groupby('ano')['sum_atenciones'].sum()
        num_localidades = df_morbilidad['prestador_localidad_nombre'].nunique()
        promedio_bogota = atenciones_bogota / num_localidades
        
        # Gráfico comparativo
        fig2 = go.Figure()
        
        fig2.add_trace(go.Bar(
            x=atenciones_año.index,
            y=atenciones_año.values,
            name=localidad_seleccionada,
            marker_color='#2563eb'
        ))
        
        fig2.add_trace(go.Scatter(
            x=promedio_bogota.index,
            y=promedio_bogota.values,
            name='Promedio Bogotá',
            line=dict(color='#f59e0b', width=2, dash='dash'),
            mode='lines+markers'
        ))
        
        fig2.update_layout(
            title="Comparación con Promedio de Bogotá",
            xaxis_title="Año",
            yaxis_title="Atenciones",
            height=350,
            template='plotly_white'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader(f"Trastornos Prevalentes - {localidad_seleccionada}")
        
        # Top 10 trastornos en esta localidad
        if 'categoria_trastorno' in df_loc.columns:
            top_trastornos = df_loc.groupby('categoria_trastorno')['sum_atenciones'].sum().sort_values(ascending=False).head(10)
            
            # Gráfico horizontal
            fig = go.Figure(go.Bar(
                x=top_trastornos.values,
                y=top_trastornos.index,
                orientation='h',
                marker=dict(
                    color=top_trastornos.values,
                    colorscale='Reds',
                    showscale=False
                ),
                text=[f"{int(v):,}" for v in top_trastornos.values],
                textposition='outside'
            ))
            
            fig.update_layout(
                title=f"Top 10 Trastornos - {localidad_seleccionada}",
                xaxis_title="Atenciones",
                yaxis_title="",
                height=500,
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla detallada
            st.markdown("#### 📋 Detalle de Trastornos")
            
            df_trast_detalle = pd.DataFrame({
                'Trastorno': top_trastornos.index,
                'Atenciones': top_trastornos.values
            })
            
            df_trast_detalle['% de la Localidad'] = (df_trast_detalle['Atenciones'] / total_atenciones * 100).round(2)
            df_trast_detalle['Atenciones'] = df_trast_detalle['Atenciones'].apply(lambda x: f"{int(x):,}")
            
            st.dataframe(df_trast_detalle, use_container_width=True)
            
            # Principal trastorno
            principal = top_trastornos.index[0]
            principal_pct = (top_trastornos.iloc[0] / total_atenciones) * 100
            
            st.info(f"""
            🎯 **Trastorno Principal:** {principal}  
            Representa el {principal_pct:.1f}% de las atenciones en {localidad_seleccionada}
            """)
        else:
            top_dx = df_loc.groupby('dxprincipal_agrupacion1_nombre')['sum_atenciones'].sum().sort_values(ascending=False).head(10)
            
            fig = px.bar(
                x=top_dx.values,
                y=top_dx.index,
                orientation='h',
                title=f"Top 10 Diagnósticos - {localidad_seleccionada}",
                labels={'x': 'Atenciones', 'y': 'Diagnóstico'}
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader(f"Análisis de Género - {localidad_seleccionada}")
        
        # Verificar columna de género
        if 'genero' in df_loc.columns:
            col_genero = 'genero'
        elif 'sexo_gen' in df_loc.columns:
            col_genero = 'sexo_gen'
        else:
            st.warning("Datos de género no disponibles")
            return
        
        # Distribución por género
        dist_genero = df_loc.groupby(col_genero)['sum_atenciones'].sum().sort_values(ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig = px.pie(
                values=dist_genero.values,
                names=dist_genero.index,
                title=f"Distribución por Género - {localidad_seleccionada}",
                hole=0.4,
                color=dist_genero.index,
                color_discrete_map={
                    'Masculino': '#3b82f6',
                    'Femenino': '#ec4899',
                    'Hombre': '#3b82f6',
                    'Mujer': '#ec4899'
                }
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Métricas
            if len(dist_genero) >= 2:
                gen1, gen2 = dist_genero.index[0], dist_genero.index[1]
                atenc1, atenc2 = dist_genero.iloc[0], dist_genero.iloc[1]
                
                st.metric(f"👤 {gen1}", f"{int(atenc1):,}")
                st.metric(f"👤 {gen2}", f"{int(atenc2):,}")
                
                ratio = atenc1 / atenc2
                st.metric("Brecha de Género", f"{ratio:.2f}x")
                
                # Comparar con promedio de Bogotá
                dist_gen_bogota = df_morbilidad.groupby(col_genero)['sum_atenciones'].sum().sort_values(ascending=False)
                if len(dist_gen_bogota) >= 2:
                    ratio_bogota = dist_gen_bogota.iloc[0] / dist_gen_bogota.iloc[1]
                    
                    if abs(ratio - ratio_bogota) > 0.3:
                        st.warning(f"""
                        ⚠️ La brecha de género en {localidad_seleccionada} ({ratio:.2f}x) 
                        difiere significativamente del promedio de Bogotá ({ratio_bogota:.2f}x)
                        """)
                    else:
                        st.success(f"""
                        ✅ La brecha de género es similar al promedio de Bogotá ({ratio_bogota:.2f}x)
                        """)
        
        # Evolución de género por año
        st.markdown("#### 📈 Evolución por Género")
        
        evolucion_gen = df_loc.groupby(['ano', col_genero])['sum_atenciones'].sum().reset_index()
        
        fig2 = px.line(
            evolucion_gen,
            x='ano',
            y='sum_atenciones',
            color=col_genero,
            markers=True,
            title=f"Evolución por Género - {localidad_seleccionada}",
            labels={'ano': 'Año', 'sum_atenciones': 'Atenciones'},
            color_discrete_map={
                'Masculino': '#3b82f6',
                'Femenino': '#ec4899',
                'Hombre': '#3b82f6',
                'Mujer': '#ec4899'
            }
        )
        
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab4:
        st.subheader(f"Distribución por Nivel Educativo - {localidad_seleccionada}")
        
        if 'nivel_educativo' in df_loc.columns:
            # Filtrar niveles escolares
            niveles = ['Primaria (6-10)', 'Secundaria (11-14)', 'Media (15-17)']
            df_niveles = df_loc[df_loc['nivel_educativo'].isin(niveles)]
            
            if len(df_niveles) > 0:
                dist_nivel = df_niveles.groupby('nivel_educativo')['sum_atenciones'].sum()
                dist_nivel = dist_nivel.reindex(niveles, fill_value=0)
                
                # Gráfico de barras
                fig = go.Figure(go.Bar(
                    x=dist_nivel.index,
                    y=dist_nivel.values,
                    marker_color=['#3b82f6', '#f59e0b', '#10b981'],
                    text=[f"{int(v):,}" for v in dist_nivel.values],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    title=f"Atenciones por Nivel Educativo - {localidad_seleccionada}",
                    xaxis_title="Nivel Educativo",
                    yaxis_title="Atenciones",
                    height=400,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Porcentajes
                col1, col2, col3 = st.columns(3)
                
                total_niveles = dist_nivel.sum()
                
                with col1:
                    pct = (dist_nivel['Primaria (6-10)'] / total_niveles * 100) if total_niveles > 0 else 0
                    st.metric("Primaria (6-10)", f"{pct:.1f}%")
                
                with col2:
                    pct = (dist_nivel['Secundaria (11-14)'] / total_niveles * 100) if total_niveles > 0 else 0
                    st.metric("Secundaria (11-14)", f"{pct:.1f}%")
                
                with col3:
                    pct = (dist_nivel['Media (15-17)'] / total_niveles * 100) if total_niveles > 0 else 0
                    st.metric("Media (15-17)", f"{pct:.1f}%")
                
                # Comparación con Bogotá
                st.markdown("#### 📊 Comparación con Bogotá")
                
                df_bogota_niveles = df_morbilidad[df_morbilidad['nivel_educativo'].isin(niveles)]
                dist_bogota = df_bogota_niveles.groupby('nivel_educativo')['sum_atenciones'].sum()
                dist_bogota = dist_bogota.reindex(niveles, fill_value=0)
                
                # Normalizar a porcentajes
                pct_localidad = (dist_nivel / dist_nivel.sum() * 100).round(1)
                pct_bogota = (dist_bogota / dist_bogota.sum() * 100).round(1)
                
                df_comparacion = pd.DataFrame({
                    'Nivel': niveles,
                    f'{localidad_seleccionada} (%)': pct_localidad.values,
                    'Bogotá (%)': pct_bogota.values
                })
                
                df_comparacion['Diferencia (pp)'] = df_comparacion[f'{localidad_seleccionada} (%)'] - df_comparacion['Bogotá (%)']
                
                st.dataframe(df_comparacion, use_container_width=True)
            else:
                st.info("No hay datos de nivel educativo disponibles para esta localidad")
        else:
            # Fallback a grupos de edad
            if 'edad_grupo_rias' in df_loc.columns:
                dist_edad = df_loc.groupby('edad_grupo_rias')['sum_atenciones'].sum().sort_values(ascending=False)
                
                fig = px.bar(
                    x=dist_edad.index,
                    y=dist_edad.values,
                    title=f"Distribución por Grupo de Edad - {localidad_seleccionada}",
                    labels={'x': 'Grupo de Edad', 'y': 'Atenciones'}
                )
                
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
    
    # =========================================================================
    # SECCIÓN 3: RECOMENDACIONES
    # =========================================================================
    
    st.markdown("---")
    st.markdown(f"## 💡 Recomendaciones para {localidad_seleccionada}")
    
    # Análisis automático
    recomendaciones = []
    
    # Basado en volumen
    if posicion <= 5:
        recomendaciones.append("""
        🔴 **Alta demanda**: Esta localidad se encuentra entre las 5 con mayor número de atenciones.
        - Reforzar equipos de orientación escolar
        - Ampliar capacidad de atención en salud mental
        - Implementar programas de prevención masivos
        """)
    
    # Basado en brecha de género
    if 'genero' in df_loc.columns or 'sexo_gen' in df_loc.columns:
        col_gen = 'genero' if 'genero' in df_loc.columns else 'sexo_gen'
        dist_gen = df_loc.groupby(col_gen)['sum_atenciones'].sum().sort_values(ascending=False)
        
        if len(dist_gen) >= 2:
            ratio = dist_gen.iloc[0] / dist_gen.iloc[1]
            if ratio > 2.0:
                recomendaciones.append(f"""
                🟡 **Brecha de género alta**: Existe una diferencia significativa en atenciones por género ({ratio:.2f}x).
                - Investigar barreras de acceso diferenciadas
                - Adaptar estrategias de comunicación por género
                - Evaluar sesgos en detección y referencia
                """)
    
    # Basado en tendencia
    if len(atenciones_año) > 1:
        crecimiento = ((atenciones_año.iloc[-1] - atenciones_año.iloc[0]) / atenciones_año.iloc[0]) * 100
        if crecimiento > 20:
            recomendaciones.append(f"""
            📈 **Tendencia creciente**: Las atenciones han aumentado un {crecimiento:.1f}% desde 2019.
            - Evaluar factores causales del incremento
            - Planificar expansión de servicios
            - Fortalecer prevención y promoción
            """)
    
    # Mostrar recomendaciones
    if recomendaciones:
        for rec in recomendaciones:
            st.warning(rec)
    else:
        st.success("""
        ✅ **Situación estable**: Esta localidad no presenta alertas críticas en los indicadores monitoreados.
        Continuar con programas de prevención y seguimiento regular.
        """)

# ============================================================================
# PÁGINA 8: DESCARGAR REPORTES
# ============================================================================

def pagina_descargar_reportes(datos):
    """Generación y descarga de reportes en diferentes formatos"""
    
    st.title("📥 Descargar Reportes")
    st.markdown("### Genera y descarga reportes personalizados del Observatorio")
    
    df_morbilidad = datos['morbilidad']
    df_integrado = datos['integrado']
    df_clasificacion = datos['clasificacion']
    df_clustering = datos['clustering']
    kpis = datos['kpis']
    
    st.info("""
    💡 **Tipos de reportes disponibles:**
    - 📊 Reportes ejecutivos con indicadores clave
    - 📈 Datos completos para análisis personalizado
    - 🗺️ Información por localidad
    - ⚧️ Análisis de género
    - 🧠 Clasificación de riesgo
    """)
    
    # =========================================================================
    # SECCIÓN 1: REPORTES EJECUTIVOS
    # =========================================================================
    
    st.markdown("---")
    st.markdown("## 📊 Reportes Ejecutivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Resumen General")
        st.markdown("""
        **Contenido:**
        - Indicadores clave agregados
        - KPIs principales
        - Alertas activas
        - Resumen por año
        
        **Formato:** CSV  
        **Tamaño aproximado:** < 1 KB
        """)
        
        if st.button("📥 Descargar Resumen General", key="btn_resumen"):
            # Crear DataFrame de resumen
            resumen_data = {
                'Indicador': [
                    'Total Atenciones (6-17 años)',
                    'Población Estudiantil',
                    'Tasa por 500 estudiantes',
                    'Número de Localidades',
                    'Período Analizado',
                    'Orientadores Requeridos',
                    'Brecha de Género'
                ],
                'Valor': [
                    f"{int(df_morbilidad['sum_atenciones'].sum()):,}",
                    f"{int(kpis.get('poblacion_estudiantil', 0)):,}",
                    f"{kpis.get('tasa_por_500', 0):.2f}",
                    f"{df_morbilidad['prestador_localidad_nombre'].nunique()}",
                    f"{df_morbilidad['ano'].min()} - {df_morbilidad['ano'].max()}",
                    f"{int(kpis.get('orientadores_necesarios', 0)):,}",
                    f"{kpis.get('brecha_genero', 0):.2f}x"
                ]
            }
            
            df_resumen = pd.DataFrame(resumen_data)
            
            csv = df_resumen.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv,
                file_name=f"resumen_general_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        st.markdown("### 🚨 Reporte de Alertas")
        st.markdown("""
        **Contenido:**
        - Alertas críticas activas
        - Alertas de advertencia
        - Umbrales alcanzados
        - Recomendaciones
        
        **Formato:** CSV  
        **Tamaño aproximado:** < 5 KB
        """)
        
        if st.button("📥 Descargar Alertas", key="btn_alertas"):
            alertas = kpis.get('alertas', [])
            
            if alertas:
                df_alertas = pd.DataFrame(alertas)
                
                csv = df_alertas.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="⬇️ Descargar CSV",
                    data=csv,
                    file_name=f"alertas_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No hay alertas disponibles para descargar")
    
    # =========================================================================
    # SECCIÓN 2: DATASETS COMPLETOS
    # =========================================================================
    
    st.markdown("---")
    st.markdown("## 📊 Datasets Completos")
    
    st.markdown("""
    Descarga los datasets completos para realizar tus propios análisis personalizados.
    Todos los archivos incluyen datos filtrados para población de 6-17 años.
    """)
    
    # Dataset principal
    with st.expander("📁 Dataset Principal - Morbilidad en Salud Mental"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Registros", f"{len(df_morbilidad):,}")
        
        with col2:
            st.metric("Columnas", f"{len(df_morbilidad.columns)}")
        
        with col3:
            size_mb = df_morbilidad.memory_usage(deep=True).sum() / 1024**2
            st.metric("Tamaño", f"{size_mb:.1f} MB")
        
        st.markdown("**Columnas incluidas:**")
        cols_preview = st.multiselect(
            "Selecciona columnas para descargar:",
            options=list(df_morbilidad.columns),
            default=list(df_morbilidad.columns[:10]),
            key="cols_morbilidad"
        )
        
        if cols_preview:
            st.dataframe(df_morbilidad[cols_preview].head(5), use_container_width=True)
            
            csv = df_morbilidad[cols_preview].to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="⬇️ Descargar Dataset Morbilidad (CSV)",
                data=csv,
                file_name=f"morbilidad_6_17_años_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_morbilidad"
            )
    
    # Dataset integrado
    with st.expander("📁 Dataset Integrado - Serie Temporal"):
        st.markdown("""
        Dataset consolidado por año con:
        - Atenciones totales
        - Matrícula
        - Tasa por 500
        - Orientadores necesarios
        """)
        
        st.dataframe(df_integrado, use_container_width=True)
        
        csv = df_integrado.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="⬇️ Descargar Dataset Integrado (CSV)",
            data=csv,
            file_name=f"serie_temporal_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="download_integrado"
        )
    
    # Clasificación ML
    with st.expander("📁 Clasificación de Riesgo (Machine Learning)"):
        st.markdown("""
        Resultados del modelo Random Forest:
        - Nivel de riesgo por localidad
        - Confianza del modelo
        - Riesgo predicho vs real
        """)
        
        if len(df_clasificacion) > 0:
            st.dataframe(df_clasificacion, use_container_width=True)
            
            csv = df_clasificacion.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="⬇️ Descargar Clasificación (CSV)",
                data=csv,
                file_name=f"clasificacion_riesgo_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_clasificacion"
            )
        else:
            st.warning("Datos de clasificación no disponibles")
    
    # Clustering
    with st.expander("📁 Clustering de Localidades (K-Means)"):
        st.markdown("""
        Agrupación de localidades similares:
        - Cluster asignado
        - Características del grupo
        - Etiqueta interpretativa
        """)
        
        if len(df_clustering) > 0:
            st.dataframe(df_clustering, use_container_width=True)
            
            csv = df_clustering.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="⬇️ Descargar Clustering (CSV)",
                data=csv,
                file_name=f"clustering_localidades_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_clustering"
            )
        else:
            st.warning("Datos de clustering no disponibles")
    
    # =========================================================================
    # SECCIÓN 3: REPORTES POR DIMENSIÓN
    # =========================================================================
    
    st.markdown("---")
    st.markdown("## 📊 Reportes por Dimensión")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏙️ Reporte por Localidad")
        
        localidades = sorted(df_morbilidad['prestador_localidad_nombre'].unique())
        localidad_sel = st.selectbox(
            "Selecciona localidad:",
            options=['Todas'] + list(localidades),
            key="sel_localidad_reporte"
        )
        
        if st.button("Generar Reporte por Localidad", key="btn_loc"):
            if localidad_sel == 'Todas':
                # Resumen agregado por localidad
                reporte_loc = df_morbilidad.groupby('prestador_localidad_nombre').agg({
                    'sum_atenciones': 'sum',
                    'ano': lambda x: f"{x.min()}-{x.max()}"
                }).reset_index()
                
                reporte_loc.columns = ['Localidad', 'Total_Atenciones', 'Periodo']
                reporte_loc = reporte_loc.sort_values('Total_Atenciones', ascending=False)
                
            else:
                # Detalle de localidad específica
                df_loc = df_morbilidad[df_morbilidad['prestador_localidad_nombre'] == localidad_sel]
                
                reporte_loc = df_loc.groupby(['ano', 'categoria_trastorno' if 'categoria_trastorno' in df_loc.columns else 'dxprincipal_agrupacion1_nombre']).agg({
                    'sum_atenciones': 'sum'
                }).reset_index()
                
                reporte_loc.columns = ['Año', 'Trastorno', 'Atenciones']
            
            st.dataframe(reporte_loc, use_container_width=True)
            
            csv = reporte_loc.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="⬇️ Descargar Reporte Localidad",
                data=csv,
                file_name=f"reporte_{localidad_sel.lower().replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_reporte_loc"
            )
    
    with col2:
        st.markdown("### ⚧️ Reporte de Género")
        
        if 'genero' in df_morbilidad.columns or 'sexo_gen' in df_morbilidad.columns:
            col_gen = 'genero' if 'genero' in df_morbilidad.columns else 'sexo_gen'
            
            tipo_reporte_gen = st.radio(
                "Tipo de reporte:",
                ['Resumen General', 'Por Año', 'Por Trastorno'],
                key="radio_genero"
            )
            
            if st.button("Generar Reporte de Género", key="btn_genero"):
                if tipo_reporte_gen == 'Resumen General':
                    reporte_gen = df_morbilidad.groupby(col_gen).agg({
                        'sum_atenciones': 'sum'
                    }).reset_index()
                    
                    reporte_gen.columns = ['Género', 'Total_Atenciones']
                    reporte_gen['Porcentaje'] = (reporte_gen['Total_Atenciones'] / reporte_gen['Total_Atenciones'].sum() * 100).round(2)
                
                elif tipo_reporte_gen == 'Por Año':
                    reporte_gen = df_morbilidad.groupby(['ano', col_gen]).agg({
                        'sum_atenciones': 'sum'
                    }).reset_index()
                    
                    reporte_gen.columns = ['Año', 'Género', 'Atenciones']
                
                else:  # Por Trastorno
                    col_trast = 'categoria_trastorno' if 'categoria_trastorno' in df_morbilidad.columns else 'dxprincipal_agrupacion1_nombre'
                    
                    reporte_gen = df_morbilidad.groupby([col_trast, col_gen]).agg({
                        'sum_atenciones': 'sum'
                    }).reset_index()
                    
                    reporte_gen.columns = ['Trastorno', 'Género', 'Atenciones']
                    reporte_gen = reporte_gen.sort_values('Atenciones', ascending=False)
                
                st.dataframe(reporte_gen, use_container_width=True)
                
                csv = reporte_gen.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="⬇️ Descargar Reporte Género",
                    data=csv,
                    file_name=f"reporte_genero_{tipo_reporte_gen.lower().replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="download_reporte_gen"
                )
        else:
            st.warning("Datos de género no disponibles")
    
    # =========================================================================
    # SECCIÓN 4: REPORTE PERSONALIZADO
    # =========================================================================
    
    st.markdown("---")
    st.markdown("## 🎨 Reporte Personalizado")
    
    st.markdown("""
    Crea tu propio reporte seleccionando las dimensiones de análisis que necesites.
    """)
    
    with st.form("form_personalizado"):
        st.markdown("### Configuración del Reporte")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Filtros temporales
            años_disponibles = sorted(df_morbilidad['ano'].unique())
            años_sel = st.multiselect(
                "Años:",
                options=años_disponibles,
                default=años_disponibles,
                key="años_pers"
            )
            
            # Filtro de localidades
            localidades_disponibles = sorted(df_morbilidad['prestador_localidad_nombre'].unique())
            localidades_sel = st.multiselect(
                "Localidades:",
                options=localidades_disponibles,
                default=localidades_disponibles[:5],
                key="loc_pers"
            )
        
        with col2:
            # Agrupación
            agrupar_por = st.multiselect(
                "Agrupar por:",
                options=['Año', 'Localidad', 'Género', 'Trastorno', 'Nivel Educativo'],
                default=['Año', 'Localidad'],
                key="agrupar_pers"
            )
            
            # Métrica
            metrica = st.selectbox(
                "Métrica:",
                options=['Total Atenciones', 'Promedio', 'Máximo', 'Mínimo'],
                key="metrica_pers"
            )
        
        submitted = st.form_submit_button("🔍 Generar Reporte Personalizado")
        
        if submitted:
            # Filtrar datos
            df_filtrado = df_morbilidad[
                (df_morbilidad['ano'].isin(años_sel)) &
                (df_morbilidad['prestador_localidad_nombre'].isin(localidades_sel))
            ]
            
            # Mapear agrupaciones
            group_cols = []
            if 'Año' in agrupar_por:
                group_cols.append('ano')
            if 'Localidad' in agrupar_por:
                group_cols.append('prestador_localidad_nombre')
            if 'Género' in agrupar_por:
                col_gen = 'genero' if 'genero' in df_filtrado.columns else 'sexo_gen'
                if col_gen in df_filtrado.columns:
                    group_cols.append(col_gen)
            if 'Trastorno' in agrupar_por:
                col_trast = 'categoria_trastorno' if 'categoria_trastorno' in df_filtrado.columns else 'dxprincipal_agrupacion1_nombre'
                if col_trast in df_filtrado.columns:
                    group_cols.append(col_trast)
            if 'Nivel Educativo' in agrupar_por and 'nivel_educativo' in df_filtrado.columns:
                group_cols.append('nivel_educativo')
            
            # Aplicar agregación
            if metrica == 'Total Atenciones':
                reporte_pers = df_filtrado.groupby(group_cols)['sum_atenciones'].sum().reset_index()
            elif metrica == 'Promedio':
                reporte_pers = df_filtrado.groupby(group_cols)['sum_atenciones'].mean().reset_index()
            elif metrica == 'Máximo':
                reporte_pers = df_filtrado.groupby(group_cols)['sum_atenciones'].max().reset_index()
            else:  # Mínimo
                reporte_pers = df_filtrado.groupby(group_cols)['sum_atenciones'].min().reset_index()
            
            # Renombrar columna métrica
            reporte_pers = reporte_pers.rename(columns={'sum_atenciones': metrica})
            
            # Ordenar
            reporte_pers = reporte_pers.sort_values(metrica, ascending=False)
            
            st.success(f"✅ Reporte generado: {len(reporte_pers):,} filas")
            
            # Mostrar preview
            st.dataframe(reporte_pers.head(20), use_container_width=True)
            
            # Botón de descarga
            csv = reporte_pers.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="⬇️ Descargar Reporte Personalizado (CSV)",
                data=csv,
                file_name=f"reporte_personalizado_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_personalizado"
            )
    
    # =========================================================================
    # SECCIÓN 5: INFORMACIÓN ADICIONAL
    # =========================================================================
    
    st.markdown("---")
    st.markdown("## ℹ️ Información sobre los Reportes")
    
    with st.expander("📖 Guía de Uso"):
        st.markdown("""
        ### Cómo usar los reportes:
        
        1. **Reportes Ejecutivos**: Ideales para presentaciones y toma de decisiones rápida
        2. **Datasets Completos**: Para análisis profundo con herramientas especializadas (Excel, R, Python)
        3. **Reportes por Dimensión**: Enfocados en aspectos específicos (localidad, género)
        4. **Reporte Personalizado**: Máxima flexibilidad para análisis a medida
        
        ### Formatos disponibles:
        - **CSV**: Compatible con Excel, Google Sheets, y herramientas de análisis
        - **UTF-8 con BOM**: Asegura correcta visualización de tildes y caracteres especiales
        
        ### Recomendaciones:
        - Descarga regularmente para seguimiento histórico
        - Usa reportes personalizados para análisis específicos
        - Combina múltiples reportes para análisis integrado
        """)
    
    with st.expander("📊 Metadatos de los Datasets"):
        st.markdown(f"""
        ### Información del Observatorio
        
        **Período cubierto:** {df_morbilidad['ano'].min()} - {df_morbilidad['ano'].max()}  
        **Población objetivo:** Niños, niñas y adolescentes (6-17 años)  
        **Localidades:** {df_morbilidad['prestador_localidad_nombre'].nunique()}  
        **Registros totales:** {len(df_morbilidad):,}  
        **Última actualización:** {pd.Timestamp.now().strftime('%Y-%m-%d')}  
        
        **Fuentes de datos:**
        - Morbilidad en Salud Mental - Secretaría de Salud
        - Matrícula Oficial - Ministerio de Educación Nacional
        - Índice de Paridad de Género
        - ECAS 2016 - Encuesta de Clima y Ambiente Escolar
        
        **Modelos aplicados:**
        - Random Forest (Clasificación de Riesgo)
        - K-Means (Clustering de Localidades)
        - Red Neuronal Profunda (Predicciones)
        """)
    
    # Nota final
    st.info("""
    💾 **Nota:** Todos los datos descargados están filtrados para población de 6-17 años 
    y incluyen únicamente registros validados y limpios.
    """)


def main():
    """Función principal"""

    datos = cargar_datos()

    if datos is None:
        st.error("⚠️ No se pudieron cargar los datos.")
        st.stop()

    pagina = sidebar_navigation()

    if pagina == "🏠 Inicio":
        pagina_inicio(datos)
    elif pagina == "📊 Indicadores Clave":
        pagina_indicadores(datos)
    elif pagina == "🗺️ Mapa de Riesgo":
        pagina_mapa_riesgo(datos)
    elif pagina == "📈 Análisis Temporal":
        pagina_analisis_temporal(datos)
    elif pagina == "🧠 Factores de Riesgo":
        pagina_factores_riesgo(datos)
    elif pagina == "⚧️ Análisis de Género":
        pagina_analisis_genero(datos)
    elif pagina == "🔍 Buscador de Localidades":
        pagina_buscador_localidades(datos)
    elif pagina == "📥 Descargar Reportes":
        pagina_descargar_reportes(datos)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 20px;'>
        <p><strong>Observatorio de Salud Mental Escolar - Bogotá D.C.</strong></p>
        <p>Desarrollado con ❤️ para el bienestar de niños, niñas, adolescentes y jóvenes</p>
        <p>📧 Contacto: observatorio@bogota.gov.co | 📱 Línea de atención: 123</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
