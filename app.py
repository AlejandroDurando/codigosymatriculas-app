import streamlit as st
import pandas as pd

# 🔑 Diccionario de palabras clave → código relacionado
keyword_map = {
    # Código 207
    "aceite wd40": "207", "aceite lubricante": "207", "agua destilada": "207",
    "anti óxido": "207", "arandelas": "207", "arena": "207", "bornera": "207",
    "brocas para taladro": "207", "bulones": "207", "cable": "207", "cabo trenzado": "207",
    "candado": "207", "caño pvc": "207", "caño galvanizado": "207", "cemento": "207",
    "cinta aisladora": "207", "cinta autosoldable": "207", "cinta enmascarar": "207",
    "conector abulonado": "207", "cruceta": "207", "disyuntor": "207", "electrodo": "207",
    "esmalte sintético": "207", "espuma de poliuretano": "207", "fotocontrol": "207",
    "fusible": "207", "grampas": "207", "grasa conductora": "207", "hierros varios": "207",
    "hilo al recocido": "207", "ladrillo": "207", "linterna": "207", "llave térmica": "207",
    "loseta de hormigón": "207", "manguera": "207", "materiales de pinturería": "207",
    "materiales varios de ferretería": "207", "malla de hierro": "207", "morceto": "207",
    "mosquetón": "207", "panel led": "207", "perfil normal": "207", "perfiles de hierro": "207",
    "piedra": "207", "pilas": "207", "placa alto impacto": "207", "placas compensadas": "207",
    "planchuela de hierro": "207", "precintos": "207", "silicona": "207", "soga": "207",
    "soporte reconectador": "207", "terminal pre-aislado": "207", "termocontraible": "207",
    "trapos de algodón": "207", "tuerca exagonal": "207", "varilla roscada": "207",
    "zapatilla prolongador": "207",

    # Código 227
    "arco sierra": "227", "caja de herramientas": "227", "cepillo de acero": "227",
    "cincha con criquet": "227", "cortacables": "227", "cortafierro": "227", "cutter": "227",
    "disco de corte": "227", "eslinga": "227", "espátula": "227", "hacha": "227", "lima": "227",
    "llave allen": "227", "llave t": "227", "llave combinada": "227", "mechas": "227",
    "pala": "227", "pinza": "227", "pulsiana": "227", "sierra copa": "227",
    "soldador tubular": "227", "soplete soldador": "227",

    # Código 200
    "calculadora": "200", "cortina": "200", "escritorio": "200", "estufa": "200",
    "heladera": "200", "pava electrica": "200", "pizarra": "200", "silla": "200",
    "ventilador": "200",

    # Código 202
    "alicate corta perno": "202", "amoladora angular": "202", "binoculares": "202",
    "bomba centrífuga": "202", "bomba estercolera": "202", "cajón porta herramienta": "202",
    "electrobomba": "202", "generador": "202", "hormigonera": "202", "llave de impacto": "202",
    "manómetro": "202", "motosierra": "202", "pinza hidráulica prensa terminales": "202",
    "pistola para pintar": "202", "podadora de altura": "202", "relaciómetro": "202",
    "rotomartillo": "202", "sierra sable": "202", "sunchadora": "202",
    "taladro": "202", "taladro hoyador": "202"
}

# Cargar Excel
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

st.title("🔎 Buscador de Materiales y Códigos")

sheet = st.selectbox(
    "Elegí la categoría:",
    ["MATRICULAS", "SUCURSALES", "COMPRAS", "AGENCIAS", "MOVILIDADES"]
)

query = st.text_input("Escribí el número o una palabra para buscar:")

if query:
    q = query.lower().strip()

    # Primero verificamos palabras clave
    if q in keyword_map:
        st.success(f"La palabra clave coincide con el código {keyword_map[q]}")
    else:
        df = data[sheet]
        if sheet == "MATRICULAS":
            mask = df.apply(lambda row: q in str(row["MATRICULA"]).lower() or q in str(row["MATERIAL"]).lower(), axis=1)
        else:
            mask = df.apply(lambda row: q in str(row["CÓDIGO"]).lower() or q in str(row["DESCRIPCIÓN"]).lower(), axis=1)
        results = df[mask]

        if not results.empty:
            st.write("### Resultados encontrados:")
            st.dataframe(results)
        else:
            st.warning("No se encontraron resultados.")
