import streamlit as st
import pandas as pd

# ===============================
# Cargar Excel
# ===============================
@st.cache_data
def load_data():
    xls = pd.ExcelFile("matriculas.xlsx")
    data = {
        "MATRICULAS": xls.parse("MATRICULAS"),
        "SUCURSALES": xls.parse("SUCURSALES"),
        "COMPRAS": xls.parse("COMPRAS"),
        "AGENCAS": xls.parse("AGENCIA"),
        "MOVILIDADES": xls.parse("MOVILIDADES"),
    }
    return data

data = load_data()

# ===============================
# Diccionario de palabras clave
# ===============================
keywords = {
    "aceite wd40": 207,
    "aceite lubricante": 207,
    "agua destilada": 207,
    "cafetera": "47040002",  # ejemplo para matriculas
}

# ===============================
# Interfaz
# ===============================
st.title("🔎 Buscador de Códigos y Matrículas")

modo = st.selectbox("Elegí el modo:", ["MATRICULAS", "CODIGOS"])

if modo == "CODIGOS":
    categoria = st.selectbox(
        "Elegí la categoría:", 
        ["SUCURSALES", "COMPRAS", "AGENCAS", "MOVILIDADES"]
    )
else:
    categoria = "MATRICULAS"

df = data[categoria]

# ===============================
# Buscador
# ===============================
query = st.text_input("Escribí el número o una palabra para buscar:")

if query:
    query_lower = query.lower()

    # 🔹 Primero, verificamos si la palabra clave está definida
    matched_code = None
    for key, code in keywords.items():
        if query_lower in key:  
            matched_code = code
            st.success(f"🔑 Palabra clave detectada: **{key}** → Código {code}")
            break

    # 🔹 Ahora filtramos en el DataFrame
    if categoria == "MATRICULAS":
        mask = df.apply(lambda row:
            query_lower in str(row["MATRICULA"]).lower() or 
            query_lower in str(row["MATERIAL"]).lower(),
            axis=1
        )
        results = df[mask]

        if not results.empty:
            for _, row in results.iterrows():
                st.info(f"**Matrícula:** {row['MATRICULA']}  \n"
                        f"**Material:** {row['MATERIAL']}  \n"
                        f"**Bien de Uso:** {row['BIEN DE USO']}")
        else:
            st.warning("No se encontraron resultados.")

    else:  # CODIGOS
        mask = df.apply(lambda row:
            query_lower in str(row["CÓDIGO"]).lower() or 
            query_lower in str(row["DESCRIPCIÓN"]).lower(),
            axis=1
        )
        results = df[mask]

        if not results.empty:
            for _, row in results.iterrows():
                st.info(f"**Código {row['CÓDIGO']}** → {row['DESCRIPCIÓN']}")
        else:
            st.warning("No se encontraron resultados.")
