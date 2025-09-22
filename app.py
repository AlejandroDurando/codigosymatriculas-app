import streamlit as st
import pandas as pd
import re

# =========================
# Cargar Excel
# =========================
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

# =========================
# Palabras clave → Código
# =========================
palabras_clave = {
    "aceite wd40": "207",
    "aceite lubricante": "207",
    "agua destilada": "207",
    "anti óxido": "207",
    "arandelas": "207",
    "arco sierra": "227",
    "caja de herramientas": "227",
    "calculadora": "200",
    "cortina": "200",
    "alicate corta perno": "202",
    "amoladora angular": "202",
}

# =========================
# Interfaz
# =========================
st.title("🔎 Buscador de Materiales, Códigos y Matrículas")

modo = st.selectbox("Elegí el modo:", ["CÓDIGOS", "MATRICULAS"])

if modo == "CÓDIGOS":
    categoria = st.selectbox(
        "Elegí la categoría:",
        ["SUCURSALES", "AGENCIAS", "COMPRAS", "MOVILIDADES"]
    )
else:
    categoria = "MATRICULAS"

query = st.text_input("Escribí el número o una palabra para buscar:")

# =========================
# Función de resaltado
# =========================
def resaltar(texto, query):
    if not query:
        return texto
    regex = re.compile(re.escape(query), re.IGNORECASE)
    return regex.sub(f"<mark style='background-color:yellow;color:black;font-weight:bold;'>{query}</mark>", str(texto))

# =========================
# Búsqueda
# =========================
if query:
    df = data[categoria]

    # Buscar coincidencia en palabras clave
    match = None
    for palabra, codigo in palabras_clave.items():
        if query.lower() in palabra.lower():
            match = (palabra, codigo)
            break

    if match:
        palabra, codigo = match
        resultados = df[df["CÓDIGO"].astype(str) == codigo]

        if not resultados.empty:
            row = resultados.iloc[0]
            st.markdown(
                f"""
                <div style="background-color:#0f5132;padding:15px;border-radius:10px;margin-bottom:10px;border:1px solid #14532d;">
                    <h3 style="color:#00ffcc;">✅ Palabra clave: {palabra.title()}</h3>
                    <p style="color:white;font-size:16px;">Código {row['CÓDIGO']}: {row['DESCRIPCIÓN']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ Palabra clave encontrada, pero no hay descripción disponible en esta categoría.")
    else:
        # Buscar en columnas directamente
        mask = df.apply(lambda row:
            query.lower() in str(row["CÓDIGO"]).lower() or
            query.lower() in str(row["DESCRIPCIÓN"]).lower(),
            axis=1
        )
        resultados = df[mask]

        if not resultados.empty:
            if len(resultados) == 1:
                row = resultados.iloc[0]
                st.markdown(
                    f"""
                    <div style="background-color:#0f5132;padding:15px;border-radius:10px;margin-bottom:10px;border:1px solid #14532d;">
                        <h3 style="color:#00ffcc;">✅ Código {row['CÓDIGO']}</h3>
                        <p style="color:white;font-size:16px;">{resaltar(row['DESCRIPCIÓN'], query)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                for _, row in resultados.iterrows():
                    st.markdown(
                        f"""
                        <div style="background-color:#1e1e1e;padding:15px;border-radius:10px;margin-bottom:10px;border:1px solid #444;">
                            <h4 style="color:#00ffcc;">📌 Código {row['CÓDIGO']}</h4>
                            <p style="color:white;">{resaltar(row['DESCRIPCIÓN'], query)}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.warning("⚠️ No se encontraron resultados.")
