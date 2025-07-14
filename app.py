import streamlit as st
import pandas as pd
import json
from pathlib import Path
import logging
from utils.scene_detection import detect_scenes_streamlit, validate_video_file, get_sample_scenes

# Configuración de la página
st.set_page_config(
    page_title="ST Scene Curat-o-matic",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_characters_data():
    """Carga los datos de personajes desde el archivo JSON."""
    try:
        with open('data/characters.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Datos de fallback si no existe el archivo
        return {
            "characters": [
                {"name": "Eleven", "actor": "Millie Bobby Brown"},
                {"name": "Mike Wheeler", "actor": "Finn Wolfhard"},
                {"name": "Dustin Henderson", "actor": "Gaten Matarazzo"},
                {"name": "Lucas Sinclair", "actor": "Caleb McLaughlin"},
                {"name": "Will Byers", "actor": "Noah Schnapp"},
                {"name": "Max Mayfield", "actor": "Sadie Sink"},
                {"name": "Steve Harrington", "actor": "Joe Keery"},
                {"name": "Nancy Wheeler", "actor": "Natalia Dyer"},
                {"name": "Jonathan Byers", "actor": "Charlie Heaton"},
                {"name": "Joyce Byers", "actor": "Winona Ryder"},
                {"name": "Jim Hopper", "actor": "David Harbour"},
                {"name": "Robin Buckley", "actor": "Maya Hawke"}
            ]
        }

def initialize_session_state():
    """Inicializa el estado de la sesión con valores por defecto."""
    print("[TERMINAL INIT] 🔧 Inicializando session state...")
    
    if 'video_file' not in st.session_state:
        st.session_state.video_file = None
        print("[TERMINAL INIT] ✅ video_file inicializado")
    
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
        print("[TERMINAL INIT] ✅ video_path inicializado")
    
    if 'threshold' not in st.session_state:
        st.session_state.threshold = 30.0
        print("[TERMINAL INIT] ✅ threshold inicializado")
    
    if 'scenes' not in st.session_state:
        st.session_state.scenes = []
        print("[TERMINAL INIT] ✅ scenes inicializado como lista vacía")
    else:
        print(f"[TERMINAL INIT] 📋 scenes ya existe: {len(st.session_state.scenes)} elementos")
    
    if 'selected_scene_id' not in st.session_state:
        st.session_state.selected_scene_id = None
        print("[TERMINAL INIT] ✅ selected_scene_id inicializado")
    
    if 'characters_data' not in st.session_state:
        st.session_state.characters_data = load_characters_data()
        print("[TERMINAL INIT] ✅ characters_data inicializado")
    
    if 'analysis_completed' not in st.session_state:
        st.session_state.analysis_completed = False
        print("[TERMINAL INIT] ✅ analysis_completed inicializado como False")
    else:
        print(f"[TERMINAL INIT] 📊 analysis_completed ya existe: {st.session_state.analysis_completed}")
    
    if 'video_info' not in st.session_state:
        st.session_state.video_info = None
        print("[TERMINAL INIT] ✅ video_info inicializado")
    
    print(f"[TERMINAL INIT] 🏁 Estado final: analysis_completed={st.session_state.analysis_completed}, scenes={len(st.session_state.scenes)}")

def render_sidebar():
    """Renderiza la barra lateral con configuración del episodio."""
    st.sidebar.title("🎬 ST Scene Curat-o-matic")
    st.sidebar.markdown("---")
    
    st.sidebar.header("📁 Configuración del Episodio")
    
    # Carga de archivo de video
    uploaded_file = st.sidebar.file_uploader(
        "Selecciona el archivo de video del episodio",
        type=['mp4', 'avi', 'mov', 'mkv'],
        help="Formatos soportados: MP4, AVI, MOV, MKV"
    )
    
    if uploaded_file is not None:
        # Solo procesar si es un archivo nuevo o diferente
        is_new_file = (
            st.session_state.video_file is None or 
            st.session_state.video_file.name != uploaded_file.name
        )
        
        print(f"[TERMINAL SIDEBAR] 📁 Archivo detectado: {uploaded_file.name}")
        print(f"[TERMINAL SIDEBAR] 🔍 Es archivo nuevo: {is_new_file}")
        
        if is_new_file:
            print(f"[TERMINAL SIDEBAR] 🆕 Procesando archivo nuevo: {uploaded_file.name}")
            # Guardar archivo temporalmente
            import tempfile
            import os
            
            # Crear archivo temporal con nombre único
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}")
            temp_path = temp_file.name
            temp_file.close()  # Cerrar el archivo antes de escribir
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.session_state.video_file = uploaded_file
            st.session_state.video_path = temp_path
            st.session_state.analysis_completed = False  # Reset analysis solo para archivo nuevo
            print(f"[TERMINAL SIDEBAR] ✅ Archivo nuevo guardado, analysis_completed reseteado a False")
            
            st.sidebar.success(f"✅ Archivo cargado: {uploaded_file.name}")
        else:
            print(f"[TERMINAL SIDEBAR] ♻️ Archivo ya cargado: {uploaded_file.name}, manteniendo estado actual")
            st.sidebar.success(f"✅ Archivo cargado: {uploaded_file.name}")
    
    # Configuración de detección
    st.sidebar.subheader("⚙️ Configuración de Detección")
    threshold = st.sidebar.slider(
        "Umbral de sensibilidad",
        min_value=10,
        max_value=50,
        value=27,
        help="Valor más bajo = más escenas detectadas. Valor más alto = menos escenas."
    )
    
    # Botón de procesamiento
    st.sidebar.markdown("---")
    process_button = st.sidebar.button(
        "🔍 1. Analizar y Cargar Episodio",
        disabled=st.session_state.video_file is None,
        use_container_width=True
    )
    
    if process_button and st.session_state.video_file is not None:
        with st.sidebar:
            print(f"[TERMINAL APP] 🔍 INICIO DEL PROCESO DE ANÁLISIS")
            print(f"[TERMINAL APP] 📁 Archivo: {st.session_state.video_file.name}")
            print(f"[TERMINAL APP] 📂 Ruta temporal: {st.session_state.video_path}")
            print(f"[TERMINAL APP] ⚙️ Umbral: {threshold}")
            
            st.write("🔍 INICIO DEL PROCESO DE ANÁLISIS")
            st.write(f"📁 Archivo: {st.session_state.video_file.name}")
            st.write(f"📂 Ruta temporal: {st.session_state.video_path}")
            st.write(f"⚙️ Umbral: {threshold}")
            
            if validate_video_file(st.session_state.video_path):
                print(f"[TERMINAL APP] ✅ Archivo de video validado correctamente")
                st.write("✅ Archivo de video validado correctamente")
                try:
                    print(f"[TERMINAL APP] 🚀 Iniciando detección de escenas...")
                    st.write("🚀 Iniciando detección de escenas...")
                    
                    # Detectar escenas usando PySceneDetect
                    print(f"[TERMINAL APP] 📞 Llamando a detect_scenes_streamlit()...")
                    scenes = detect_scenes_streamlit(
                        st.session_state.video_path, 
                        threshold
                    )
                    print(f"[TERMINAL APP] 📞 detect_scenes_streamlit() retornó: {type(scenes)} con {len(scenes) if scenes else 0} elementos")
                    
                    st.write(f"📊 RESULTADO: {len(scenes) if scenes else 0} escenas detectadas")
                    st.write(f"🔍 Tipo de resultado: {type(scenes)}")
                    print(f"[TERMINAL APP] 📊 RESULTADO: {len(scenes) if scenes else 0} escenas detectadas")
                    print(f"[TERMINAL APP] 🔍 Tipo de resultado: {type(scenes)}")
                    
                    if scenes:
                        print(f"[TERMINAL APP] ✅ Guardando escenas en session_state...")
                        st.write("✅ Guardando escenas en session_state...")
                        st.session_state.scenes = scenes
                        print(f"[TERMINAL APP] ✅ Escenas guardadas: {len(st.session_state.scenes)} elementos")
                        
                        st.session_state.analysis_completed = True
                        print(f"[TERMINAL APP] ✅ analysis_completed = {st.session_state.analysis_completed}")
                        
                        st.write(f"📋 Session state actualizado:")
                        st.write(f"  - scenes: {len(st.session_state.scenes)} elementos")
                        st.write(f"  - analysis_completed: {st.session_state.analysis_completed}")
                        
                        print(f"[TERMINAL APP] 📋 Session state actualizado:")
                        print(f"[TERMINAL APP]   - scenes: {len(st.session_state.scenes)} elementos")
                        print(f"[TERMINAL APP]   - analysis_completed: {st.session_state.analysis_completed}")
                        
                        st.success(f"✅ ¡Análisis completado! Detectadas {len(scenes)} escenas")
                        print(f"[TERMINAL APP] ✅ ¡Análisis completado! Detectadas {len(scenes)} escenas")
                        
                        st.write("🔄 Ejecutando st.rerun()...")
                        st.rerun()
                    else:
                        st.error("No se detectaron escenas. Prueba con un umbral más bajo.")
                        print(f"[TERMINAL APP] ❌ No se detectaron escenas.")
                except Exception as e:
                    st.error(f"Ocurrió un error durante el análisis: {e}")
                    logging.error(f"Error en la detección de escenas: {e}", exc_info=True)
                    print(f"[TERMINAL APP] ❌ Ocurrió un error durante el análisis: {e}")
            else:
                st.error("El archivo de video no es válido o no se puede procesar.")
                print(f"[TERMINAL APP] ❌ El archivo de video no es válido.")

# Función display_interactive_timeline eliminada - será reemplazada por timeline de chips

# Función handle_scene_merging eliminada - será reemplazada por herramientas de edición

def render_timeline_chips(scenes):
    """Renderiza la timeline horizontal con chips clickeables para cada escena"""
    if not scenes:
        st.info("No hay escenas para mostrar")
        return
    
    # CSS personalizado para los chips
    st.markdown("""
    <style>
    .chip-button {
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        border-radius: 20px;
        padding: 8px 16px;
        margin: 4px;
        font-size: 14px;
        font-weight: 500;
        color: #374151;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
        min-width: 120px;
        text-align: center;
    }
    
    .chip-button:hover {
        background-color: #e5e7eb;
        border-color: #9ca3af;
        transform: translateY(-1px);
    }
    
    .chip-selected {
        background-color: #3b82f6 !important;
        border-color: #2563eb !important;
        color: white !important;
    }
    
    .chip-selected:hover {
        background-color: #2563eb !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("**🎞️ Selecciona una escena:**")
    
    # Crear columnas para los chips
    cols_per_row = 4
    num_scenes = len(scenes)
    
    for i in range(0, num_scenes, cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            scene_idx = i + j
            if scene_idx < num_scenes:
                scene = scenes[scene_idx]
                scene_id = f"scene_{scene_idx + 1}"
                duration = scene['end_time'] - scene['start_time']
                
                with cols[j]:
                    # Determinar si este chip está seleccionado
                    is_selected = st.session_state.get('selected_scene_id') == scene_id
                    
                    # Crear el botón chip
                    button_key = f"chip_{scene_idx}"
                    if st.button(
                        f"Escena {scene_idx + 1}\n{duration:.1f}s",
                        key=button_key,
                        disabled=is_selected,
                        help=f"Tiempo: {scene['start_time']:.1f}s - {scene['end_time']:.1f}s\nConfianza: {scene['confidence']:.2f}"
                    ):
                        st.session_state.selected_scene_id = scene_id
                        st.rerun()


# --- Interfaz Principal ---
def main():
    """Función principal que renderiza la aplicación Streamlit."""
    initialize_session_state()
    render_sidebar()

    st.title("Editor Visual de Escenas")
    st.markdown("---")

    if not st.session_state.analysis_completed:
        st.info("👋 ¡Bienvenido! Por favor, carga un video y haz clic en 'Analizar' en la barra lateral para comenzar.")
        # Mostrar video si ya está cargado pero no analizado
        if st.session_state.video_path:
            st.video(st.session_state.video_path)
    else:
        # --- Layout principal con columnas ---
        col1, col2 = st.columns([3, 2])

        with col1:
            st.header("🎬 Reproductor y Timeline")
            if st.session_state.video_path:
                st.video(st.session_state.video_path)
            
            # ETAPA 2: Timeline de chips implementada
            st.subheader("🎞️ Timeline de Escenas")
            render_timeline_chips(st.session_state.scenes)
            
            # Mostrar información de la escena seleccionada
            if st.session_state.get('selected_scene_id'):
                selected_idx = int(st.session_state.selected_scene_id.split('_')[1]) - 1
                if 0 <= selected_idx < len(st.session_state.scenes):
                    selected_scene = st.session_state.scenes[selected_idx]
                    st.info(f"🎯 **Escena seleccionada:** {st.session_state.selected_scene_id} | "
                           f"**Tiempo:** {selected_scene['start_time']:.1f}s - {selected_scene['end_time']:.1f}s | "
                           f"**Duración:** {selected_scene['end_time'] - selected_scene['start_time']:.1f}s")
            
            # Herramientas de edición - se implementarán en ETAPA 3
            st.info("🚧 Herramientas de edición (Group/Cut) se implementarán en ETAPA 3")

        with col2:
            st.header("📝 Panel de Anotación")
            st.info("🚧 Panel de anotación completo se implementará en ETAPA 4")
            
            # Mostrar información básica de escenas por ahora
            st.subheader("Escenas Detectadas")
            if st.session_state.scenes:
                df_display = pd.DataFrame(st.session_state.scenes)
                df_display['start'] = df_display['start_timecode']
                df_display['end'] = df_display['end_timecode']
                df_display['duration_s'] = df_display['duration']
                st.dataframe(df_display[['id', 'start', 'end', 'duration_s']], use_container_width=True)
            else:
                st.info("No hay escenas para mostrar.")

if __name__ == "__main__":
    main()