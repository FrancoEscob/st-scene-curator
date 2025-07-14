import streamlit as st
import pandas as pd
from datetime import timedelta

# --- INICIALIZACIÓN Y DATOS DE EJEMPLO ---

def initialize_state():
    if 'scenes' not in st.session_state:
        # Usamos datos de ejemplo hasta que se analice un video
        st.session_state.scenes = []
    if 'selected_scene_id' not in st.session_state:
        st.session_state.selected_scene_id = None
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None # Ruta al video analizado

def get_sample_scenes():
    # Simula la salida de PySceneDetect para la demo
    return [
        {'id': 'scene_001', 'start_time': 0, 'end_time': 8, 'duration': 8, 'notes': '', 'characters': []},
        {'id': 'scene_002', 'start_time': 8, 'end_time': 13, 'duration': 5, 'notes': '', 'characters': []},
        {'id': 'scene_003', 'start_time': 13, 'end_time': 28, 'duration': 15, 'notes': '', 'characters': []},
        {'id': 'scene_004', 'start_time': 28, 'end_time': 63, 'duration': 35, 'notes': '', 'characters': []},
        {'id': 'scene_005', 'start_time': 63, 'end_time': 71, 'duration': 8, 'notes': '', 'characters': []},
    ]

# --- COMPONENTES DE LA INTERFAZ ---

def render_timeline(scenes):
    st.subheader("Timeline")
    
    # Inyectamos CSS para que los botones parezcan "chips"
    st.markdown("""
        <style>
            .stButton>button {
                border-radius: 8px;
                border: 1px solid #555;
                padding: 10px 15px;
                margin: 2px;
                width: 150px; /* Ancho fijo para cada chip */
            }
            .stButton>button:hover {
                border-color: #00A3FF;
                color: #00A3FF;
            }
            /* Estilo para el botón seleccionado */
            div[data-testid*="stButton"] > button[disabled] {
                background-color: #00A3FF !important;
                color: white !important;
                border: 1px solid #00A3FF !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Creamos una fila horizontal con scroll
    # Usamos st.columns dentro de un contenedor para simular el scroll horizontal si hay muchas escenas
    cols = st.columns(len(scenes))
    for i, scene in enumerate(scenes):
        with cols[i]:
            # El botón se deshabilita si es el seleccionado, para resaltarlo visualmente
            is_selected = (scene['id'] == st.session_state.get('selected_scene_id'))
            if st.button(f"{scene['id']}\n({scene['duration']:.1f}s)", key=scene['id'], disabled=is_selected):
                st.session_state.selected_scene_id = scene['id']
                st.rerun()

def render_annotation_panel():
    st.header("📝 Panel de Anotación")
    
    selected_id = st.session_state.get('selected_scene_id')
    
    if selected_id is None:
        st.info("Selecciona una escena de la timeline para ver sus detalles y editarla.")
        return

    # Encontrar la escena seleccionada en nuestra lista de estado
    # Usamos un generador para encontrarlo eficientemente
    scene_index, scene_data = next(
        ((i, s) for i, s in enumerate(st.session_state.scenes) if s['id'] == selected_id), 
        (None, None)
    )

    if scene_data is None:
        st.error("Error: La escena seleccionada no se encuentra. Refrescando...")
        st.session_state.selected_scene_id = None
        st.rerun()
        return

    st.subheader(f"Editando: `{scene_data['id']}`")
    st.write(f"**Duración:** {scene_data['duration']:.2f} segundos")
    
    # Widgets para editar
    # Ejemplo con una lista de personajes predefinida
    all_characters = ["Eleven", "Max", "Dustin", "Lucas", "Mike", "Eddie", "Steve", "Nancy", "Robin"]
    selected_chars = st.multiselect(
        "Personajes en la escena",
        options=all_characters,
        default=scene_data.get('characters', [])
    )
    
    notes = st.text_area(
        "Contexto adicional (narrativa semántica)",
        value=scene_data.get('notes', ''),
        height=200
    )
    
    # Guardar los cambios en el estado de la sesión
    st.session_state.scenes[scene_index]['characters'] = selected_chars
    st.session_state.scenes[scene_index]['notes'] = notes


# --- LÓGICA DE EDICIÓN ---

def render_editing_tools():
    st.subheader("Herramientas de Edición")
    
    # --- Lógica de Fusión (GROUP) ---
    st.markdown("##### 🔗 Unir Escenas (Group)")
    scene_ids = [s['id'] for s in st.session_state.scenes]
    scenes_to_merge = st.multiselect("Selecciona 2 o más escenas para unir:", options=scene_ids)
    
    if st.button("Unir seleccionadas", disabled=len(scenes_to_merge) < 2):
        # Lógica de fusión que ya tenías
        # (Aquí va el código para encontrar min_start, max_end, crear nueva escena, etc.)
        st.success(f"Se unieron {len(scenes_to_merge)} escenas.")
        # Aquí actualizas st.session_state.scenes
        # st.rerun()

    # --- Lógica de División (CUT) ---
    st.markdown("##### ✂️ Dividir Escena (Cut)")
    selected_id = st.session_state.get('selected_scene_id')
    
    if selected_id:
        st.write(f"Dividir la escena seleccionada: `{selected_id}`")
        cut_timestamp = st.number_input("Introducir el timestamp (en segundos) para el corte:", min_value=0.0, format="%.2f")
        if st.button("Dividir", disabled=cut_timestamp <= 0):
            # Lógica de división
            st.success(f"Escena {selected_id} dividida en el segundo {cut_timestamp}.")
            # Aquí actualizas st.session_state.scenes
            # st.rerun()
    else:
        st.info("Selecciona una escena en la timeline para poder dividirla.")


# --- APLICACIÓN PRINCIPAL ---

# 1. Inicializar estado
initialize_state()

# Simular la carga de un video y el análisis
# En tu app real, esto estaría dentro de la lógica del botón "Analizar"
if not st.session_state.scenes:
    if st.sidebar.button("Simular Análisis de Video"):
        st.session_state.scenes = get_sample_scenes()
        st.session_state.video_path = "path/to/your/video.mp4" # Placeholder
        st.rerun()

# 2. Renderizar la interfaz
st.title("🎬 Editor Visual de Escenas")
st.markdown("---")

if not st.session_state.scenes:
    st.info("Carga y analiza un video para comenzar.")
else:
    # --- Layout principal ---
    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.header("Reproductor y Timeline")
        
        # Sincronizar video con la escena seleccionada
        start_time = 0
        if st.session_state.selected_scene_id:
            scene_data = next((s for s in st.session_state.scenes if s['id'] == st.session_state.selected_scene_id), None)
            if scene_data:
                start_time = int(scene_data['start_time'])
        
        #st.video(st.session_state.video_path, start_time=start_time)
        st.image("https://i.imgur.com/k2oT3Iu.png", caption=f"Video player (simulado). Debería empezar en el segundo {start_time}")
        
        render_timeline(st.session_state.scenes)
        render_editing_tools()

    with right_col:
        render_annotation_panel()

    # Para depuración: Muestra el estado actual
    with st.expander("Ver estado actual de `session_state`"):
        st.json(st.session_state.scenes)