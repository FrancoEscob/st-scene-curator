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
    
    if 'selected_scene' not in st.session_state:
        st.session_state.selected_scene = None
        print("[TERMINAL INIT] ✅ selected_scene inicializado")
    
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
                        print(f"[TERMINAL APP] 🔄 Ejecutando st.rerun()...")
                        st.rerun()  # Refrescar para mostrar las escenas
                    else:
                        print(f"[TERMINAL APP] ❌ No se pudieron detectar escenas en el video")
                        print(f"[TERMINAL APP] ⚠️ Lista de escenas vacía o None")
                        st.error("❌ No se pudieron detectar escenas en el video")
                        st.write("⚠️ Lista de escenas vacía o None")
                        
                except Exception as e:
                    print(f"[TERMINAL APP] ❌ ERROR durante el análisis: {str(e)}")
                    print(f"[TERMINAL APP] 🐛 Tipo de error: {type(e).__name__}")
                    import traceback
                    print(f"[TERMINAL APP] 📋 Stack trace:")
                    print(traceback.format_exc())
                    
                    st.error(f"❌ Error durante el análisis: {str(e)}")
                    st.write(f"🐛 Tipo de error: {type(e).__name__}")
                    st.code(traceback.format_exc())
                    logging.error(f"Error en análisis: {e}")
                    
                    # Fallback a datos de ejemplo
                    st.warning("🔄 Usando datos de ejemplo para continuar...")
                    st.session_state.scenes = get_sample_scenes()
                    st.session_state.analysis_completed = True
                    st.write("✅ Datos de ejemplo cargados")
            else:
                st.error("❌ Formato de video no soportado")
                st.write(f"🔍 Validación falló para: {st.session_state.video_path}")
    
    # Información del proyecto
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Estado del Proyecto")
    if st.session_state.analysis_completed:
        st.sidebar.metric("Escenas detectadas", len(st.session_state.scenes))
        processed_scenes = len([s for s in st.session_state.scenes if s.get('status') == 'processed'])
        st.sidebar.metric("Escenas procesadas", processed_scenes)
    else:
        st.sidebar.info("Carga un video para comenzar")

def render_main_interface():
    """Renderiza la interfaz principal con editor de video y panel de anotación."""
    
    print(f"[TERMINAL INTERFACE] 🎬 Iniciando render_main_interface()")
    print(f"[TERMINAL INTERFACE] 📊 Estado: analysis_completed={st.session_state.analysis_completed}, scenes={len(st.session_state.scenes) if st.session_state.scenes else 0}")
    
    # Debug: Estado actual
    st.write("🔍 DEBUG - Estado actual:")
    st.write(f"  - analysis_completed: {st.session_state.analysis_completed}")
    st.write(f"  - scenes disponibles: {len(st.session_state.scenes) if st.session_state.scenes else 0}")
    st.write(f"  - video_file: {st.session_state.video_file.name if st.session_state.video_file else 'None'}")
    
    # Capturar el valor exacto antes de la condición
    analysis_completed_value = st.session_state.analysis_completed
    print(f"[TERMINAL INTERFACE] 🔍 Valor capturado de analysis_completed: {analysis_completed_value}")
    print(f"[TERMINAL INTERFACE] 🔍 Tipo de valor: {type(analysis_completed_value)}")
    print(f"[TERMINAL INTERFACE] 🔍 Evaluación de 'not analysis_completed': {not analysis_completed_value}")
    
    if not analysis_completed_value:
        print(f"[TERMINAL INTERFACE] 📋 Mostrando pantalla de bienvenida (analysis_completed = False)")
        st.write("📋 Mostrando pantalla de bienvenida (analysis_completed = False)")
        # Pantalla de bienvenida
        st.title("🎬 ST Scene Curat-o-matic")
        st.markdown("""
        ### Herramienta de Curación y Anotación de Escenas de Stranger Things
        
        **¿Cómo funciona?**
        1. 📁 **Carga** un archivo de video del episodio en la barra lateral
        2. ⚙️ **Configura** el umbral de detección según tus necesidades
        3. 🔍 **Analiza** el video para detectar escenas automáticamente
        4. ✂️ **Edita** las escenas en el timeline interactivo
        5. 📝 **Anota** cada escena con personajes y contexto narrativo
        6. 🚀 **Envía** las escenas curadas al pipeline de IA
        
        **Funcionalidades del Editor:**
        - 🎯 Selección de escenas en timeline visual
        - ✂️ Ajuste preciso de tiempos (trimming)
        - 🔗 Fusión de escenas adyacentes
        - ✂️ División de escenas en puntos específicos
        - 👥 Anotación de personajes presentes
        - 📖 Notas de contexto narrativo
        
        **¡Comienza cargando un video en la barra lateral!**
        """)
        return
    
    print(f"[TERMINAL INTERFACE] 🎬 Mostrando interfaz del editor (analysis_completed = True)")
    print(f"[TERMINAL INTERFACE] ✅ EJECUTANDO RAMA ELSE - INTERFAZ DEL EDITOR")
    st.write("🎬 Mostrando interfaz del editor (analysis_completed = True)")
    st.write("✅ EJECUTANDO RAMA ELSE - INTERFAZ DEL EDITOR")
    
    # Interfaz principal del editor
    st.title("🎬 Editor de Escenas")
    
    # Layout de dos columnas
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📹 Reproductor de Video")
        
        # Placeholder para el reproductor de video
        if st.session_state.video_file:
            # TODO: Implementar reproductor sincronizado en ETAPA 4
            st.info("🚧 Reproductor de video (se implementará en ETAPA 4)")
            st.video(st.session_state.video_file)
        
        st.subheader("⏱️ Timeline de Escenas")
        # TODO: Implementar timeline interactivo en ETAPA 3
        st.info("🚧 Timeline interactivo (se implementará en ETAPA 3)")
        
        # Vista temporal de lista de escenas
        if st.session_state.scenes:
            st.markdown("**Escenas detectadas:**")
            
            # Estadísticas rápidas
            total_scenes = len(st.session_state.scenes)
            total_duration = sum(scene['duration'] for scene in st.session_state.scenes)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Escenas", total_scenes)
            with col2:
                st.metric("Duración Total", f"{total_duration/60:.1f} min")
            with col3:
                avg_duration = total_duration / total_scenes if total_scenes > 0 else 0
                st.metric("Duración Promedio", f"{avg_duration:.1f}s")
            
            st.divider()
            
            for scene in st.session_state.scenes:
                col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
                with col1:
                    st.write(f"**{scene['id']}**")
                with col2:
                    st.write(f"{scene['start_timecode']} - {scene['end_timecode']}")
                with col3:
                    st.write(f"Duración: {scene['duration']:.1f}s")
                with col4:
                    status_color = {
                        'detected': '🔍',
                        'edited': '✏️', 
                        'annotated': '📝',
                        'processed': '✅'
                    }
                    st.write(f"{status_color.get(scene['status'], '❓')} {scene['status']}")
                with col5:
                    if st.button("📝", key=f"select_{scene['id']}", help="Seleccionar para anotar"):
                        st.session_state.selected_scene = scene
                        st.rerun()
    
    with col_right:
        render_annotation_panel()

def render_annotation_panel():
    """Renderiza el panel de anotación contextual."""
    st.subheader("📝 Panel de Anotación")
    
    if st.session_state.selected_scene is None:
        st.info("👈 Selecciona una escena del timeline para comenzar a anotar")
        return
    
    # Obtener la escena seleccionada
    selected_scene_data = st.session_state.selected_scene
    
    if selected_scene_data is None:
        st.error("Error: Escena no encontrada")
        return
    
    # Información de la escena
    st.markdown(f"### 🎬 {selected_scene_data['id']}")
    st.markdown(f"**Duración:** {selected_scene_data['duration']:.1f} segundos")
    st.markdown(f"**Tiempo:** {selected_scene_data['start_timecode']} - {selected_scene_data['end_timecode']}")
    
    # TODO: Implementar vista previa de fotogramas en ETAPA 5
    st.markdown("**Vista previa:**")
    st.info("🚧 Fotogramas de vista previa (se implementarán en ETAPA 5)")
    
    # Anotación de personajes
    st.markdown("**👥 Personajes presentes:**")
    characters = [char['name'] for char in st.session_state.characters_data['characters']]
    
    selected_characters = st.multiselect(
        "Selecciona los personajes que aparecen en esta escena",
        characters,
        key=f"characters_{selected_scene_data['id']}"
    )
    
    # Notas de contexto narrativo
    st.markdown("**📖 Notas de Contexto Narrativo:**")
    narrative_notes = st.text_area(
        "Notas de Contexto para la IA (Callbacks, Simbolismo, Lore):",
        placeholder="Ejemplo: Esta escena muestra el primer encuentro de Eleven con el Demogorgon. Importante para el arco narrativo de la temporada. Referencias al Upside Down y experimentos del laboratorio.",
        height=150,
        key=f"notes_{selected_scene_data['id']}"
    )
    
    # Estado de la escena
    st.markdown("**📊 Estado:**")
    status_color = {
        "Sin procesar": "🔴",
        "En cola": "🟡", 
        "Procesado": "🟢"
    }
    st.markdown(f"{status_color.get(selected_scene_data['status'], '⚪')} {selected_scene_data['status']}")
    
    # Botón de procesamiento
    st.markdown("---")
    process_scene_button = st.button(
        "🚀 Enviar a Procesamiento IA",
        use_container_width=True,
        disabled=selected_scene_data['status'] == "Procesado"
    )
    
    if process_scene_button:
        # TODO: Implementar pipeline de IA en ETAPA 6
        st.success("🚧 Pipeline de IA (se implementará en ETAPA 6)")
        # Actualizar estado temporalmente
        for scene in st.session_state.scenes:
            if scene['id'] == selected_scene_data['id']:
                scene['status'] = "processed"
                break
        st.rerun()

def main():
    """Función principal de la aplicación."""
    print(f"[TERMINAL MAIN] 🚀 Iniciando main()")
    initialize_session_state()
    print(f"[TERMINAL MAIN] ✅ Session state inicializado")
    print(f"[TERMINAL MAIN] 📊 Estado actual: analysis_completed={st.session_state.analysis_completed}, scenes={len(st.session_state.scenes) if st.session_state.scenes else 0}")
    
    render_sidebar()
    print(f"[TERMINAL MAIN] ✅ Sidebar renderizado")
    
    render_main_interface()
    print(f"[TERMINAL MAIN] ✅ Main interface renderizada")

if __name__ == "__main__":
    main()