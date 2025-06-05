import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="DashWise | Fitness Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
st.sidebar.image("https://i.imgur.com/9WnR2hD.png", width=180)
st.sidebar.title("DashWise")
st.sidebar.caption("Empowering local fitness businesses with data")

# --- Upload Data ---
st.sidebar.subheader("Upload your data")
uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx"])

# --- Main Content ---
st.title("📊 DashWise - Cork Fitness Intelligence Dashboard")

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # --- Data Preprocessing ---
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Día'] = df['Fecha'].dt.day_name()
    df['Hora'] = df['Fecha'].dt.hour

    # --- KPIs ---
    ingresos_totales = df['Ingresos'].sum()
    miembros_unicos = df['Cliente ID'].nunique()
    clases_realizadas = df['Actividad'].count()

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos Totales", f"€{ingresos_totales:,.2f}")
    col2.metric("Miembros Únicos", miembros_unicos)
    col3.metric("Clases Realizadas", clases_realizadas)

    st.markdown("---")

    # --- Activity Distribution ---
    actividad_count = df['Actividad'].value_counts().reset_index()
    actividad_count.columns = ['Actividad', 'Sesiones']
    fig_actividad = px.bar(actividad_count, x='Actividad', y='Sesiones', title="Actividad por Tipo", color='Actividad')
    st.plotly_chart(fig_actividad, use_container_width=True)

    # --- Attendance Heatmap ---
    heatmap_data = df.groupby(['Día', 'Hora']).size().reset_index(name='Asistencias')
    dias_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data['Día'] = pd.Categorical(heatmap_data['Día'], categories=dias_order, ordered=True)
    heatmap_pivot = heatmap_data.pivot(index='Hora', columns='Día', values='Asistencias').fillna(0)

    st.subheader("🕒 Asistencia por Día y Hora")
    st.dataframe(heatmap_pivot.style.background_gradient(cmap='YlOrRd'), height=400)

    # --- Simple AI Recommendation ---
    peak_hour = heatmap_data.loc[heatmap_data['Asistencias'].idxmax(), 'Hora']
    st.markdown("### 🤖 Recomendaciones Potenciadas por IA")
    st.info(f"El momento pico de asistencia es a las {peak_hour}:00. Considera añadir más sesiones en ese horario.")

else:
    st.warning("Por favor, sube un archivo Excel con tus datos de gimnasio para comenzar.")
