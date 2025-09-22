import streamlit as st
import pandas as pd

# ---------------------------
# Cargar datos del Excel
# ---------------------------
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

# ---------------------------
# Diccionario de palabras clave relacionadas con códigos
# ---------------------------
palabras_clave = {
    # --- Código 207 ---
    "aceite wd40": 207, "aceite lubricante": 207, "agua destilada": 207, "anti óxido": 207,
    "arandelas": 207, "arena": 207, "bornera": 207, "brocas para taladro": 207,
    "bulones": 207, "cable": 207, "cabo trenzado": 207, "candado": 207, "caño pvc": 207,
    "caño galvanizado": 207, "cemento": 207, "cinta aisladora": 207, "cinta autosoldable": 207,
    "cinta enmascarar": 207, "conector abulonado": 207, "cruceta": 207, "disyuntor": 207,
    "electrodo": 207, "esmalte sintético": 207, "espuma de poliuretano": 207,
    "fotocontrol": 207, "fusible": 207, "grampas": 207, "grasa conductora": 207,
    "hierros varios": 207, "hilo al recocido": 207, "ladrillo": 207, "linterna": 207,
    "llave térmica": 207, "loseta de hormigón": 207, "manguera": 207,
    "materiales de pinturería": 207, "materiales varios de ferretería": 207,
    "malla de hierro": 207, "morceto": 207, "mosquetón": 207,
    "panel led para sub-estación": 207, "perfil normal": 207, "perfiles de hierro": 207,
    "piedra": 207, "pilas": 207, "placa alto impacto": 207,
    "placas compensadas de madera": 207, "planchuela de hierro": 207,
    "precintos": 207, "silicona": 207, "soga": 207, "soporte reconectador": 207,
    "terminal pre-aislado": 207, "termocontraible": 207, "trapos de algodón": 207,
    "tuerca hexagonal": 207, "varilla roscada": 207, "zapatilla prolongador": 207,

    # --- Código 227 ---
    "arco sierra": 227, "caja de herramientas": 227, "cepillo de acero": 227,
    "cincha con criquet": 227, "cortacables": 227, "cortafierro": 227, "cúter": 227,
    "disco de corte": 227, "eslinga": 227, "espátula": 227, "hacha": 227, "lima": 227,
    "llave allen": 227, "llave t": 227, "llave combinada": 227, "mechas": 227,
    "pala": 227, "pinza": 227, "pulsiana": 227, "sierra copa": 227,
    "soldador tubular": 227, "soplete soldador": 227,

    # --- Código 200 ---
    "calculadora": 200, "cortina": 200, "escritorio": 200, "estufa": 200,
    "heladera": 200, "pava eléctrica": 200, "pizarra": 200, "silla": 200, "ventilador": 200,

    # --- Código 202 ---
    "alicate corta perno": 202, "amoladora angular": 202, "binoculares": 202,
    "bomba centrífuga": 202, "bomba estercolera": 202, "cajón porta herramienta": 202,
    "electrobomba": 202, "generador": 202, "hormigonera": 202, "llave de impacto": 202,
    "manómetro": 202, "motosierra": 202, "pinza hidráulica prensa terminales": 202,
    "pistola para pintar": 202, "podadora de altura": 202,
    "relaciómetro": 202, "rotomartillo": 202, "sierra sable": 202,
    "sunchadora": 202, "taladro": 202, "taladro hoyador": 202
}

# ---------------------------
# Interfaz en Streamlit
# ---------------------------
st.title("Buscador de Códigos y Matrículas")

data = load_data()

# Nivel 1 → Selección de modo
modo = st.selectbox("Elegí el modo de búsqueda:", ["CÓDIGOS", "MATRÍCULAS"])

if modo == "CÓDIGOS":
    # Nivel 2 → Subcategorías
    categoria = st.selectbox("Elegí la categoría:", ["SUCURSALES", "AGENCIAS", "COMPRAS", "MOVILIDADES"])
    query = st.text_input("Escribí el número o una palabra para buscar:")

    if query:
        query_lower = query.lower()

        # Buscar coincidencias en palabras clave (parciales)
        coincidencias = [(palabra, codigo) for palabra, codigo in palabras_clave.items() if query_lower in palabra]

        if coincidencias:
            df = data[categoria]
            for palabra_completa, codigo_encontrado in coincidencias:
                resultado = df[df["CÓDIGO"] == codigo_encontrado]
                if not resultado.empty:
                    st.success(
                        f"Palabra clave encontrada: **{palabra_completa.capitalize()}**\n\n"
                        f"Código {codigo_encontrado}: {resultado.iloc[0]['DESCRIPCIÓN']}"
                    )
                else:
                    st.warning(f"La palabra clave '{palabra_completa}' coincide con el código {codigo_encontrado}, pero no está en esta categoría.")
        else:
            # Buscar en el Excel directamente
            df = data[categoria]
            mask = df.apply(lambda row: query_lower in str(row["CÓDIGO"]).lower() or query_lower in str(row["DESCRIPCIÓN"]).lower(), axis=1)
            resultados = df[mask]
            if not resultados.empty:
                st.write(resultados)
            else:
                st.warning("No se encontraron resultados.")

elif modo == "MATRÍCULAS":
    query = st.text_input("Escribí el número o una palabra para buscar en MATRÍCULAS:")

    if query:
        query_lower = query.lower()
        df = data["MATRICULAS"]

        mask = df.apply(lambda row: query_lower in str(row["CÓDIGO"]).lower() or query_lower in str(row["DESCRIPCIÓN"]).lower(), axis=1)
        resultados = df[mask]

        if not resultados.empty:
            st.write(resultados)
        else:
            st.warning("No se encontraron resultados en Matrículas.")
