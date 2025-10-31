import streamlit as st
import pandas as pd
import re
import unicodedata

# ---------- Helpers de normalización ----------
def strip_accents(s: str) -> str:
    """Quita tildes/diacríticos."""
    return "".join(
        c for c in unicodedata.normalize("NFD", str(s))
        if unicodedata.category(c) != "Mn"
    )

def norm(s) -> str:
    """Normaliza para comparar: sin tildes, minúsculas, trim."""
    return strip_accents(str(s)).lower().strip()

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Quita espacios y pasa a mayúsculas para evitar errores por variantes
    mapping = {c: c.strip().upper() for c in df.columns}
    df = df.rename(columns=mapping)
    # Normaliza variantes con/sin tilde o espacios
    if "CÓDIGO" in df.columns and "CODIGO" not in df.columns:
        df = df.rename(columns={"CÓDIGO": "CODIGO"})
    if "DESCRIPCIÓN" in df.columns and "DESCRIPCION" not in df.columns:
        df = df.rename(columns={"DESCRIPCIÓN": "DESCRIPCION"})
    if "BIEN DE USO" in df.columns and "BIEN_DE_USO" not in df.columns:
        df = df.rename(columns={"BIEN DE USO": "BIEN_DE_USO"})
    return df

@st.cache_data
def load_data():
    xls = pd.ExcelFile("matriculas.xlsx")
    data = {
        "MATRICULAS": normalize_columns(xls.parse("MATRICULAS")),
        "SUCURSALES": normalize_columns(xls.parse("SUCURSALES")),
        "COMPRAS":    normalize_columns(xls.parse("COMPRAS")),
        "AGENCIAS":   normalize_columns(xls.parse("AGENCIAS")),
        "MOVILIDADES":normalize_columns(xls.parse("MOVILIDADES")),
    }
    return data

# ---------- Resaltado ignorando tildes ----------
def highlight(text: str, q: str) -> str:
    """
    Resalta coincidencias de q en text ignorando tildes y mayúsculas/minúsculas,
    conservando el texto original.
    """
    if not q:
        return str(text)

    original = str(text)

    # Construimos una versión sin tildes + un mapa de índices al original
    norm_chars = []
    index_map = []  # index_map[i_norm] = i_original
    for i, ch in enumerate(original):
        decomp = unicodedata.normalize("NFD", ch)
        for d in decomp:
            if unicodedata.category(d) != "Mn":
                norm_chars.append(d)
                index_map.append(i)
    norm_text = "".join(norm_chars).lower()
    norm_q = norm(q)

    if not norm_q:
        return original

    pattern = re.compile(re.escape(norm_q), re.IGNORECASE)
    result = []
    last_orig = 0

    for m in pattern.finditer(norm_text):
        # m.start/end están en el string normalizado → mapeamos al original
        start_norm, end_norm = m.start(), m.end()
        start_orig = index_map[start_norm]
        end_orig = index_map[end_norm - 1] + 1  # fin exclusivo

        result.append(original[last_orig:start_orig])
        result.append(
            f"<mark style='background:yellow;color:black;font-weight:600'>"
            f"{original[start_orig:end_orig]}"
            f"</mark>"
        )
        last_orig = end_orig

    result.append(original[last_orig:])
    return "".join(result)

# ---------- Palabras clave -> código ----------
keyword_map = {
    # 207
    "aceite wd40": "207","aceite lubricante":"207","agua destilada":"207","anti óxido":"207","arandelas":"207",
    "arena":"207","bornera":"207","brocas para taladro":"207","bulones":"207","cable":"207","cabo trenzado":"207",
    "candado":"207","caño pvc":"207","caño galvanizado":"207","cemento":"207","cinta aisladora":"207",
    "cinta autosoldable":"207","cinta enmascarar":"207","conector abulonado":"207","cruceta":"207","disyuntor":"207",
    "electrodo":"207","esmalte sintético":"207","espuma de poliuretano":"207","fotocontrol":"207","fusible":"207",
    "grampas":"207","grasa conductora":"207","hierros varios":"207","hilo al recocido":"207","ladrillo":"207",
    "linterna":"207","llave térmica":"207","loseta de hormigón":"207","manguera":"207",
    "materiales de pinturería":"207","materiales varios de ferretería":"207","malla de hierro":"207","morceto":"207",
    "mosquetón":"207","panel led para sub-estación":"207","perfil normal":"207","perfiles de hierro":"207","piedra":"207",
    "pilas":"207","placa alto impacto":"207","placas compensadas de madera":"207","planchuela de hierro":"207",
    "precintos":"207","silicona":"207","soga":"207","soporte reconectador":"207","terminal pre-aislado":"207",
    "termocontraible":"207","trapos de algodón":"207","tuerca exagonal":"207","varilla roscada":"207",
    "zapatilla prolongador":"207",
    # 227
    "arco sierra":"227","caja de herramientas":"227","cepillo de acero":"227","cincha con criquet":"227",
    "cortacables":"227","cortafierro":"227","cutter":"227","disco de corte":"227","eslinga":"227","espátula":"227",
    "hacha":"227","lima":"227","llave allen":"227","llave t":"227","llave combinada":"227","mechas":"227","pala":"227",
    "pinza":"227","pulsiana":"227","sierra copa":"227","soldador tubular":"227","soplete soldador":"227",
    # 200
    "calculadora":"200","cortina":"200","escritorio":"200","estufa":"200","heladera":"200","pava electrica":"200",
    "pizarra":"200","silla":"200","ventilador":"200",
    # 202
    "alicate corta perno":"202","amoladora angular":"202","binoculares":"202","bomba centrífuga":"202",
    "bomba estercolera":"202","cajón porta herramienta":"202","electrobomba":"202","generador":"202","hormigonera":"202",
    "llave de impacto":"202","manómetro":"202","motosierra":"202","pinza hidráulica prensa terminales":"202",
    "pistola para pintar":"202","podadora de altura":"202","relaciómetro":"202","rotomartillo":"202","sierra sable":"202",
    "sunchadora":"202","taladro":"202","taladro hoyador":"202",
}

# ---------- UI ----------
st.title("🔎 Buscador de Códigos y Matrículas")
data = load_data()

modo = st.selectbox("Elegí el modo de búsqueda:", ["CÓDIGOS", "MATRÍCULAS"])

if modo == "CÓDIGOS":
    categoria = st.selectbox("Elegí la categoría:", ["SUCURSALES", "AGENCIAS", "COMPRAS", "MOVILIDADES"])
    df = data[categoria]
    q = st.text_input("Escribí el número o una palabra para buscar:")

    if q:
        qn = norm(q)  # <-- sin tildes, lowercase

        # 1) Coincidencias por palabras clave (parcial, ignorando tildes)
        matches = [(phrase, code) for phrase, code in keyword_map.items() if qn in norm(phrase)]

        if matches:
            for phrase, code in matches:
                rows = df[df["CODIGO"].astype(str) == str(code)]
                if not rows.empty:
                    desc = rows.iloc[0]["DESCRIPCION"]
                    st.markdown(
                        f"""
                        <div style="background:#0f5132;border:1px solid #14532d;border-radius:12px;padding:14px;margin:10px 0">
                          <h4 style="color:#00ffc8;margin:0 0 6px">🔑 Palabra clave: {highlight(phrase, q)}</h4>
                          <div style="color:#fff">Código <b>{code}</b>: {highlight(desc, q)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.warning(f"La palabra clave '{phrase}' apunta al código {code}, pero no existe en **{categoria}**.")

        # 2) Búsqueda normal en código/descr. (ignorando tildes)
        mask = df.apply(
            lambda r: qn in norm(r.get("CODIGO","")) or qn in norm(r.get("DESCRIPCION","")),
            axis=1
        )
        results = df[mask]

        if not results.empty:
            for _, r in results.iterrows():
                st.markdown(
                    f"""
                    <div style="background:#1e1e1e;border:1px solid #444;border-radius:12px;padding:14px;margin:10px 0">
                      <h4 style="color:#00ffc8;margin:0 0 6px">📌 Código {r['CODIGO']}</h4>
                      <div style="color:#fff">{highlight(r['DESCRIPCION'], q)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        elif not matches:
            st.warning("⚠️ No se encontraron resultados.")

else:  # MATRÍCULAS
    df = data["MATRICULAS"]
    q = st.text_input("Escribí número de matrícula o parte del material:")
    if q:
        qn = norm(q)  # <-- sin tildes

        mask = df.apply(
            lambda r: qn in norm(r.get("MATRICULA","")) or qn in norm(r.get("MATERIAL","")),
            axis=1
        )
        results = df[mask]

        if not results.empty:
            for _, r in results.iterrows():
                material = highlight(r.get("MATERIAL",""), q)
                st.markdown(
                    f"""
                    <div style="background:#1e1e1e;border:1px solid #444;border-radius:12px;padding:14px;margin:10px 0">
                      <h4 style="color:#00ffc8;margin:0 0 6px">🔖 Matrícula {r.get('MATRICULA','')}</h4>
                      <div style="color:#fff">{material}</div>
                      <div style="color:#bbb;margin-top:6px">Bien de uso: <b>{r.get('BIEN_DE_USO', r.get('BIEN DE USO',''))}</b></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("⚠️ No se encontraron resultados en Matrículas.")
