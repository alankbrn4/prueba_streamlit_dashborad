import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='LIAD6002 Dashboard', layout='wide', page_icon='🇲🇽')

# Cargar datos
df = pd.read_csv('datos_dashboard.csv')
df['fecha'] = pd.to_datetime(df['fecha'])

# HEADER
st.title('🇲🇽 Dashboard — Análisis de Datos No Estructurados')
st.markdown('**LIAD6002** | ICE — Ingeniería en Análisis de Datos')
st.markdown('---')

# SIDEBAR — Filtros
st.sidebar.header('🔍 Filtros')
sector_sel = st.sidebar.multiselect('Sector', df['sector'].unique(), default=df['sector'].unique())
fuente_sel = st.sidebar.multiselect('Fuente', df['fuente'].unique(), default=df['fuente'].unique())
sent_sel = st.sidebar.multiselect('Sentimiento', df['sentimiento'].unique(), default=df['sentimiento'].unique())

# Filtrar
mask = (df['sector'].isin(sector_sel)) & (df['fuente'].isin(fuente_sel)) & (df['sentimiento'].isin(sent_sel))
df_f = df[mask]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric('📝 Registros', f'{len(df_f):,}')
col2.metric('😡 % Negativo', f'{(df_f["sentimiento"]=="NEG").mean()*100:.0f}%')
col3.metric('📊 Score medio', f'{df_f["score_sentimiento"].mean():.3f}')
col4.metric('🏙️ Ciudades', f'{df_f["ciudad"].nunique()}')

st.markdown('---')

# GRÁFICAS
c1, c2 = st.columns(2)
with c1:
    fig1 = px.pie(df_f, names='sentimiento', title='Distribución de Sentimiento',
                 color='sentimiento', color_discrete_map={'NEG':'#E74C3C','POS':'#27AE60','NEU':'#3498DB'})
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.histogram(df_f, x='sector', color='sentimiento', barmode='group',
                        title='Sentimiento por Sector',
                        color_discrete_map={'NEG':'#E74C3C','POS':'#27AE60','NEU':'#3498DB'})
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    df_time = df_f.set_index('fecha').resample('D').size().reset_index(name='count')
    fig3 = px.line(df_time, x='fecha', y='count', title='Actividad Temporal')
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = px.box(df_f, x='sector', y='score_sentimiento', color='sector',
                 title='Score de Sentimiento por Sector')
    st.plotly_chart(fig4, use_container_width=True)

# TABLA
st.markdown('### 📋 Datos Filtrados')
st.dataframe(df_f.head(50), use_container_width=True)

# FOOTER
st.markdown('---')
st.markdown('*Dr. Alan David Blanco Miranda | LIAD6002 | ICE | 2026*')
