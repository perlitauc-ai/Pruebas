import streamlit as st
import pandas as pd
import requests

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
# CONFIGURACIÓN
# ------------------------------------------------------
st.set_page_config(page_title="Cuestionario Estadístico", page_icon="📊", layout="centered")

st.title("📊 Cuestionario para elegir pruebas estadísticas")
st.write("Responde cada pregunta. El dashboard mostrará retroalimentación inmediata.")

# URL DEL ARCHIVO RAW EN GITHUB (modifica por el tuyo)
url_items = "AQUÍ_VA_EL_LINK_RAW_DE_GITHUB"

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

if "respuesta_seleccionada" not in st.session_state:
    st.session_state.respuesta_seleccionada = None

if "respondido" not in st.session_state:
    st.session_state.respondido = False

total_preguntas = len(items)

# ------------------------------------------------------
# MOSTRAR UNA PREGUNTA A LA VEZ
# ------------------------------------------------------
if st.session_state.indice < total_preguntas:

    pregunta_actual = items.iloc[st.session_state.indice]
    pregunta = pregunta_actual["pregunta"]
    opciones = pregunta_actual["opciones"].split(";")
    respuesta_correcta = pregunta_actual["respuesta_correcta"]

    st.subheader(f"Pregunta {st.session_state.indice + 1} de {total_preguntas}")
    st.write(pregunta)

    # Selección del usuario
    seleccion = st.radio("Selecciona una respuesta:", opciones, key=f"radio_{st.session_state.indice}")

    # Botón para validar
    if st.button("Responder") and not st.session_state.respondido:
        st.session_state.respondido = True
        st.session_state.respuesta_seleccionada = seleccion

        if seleccion == respuesta_correcta:
            st.success("✔ ¡Correcto!")
            st.session_state.aciertos += 1
        else:
            st.error(f"✘ Incorrecto. La respuesta correcta es: **{respuesta_correcta}**")

    # Botón para avanzar
    if st.session_state.respondido:
        if st.button("Siguiente pregunta ➜"):
            st.session_state.indice += 1
            st.session_state.respondido = False
            st.session_state.respuesta_seleccionada = None
            st.rerun()

else:
    # ------------------------------------------------------
    # RESULTADO FINAL
    # ------------------------------------------------------
    st.success("🎉 ¡Has completado el cuestionario!")
    st.subheader("Resultados finales")
    st.write(f"**Aciertos:** {st.session_state.aciertos} de {total_preguntas}")
    st.write(f"**Puntaje (%):** {round((st.session_state.aciertos / total_preguntas) * 100, 2)}%")

    if st.button("Reiniciar cuestionario"):
        st.session_state.indice = 0
        st.session_state.aciertos = 0
        st.session_state.respondido = False
        st.rerun()
