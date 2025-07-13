"""Módulo de detección de escenas usando PySceneDetect.

Este módulo proporciona funcionalidades para detectar escenas en videos
utilizando diferentes algoritmos de detección de PySceneDetect.
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import tempfile
import os

try:
    from scenedetect import open_video, SceneManager, detect
    from scenedetect.detectors import ContentDetector, ThresholdDetector
    from scenedetect.video_splitter import split_video_ffmpeg
    from scenedetect.frame_timecode import FrameTimecode
except ImportError as e:
    logging.error(f"Error importing PySceneDetect: {e}")
    raise ImportError("PySceneDetect no está instalado. Ejecuta: pip install scenedetect[opencv]")

import streamlit as st


class SceneDetector:
    """Clase principal para detección de escenas en videos."""
    
    def __init__(self, video_path: str, threshold: float = 30.0):
        """
        Inicializa el detector de escenas.
        
        Args:
            video_path: Ruta al archivo de video
            threshold: Umbral de sensibilidad para detección (0-100)
        """
        self.video_path = Path(video_path)
        self.threshold = threshold
        self.video = None
        self.scene_manager = None
        self.scenes = []
        
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video no encontrado: {video_path}")
    
    def _setup_managers(self) -> None:
        """Configura los managers de video y escenas."""
        try:
            # Abrir video usando la nueva API
            self.video = open_video(str(self.video_path))
            self.scene_manager = SceneManager()
            
            # Agregar detector de contenido con el umbral especificado
            self.scene_manager.add_detector(
                ContentDetector(threshold=self.threshold)
            )
            
        except Exception as e:
            logging.error(f"Error configurando managers: {e}")
            raise
    
    def detect_scenes(self, progress_callback=None) -> List[Dict]:
        """
        Detecta escenas en el video.
        
        Args:
            progress_callback: Función callback para mostrar progreso
            
        Returns:
            Lista de diccionarios con información de escenas
        """
        try:
            self._setup_managers()
            
            # Detectar escenas
            if progress_callback:
                progress_callback("Analizando video...")
            
            self.scene_manager.detect_scenes(
                video=self.video,
                show_progress=False  # Usamos nuestro propio callback
            )
            
            # Obtener lista de escenas
            scene_list = self.scene_manager.get_scene_list()
            
            # Procesar escenas
            self.scenes = self._process_scenes(scene_list)
            
            if progress_callback:
                progress_callback(f"Detectadas {len(self.scenes)} escenas")
            
            return self.scenes
            
        except Exception as e:
            logging.error(f"Error detectando escenas: {e}")
            raise
    
    def _process_scenes(self, scene_list: List[Tuple]) -> List[Dict]:
        """
        Procesa la lista de escenas raw de PySceneDetect.
        
        Args:
            scene_list: Lista de tuplas (start_time, end_time) donde cada elemento es un FrameTimecode
            
        Returns:
            Lista de diccionarios con información procesada
        """
        processed_scenes = []
        
        for i, scene_tuple in enumerate(scene_list):
            try:
                # Verificar que tenemos una tupla con dos elementos
                if not isinstance(scene_tuple, tuple) or len(scene_tuple) != 2:
                    logging.error(f"Scene {i}: Expected tuple with 2 elements, got {type(scene_tuple)}")
                    continue
                    
                start_time, end_time = scene_tuple
                
                # Verificar que son objetos FrameTimecode válidos
                if not (hasattr(start_time, 'get_seconds') and hasattr(end_time, 'get_seconds')):
                    logging.error(f"Scene {i}: Invalid FrameTimecode objects - start: {type(start_time)}, end: {type(end_time)}")
                    continue
                
                # Extraer información de los FrameTimecode
                start_seconds = start_time.get_seconds()
                end_seconds = end_time.get_seconds()
                duration_seconds = end_seconds - start_seconds
                
                # Obtener frames si el método existe
                start_frame = start_time.get_frames() if hasattr(start_time, 'get_frames') else 0
                end_frame = end_time.get_frames() if hasattr(end_time, 'get_frames') else 0
                
                scene_data = {
                    'id': f"scene_{i+1:03d}",
                    'index': i,
                    'start_time': start_seconds,
                    'end_time': end_seconds,
                    'duration': duration_seconds,
                    'start_frame': start_frame,
                    'end_frame': end_frame,
                    'start_timecode': str(start_time),
                    'end_timecode': str(end_time),
                    'status': 'detected',  # detected, edited, annotated, processed
                    'characters': [],
                    'notes': '',
                    'ai_analysis': None,
                    'thumbnail_path': None
                }
                processed_scenes.append(scene_data)
                
            except Exception as e:
                logging.error(f"Error processing scene {i}: {e}")
                continue
        
        return processed_scenes
    
    def get_video_info(self) -> Dict:
        """
        Obtiene información básica del video.
        
        Returns:
            Diccionario con información del video
        """
        try:
            self._setup_managers()
            
            # Obtener información del video usando la nueva API
            video_fps = self.video.frame_rate
            duration_timecode = self.video.duration
            
            # Verificar que duration_timecode es un objeto FrameTimecode válido
            if hasattr(duration_timecode, 'get_frames') and hasattr(duration_timecode, 'get_seconds'):
                frame_count = duration_timecode.get_frames()
                duration = duration_timecode.get_seconds()
            else:
                # Fallback si no es un FrameTimecode válido
                logging.warning(f"Duration object type: {type(duration_timecode)}")
                frame_count = 0
                duration = 0.0
            
            info = {
                'filename': self.video_path.name,
                'path': str(self.video_path),
                'fps': video_fps,
                'frame_count': frame_count,
                'duration': duration,
                'duration_formatted': self._format_time(duration),
                'file_size': self.video_path.stat().st_size,
                'file_size_mb': round(self.video_path.stat().st_size / (1024*1024), 2)
            }
            
            return info
            
        except Exception as e:
            logging.error(f"Error obteniendo info del video: {e}")
            raise
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Formatea segundos a formato HH:MM:SS.
        
        Args:
            seconds: Tiempo en segundos
            
        Returns:
            Tiempo formateado como string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def export_scenes_csv(self, output_path: str) -> None:
        """
        Exporta las escenas detectadas a un archivo CSV.
        
        Args:
            output_path: Ruta del archivo CSV de salida
        """
        import pandas as pd
        
        if not self.scenes:
            raise ValueError("No hay escenas detectadas para exportar")
        
        # Preparar datos para CSV
        csv_data = []
        for scene in self.scenes:
            csv_data.append({
                'Scene_ID': scene['id'],
                'Start_Time': scene['start_timecode'],
                'End_Time': scene['end_timecode'],
                'Duration': f"{scene['duration']:.2f}s",
                'Start_Seconds': scene['start_time'],
                'End_Seconds': scene['end_time'],
                'Status': scene['status'],
                'Characters': ', '.join(scene['characters']),
                'Notes': scene['notes']
            })
        
        df = pd.DataFrame(csv_data)
        df.to_csv(output_path, index=False)
        logging.info(f"Escenas exportadas a: {output_path}")


def detect_scenes_streamlit(video_path: str, threshold: float = 30.0) -> List[Dict]:
    """
    Función wrapper para usar en Streamlit con manejo de progreso.
    
    Args:
        video_path: Ruta al archivo de video
        threshold: Umbral de detección
        
    Returns:
        Lista de escenas detectadas
    """
    try:
        print(f"[TERMINAL] 🔍 Iniciando análisis de: {video_path}")
        print(f"[TERMINAL] ⚙️ Umbral configurado: {threshold}")
        st.write(f"🔍 Iniciando análisis de: {video_path}")
        st.write(f"⚙️ Umbral configurado: {threshold}")
        
        # Crear detector
        print(f"[TERMINAL] Creando detector...")
        detector = SceneDetector(video_path, threshold)
        print(f"[TERMINAL] ✅ Detector creado exitosamente")
        st.write("✅ Detector creado exitosamente")
        
        # Mostrar información del video
        print(f"[TERMINAL] Obteniendo información del video...")
        with st.spinner("Obteniendo información del video..."):
            video_info = detector.get_video_info()
            print(f"[TERMINAL] ✅ Información del video obtenida: {video_info}")
            st.write(f"✅ Información del video obtenida: {video_info}")
            
        st.success(f"📹 Video: {video_info['filename']}")
        st.info(f"⏱️ Duración: {video_info['duration_formatted']} | 📊 FPS: {video_info['fps']:.2f} | 💾 Tamaño: {video_info['file_size_mb']} MB")
        
        # Crear barra de progreso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def progress_callback(message):
            print(f"[TERMINAL] 📊 Progreso: {message}")
            st.write(f"📊 Progreso: {message}")
            status_text.text(message)
            progress_bar.progress(50)  # Progreso genérico
        
        # Detectar escenas
        print(f"[TERMINAL] 🔍 Iniciando detección de escenas...")
        st.write("🔍 Iniciando detección de escenas...")
        with st.spinner("Detectando escenas..."):
            print(f"[TERMINAL] Llamando a detector.detect_scenes()...")
            scenes = detector.detect_scenes(progress_callback)
            print(f"[TERMINAL] detector.detect_scenes() retornó: {type(scenes)} con {len(scenes) if scenes else 0} elementos")
        
        print(f"[TERMINAL] ✅ Detección completada. Escenas encontradas: {len(scenes)}")
        st.write(f"✅ Detección completada. Escenas encontradas: {len(scenes)}")
        
        if scenes:
            print(f"[TERMINAL] 📋 Primeras 3 escenas detectadas:")
            st.write("📋 Primeras 3 escenas detectadas:")
            for i, scene in enumerate(scenes[:3]):
                print(f"[TERMINAL]   - Escena {i+1}: {scene}")
                st.write(f"  - Escena {i+1}: {scene}")
        else:
            print(f"[TERMINAL] ⚠️ No se detectaron escenas")
        
        progress_bar.progress(100)
        status_text.text(f"✅ Análisis completado: {len(scenes)} escenas detectadas")
        print(f"[TERMINAL] ✅ Análisis completado: {len(scenes)} escenas detectadas")
        
        print(f"[TERMINAL] 🔄 Retornando {len(scenes)} escenas")
        return scenes
        
    except Exception as e:
        print(f"[TERMINAL] ❌ ERROR en detección: {str(e)}")
        print(f"[TERMINAL] 🐛 Tipo de error: {type(e).__name__}")
        import traceback
        print(f"[TERMINAL] 📋 Stack trace:")
        print(traceback.format_exc())
        
        st.error(f"❌ Error en detección: {str(e)}")
        st.write(f"🐛 Detalles del error: {type(e).__name__}: {e}")
        st.code(traceback.format_exc())
        logging.error(f"Error en detect_scenes_streamlit: {e}")
        
        print(f"[TERMINAL] 🔄 Retornando lista vacía debido al error")
        return []


def validate_video_file(file_path: str) -> bool:
    """
    Valida si el archivo es un video soportado.
    
    Args:
        file_path: Ruta al archivo
        
    Returns:
        True si es válido, False en caso contrario
    """
    if not file_path:
        return False
        
    path = Path(file_path)
    if not path.exists():
        return False
    
    # Extensiones soportadas
    supported_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
    
    return path.suffix.lower() in supported_extensions


def get_sample_scenes() -> List[Dict]:
    """
    Genera escenas de ejemplo para testing.
    
    Returns:
        Lista de escenas de ejemplo
    """
    return [
        {
            'id': 'scene_001',
            'index': 0,
            'start_time': 0.0,
            'end_time': 45.2,
            'duration': 45.2,
            'start_frame': 0,
            'end_frame': 1130,
            'start_timecode': '00:00:00.000',
            'end_timecode': '00:00:45.200',
            'status': 'detected',
            'characters': [],
            'notes': '',
            'ai_analysis': None,
            'thumbnail_path': None
        },
        {
            'id': 'scene_002',
            'index': 1,
            'start_time': 45.2,
            'end_time': 92.8,
            'duration': 47.6,
            'start_frame': 1130,
            'end_frame': 2320,
            'start_timecode': '00:00:45.200',
            'end_timecode': '00:01:32.800',
            'status': 'detected',
            'characters': [],
            'notes': '',
            'ai_analysis': None,
            'thumbnail_path': None
        },
        {
            'id': 'scene_003',
            'index': 2,
            'start_time': 92.8,
            'end_time': 156.4,
            'duration': 63.6,
            'start_frame': 2320,
            'end_frame': 3910,
            'start_timecode': '00:01:32.800',
            'end_timecode': '00:02:36.400',
            'status': 'detected',
            'characters': [],
            'notes': '',
            'ai_analysis': None,
            'thumbnail_path': None
        }
    ]