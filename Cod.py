import streamlit as st
import pandas as pd

# ---------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------
st.set_page_config(page_title="Cuestionario Pruebas Estadísticas", layout="centered")

RAW_GITHUB_URL = "https://raw.githubusercontent.com/usuario/repositorio/rama/items.csv"  # <-- CAMBIAR AQUÍ

@st.cache_data
def cargar_items():
    return pd.read_csv(RAW_GITHUB_URL)

# Cargar datos
try:
    items = cargar_items()
except Exception as e:
    st.error(f"Error cargando los datos: {e}")
    st.stop()

# Asegurarse de que existan columnas requeridas
columnas_requeridas = {"pregunta", "opcion_a", "opcion_b", "opcion_c", "opcion_d", "respuesta_correcta"}
if not columnas_requeridas.issubset(set(items.columns)):
    st.error("El CSV no contiene las columnas necesarias: pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta")
    st.stop()

# ---------------------------------------------
# ESTADOS DE SESIÓN
# ---------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0

if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0

if "respondido" not in st.session_state:
    st.session_state.respondido = False

if "retro" not in st.session_state:
    st.session_state.retro = ""


# ---------------------------------------------
# FUNCIÓN PARA AVANZAR
# ---------------------------------------------
def siguiente_pregunta():
    st.session_state.indice += 1
    st.session_state.respondido = False
    st.session_state.retro = ""


# ---------------------------------------------
# MOSTRAR PREGUNTA ACTUAL
# ---------------------------------------------
if st.session_state.indice < len(items):

    fila = items.iloc[st.session_state.indice]

    st.title("Cuestionario: Elección de Pruebas Estadísticas")
    st.subheader(f"Pregunta {st.session_state.indice + 1} de {len(items)}")

    st.write(f"### {fila['pregunta']}")

    opciones = {
        "A": fila["opcion_a"],
        "B": fila["opcion_b"],
        "C": fila["opcion_c"],
        "D": fila["opcion_d"]
    }

    seleccion = st.radio("Selecciona una opción:", list(opciones.keys()))

    # Botón para responder
    if st.button("Responder"):

        if st.session_state.respondido:
            st.warning("Ya respondiste esta pregunta.")
        else:
            correcta = fila["respuesta_correcta"].strip().upper()

            if seleccion == correcta:
                st.session_state.puntaje += 1
                st.session_state.retro = "✅ ¡Correcto!"
            else:
                st.session_state.retro = f"❌ Incorrecto. La respuesta correcta era: **{correcta}**"

            st.session_state.respondido = True

    # Mostrar retroalimentación
    if st.session_state.respondido:
        st.info(st.session_state.retro)

        if st.button("Siguiente"):
            siguiente_pregunta()

else:
    # ---------------------------------------------
    # RESULTADO FINAL
    # ---------------------------------------------
    st.title("🎉 ¡Has terminado el cuestionario!")
    st.subheader("Resultados finales:")
    st.success(f"Puntaje obtenido: **{st.session_state.puntaje} / {len(items)}**")

    if st.button("Reiniciar cuestionario"):
        st.session_state.indice = 0
        st.session_state.puntaje = 0
        st.session_state.respondido = False
        st.session_state.retro = ""
