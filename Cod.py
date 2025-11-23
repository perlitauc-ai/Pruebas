import streamlit as st
import pandas as pd

# ------------------------------------------------------
# CARGAR ÍTEMS DESDE GITHUB
# ------------------------------------------------------
@st.cache_data
def cargar_items(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error cargando los datos: {e}")
        return pd.DataFrame()

# ------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ------------------------------------------------------
st.set_page_config(page_title="Cuestionario Estadístico", page_icon="📊")

st.title("📊 Cuestionario de Pruebas Estadísticas")
st.write("Responde cada ítem. Recibirás retroalimentación inmediata.")

# ------------------------------------------------------
# URL DEL ARCHIVO EN GITHUB (RAW)
# ⚠️ IMPORTANTE: REEMPLAZA ESTO POR TU LINK REAL RAW
# ------------------------------------------------------
url_items = "https://raw.githubusercontent.com/usuario/repositorio/rama/items.csv"

items = cargar_items(url_items)

if items.empty:
    st.stop()

# ------------------------------------------------------
# CONTROL DE ESTADO
# ------------------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0

if "aciertos" not in st.session_state:
    st.session_state.aciertos = 0

if "respondido" not in st.session_state:
    st.session_state.respondido = False

if "seleccion" not in st.session_state:
    st.session_state.seleccion = None


total = len(items)

# ------------------------------------------------------
# MOSTRAR ÍTEM ACTUAL
# ------------------------------------------------------
if st.session_state.indice < total:

    fila = items.iloc[st.session_state.indice]
    pregunta = fila["pregunta"]
    opciones = fila["opciones"].split(";")
    correcta = fila["respuesta_correcta"]

    st.subheader(f"Pregunta {st.session_state.indice + 1} de {total}")
    st.write(pregunta)

    # Selección del usuario
    seleccion = st.radio("Selecciona una opción:", opciones, key=f"preg_{st.session_state.indice}")

    # Botón para responder
    if st.button("Responder") and not st.session_state.respondido:
        st.session_state.respondido = True
        st.session_state.seleccion = seleccion

        # Retroalimentación
        if seleccion == correcta:
            st.success("✔ ¡Correcto!")
            st.session_state.aciertos += 1
        else:
            st.error(f"✘ Incorrecto. La respuesta correcta es: **{correcta}**")

    # Botón para continuar
    if st.session_state.respondido:
        if st.button("Siguiente ➜"):
            st.session_state.indice += 1
            st.session_state.respondido = False
            st.session_state.seleccion = None
            st.rerun()

else:
    # ------------------------------------------------------
    # RESULTADO FINAL
    # ------------------------------------------------------
    st.success("🎉 ¡Has completado el cuestionario!")

    st.subheader("Resultados")
    st.write(f"**Aciertos:** {st.session_state.aciertos} de {total}")
    st.write(f"**Porcentaje:** {round((st.session_state.aciertos / total) * 100, 2)}%")

    if st.button("Reiniciar cuestionario"):
        st.session_state.indice = 0
        st.session_state.aciertos = 0
        st.session_state.respondido = False
        st.session_state.seleccion = None
        st.rerun()
