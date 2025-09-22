import streamlit as st
import pandas as pd

# Cargar el Excel (ajustar el nombre a tu archivo real)
@st.cache_data
def load_data():
    xls = pd.ExcelFile("matriculas.xlsx")
    data = {
        "MATRICULAS": xls.parse("MATRICULAS"),
        "SUCURSALES": xls.parse("SUCURSALES"),
        "COMPRAS": xls.parse("COMPRAS"),
        "AGENCIAS": xls.parse("AGENCIAS"),
        "MOVILIDADES": xls.parse("MOVILIDADES"),
    }
    return data

data = load_data()

# Interfaz
st.title("🔎 Buscador de Materiales y Códigos")

# Selector de pestaña
sheet = st.selectbox(
    "Elegí la categoría:",
    ["MATRICULAS", "SUCURSALES", "COMPRAS", "AGENCIAS", "MOVILIDADES"]
)

# Buscador
query = st.text_input("Escribí el número o una palabra para buscar:")

if query:
    df = data[sheet]
    query = str(query).lower()

    if sheet == "MATRICULA":
        mask = df.apply(lambda row:
            query in str(row["MATRICULA"]).lower() or query in str(row["MATERIAL"]).lower(),
            axis=1
        )
    else:
        mask = df.apply(lambda row:
            query in str(row["CÓDIGO"]).lower() or query in str(row["DESCRIPCIÓN"]).lower(),
            axis=1
        )

    results = df[mask]

    if not results.empty:
        st.write("### Resultados encontrados:")
        st.dataframe(results)
    else:
        st.warning("No se encontraron resultados.")
