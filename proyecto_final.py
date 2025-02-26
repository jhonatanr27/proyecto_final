import streamlit as st
import pandas as pd
import plotly as px

# Título de la aplicación Streamlit
st.title("Panel de Visualización de Datos Energéticos")

# Cargar los datos
# Asumiendo que los datos están guardados como 'energy_data.csv'
data = pd.read_csv("energy_data.csv")

# Mostrar los datos crudos
st.subheader("Datos Crudos")
st.dataframe(data)

# Barra lateral para filtros
st.sidebar.header("Filtros")

# Filtro por Departamento
departamentos = data["DEPARTAMENTO"].unique()
departamento_seleccionado = st.sidebar.multiselect("Seleccionar Departamento", departamentos, default=departamentos)

# Filtro por Tipo de Energía
tipos_energia = data["Energia_Prioritaria"].unique()
energia_seleccionada = st.sidebar.multiselect("Seleccionar Tipo de Energía", tipos_energia, default=tipos_energia)

# Aplicar filtros
datos_filtrados = data[
    (data["DEPARTAMENTO"].isin(departamento_seleccionado)) &
    (data["Energia_Prioritaria"].isin(energia_seleccionada))
]

# Mostrar datos filtrados
st.subheader("Datos Filtrados")
st.dataframe(datos_filtrados)

# Visualización 1: Gráfico de barras del consumo promedio de energía por departamento
st.subheader("Consumo Promedio de Energía por Departamento")
consumo_promedio = datos_filtrados.groupby("DEPARTAMENTO")["consumo_energia_promedio"].mean().reset_index()
fig1 = px.bar(consumo_promedio, x="DEPARTAMENTO", y="consumo_energia_promedio", 
              title="Consumo Promedio de Energía por Departamento",
              labels={"consumo_energia_promedio": "Consumo Promedio de Energía (kWh)"})
st.plotly_chart(fig1)

# Visualización 2: Gráfico de barras de la distribución de tipos de energía
st.subheader("Distribución de Tipos de Energía Priorizados")
dist_energia = datos_filtrados["Energia_Prioritaria"].value_counts().reset_index()
dist_energia.columns = ["Energia_Prioritaria", "Cantidad"]
fig2 = px.bar(dist_energia, x="Energia_Prioritaria", y="Cantidad", 
              title="Distribución de Tipos de Energía Priorizados",
              labels={"Cantidad": "Número de Localidades"})
st.plotly_chart(fig2)

# Visualización 3: Mapa de localidades
st.subheader("Distribución Geográfica de Localidades")
fig3 = px.scatter_mapbox(datos_filtrados, 
                         lat="Latitud", 
                         lon="Longitud", 
                         hover_name="LOCALIDAD", 
                         hover_data=["Energia_Prioritaria", "consumo_energia_promedio"],
                         color="Energia_Prioritaria", 
                         size="consumo_energia_promedio",
                         zoom=4, 
                         height=600)
fig3.update_layout(mapbox_style="open-street-map")
fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig3)

# Estadísticas resumidas
st.subheader("Estadísticas Resumidas")
st.write(datos_filtrados.describe())

# Instrucciones para ejecutar la aplicación
st.markdown("""
### Cómo Ejecutar Esta Aplicación
1. Guarda este script como `app.py`.
2. Asegúrate de que tus datos estén guardados como `energy_data.csv` en el mismo directorio.
3. Ejecuta la aplicación con el comando: `streamlit run app.py`.
""")
