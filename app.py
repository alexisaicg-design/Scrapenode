import streamlit as st
import pandas as pd
import os
from main import run_pipeline

st.set_page_config(page_title="ScrapeNode | Monitoreo B2B", layout="wide")

st.title("📊 Portal de Inteligencia de Datos y Licitaciones")
st.markdown("---")

# Botón de ejecución directa del pipeline desde la UI
col_btn, _ = st.columns([1, 4])
with col_btn:
    if st.button("🔄 Actualizar Datos Ahora"):
        with st.spinner("Ejecutando scraper..."):
            run_pipeline()
        st.success("¡Pipeline ejecutado con éxito!")
        st.rerun()

csv_file = "licitaciones_extraidas.csv"

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)

    # Panel de Métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("Registros Capturados", len(df))
    col2.metric("Estado del Pipeline", "Activo (OK)")
    col3.metric("Monitoreo", "24/7 Automático")

    st.markdown("---")

    # Buscador y Filtrado
    search = st.text_input("🔍 Buscar por palabra clave o título:")
    if search:
        df_filtered = df[df["titulo"].str.contains(search, case=False, na=False)]
    else:
        df_filtered = df

    # Tabla Interactiva (Sintaxis actualizada)
    st.dataframe(df_filtered, width="stretch")

    # Descarga de Reportes
    st.download_button(
        label="📥 Descargar Reporte Ejecutivo (CSV)",
        data=df_filtered.to_csv(index=False).encode("utf-8"),
        file_name="reporte_licitaciones.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ No se encontró el archivo 'licitaciones_extraidas.csv'. Presiona 'Actualizar Datos Ahora' o ejecuta 'python main.py'.")
    