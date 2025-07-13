# ST Scene Curat-o-matic - TODO & Progress Tracker

## 📋 Estado General del Proyecto
- **Proyecto:** Herramienta de Curación de Escenas de Stranger Things
- **Framework:** Streamlit + Python
- **Fecha de Inicio:** [Fecha actual]
- **Estado Actual:** 🟡 En Desarrollo

---

## 🎯 ETAPA 1: Estructura Base y UI Básica
**Objetivo:** Crear la base del proyecto con interfaz básica funcional

### Tareas:
- [x] **1.1** Crear estructura de carpetas del proyecto
  - [x] Carpeta `components/`
  - [x] Carpeta `utils/`
  - [x] Carpeta `assets/`
  - [x] Carpeta `data/`

- [x] **1.2** Crear archivo principal `app.py`
  - [x] Configuración básica de Streamlit
  - [x] Sidebar con título "Configuración del Episodio"
  - [x] Layout de dos columnas principales
  - [x] Placeholders para funcionalidades futuras

- [x] **1.3** Crear `requirements.txt`
  - [x] Streamlit
  - [x] PySceneDetect
  - [x] MoviePy
  - [x] Pandas
  - [x] Google-generativeai
  - [x] Otras dependencias necesarias

- [x] **1.4** Crear `data/characters.json`
  - [x] Lista completa de personajes de Stranger Things
  - [x] Estructura JSON organizada por temporadas

- [x] **1.5** Crear archivos `__init__.py` para módulos

**Estado ETAPA 1:** ✅ Completado

---

## 🎬 ETAPA 2: Detección de Escenas
**Objetivo:** Implementar la funcionalidad de análisis automático de videos

### Tareas:
- [x] **2.1** Crear `utils/scene_detection.py`
  - [x] Wrapper para PySceneDetect
  - [x] Función de análisis con threshold configurable
  - [x] Manejo de errores y validaciones

- [x] **2.2** Integrar carga de archivos en `app.py`
  - [x] `st.file_uploader` para videos
  - [x] Validación de formatos de video
  - [x] Guardado temporal de archivos

- [x] **2.3** Implementar slider de threshold
  - [x] `st.slider` con rango apropiado
  - [x] Valor por defecto: 27
  - [x] Tooltip explicativo

- [x] **2.4** Botón "Analizar y Cargar Episodio"
  - [x] Ejecutar detección de escenas
  - [x] Guardar resultados en `st.session_state`
  - [x] Indicador de progreso

- [x] **2.5** Vista básica de lista de escenas
  - [x] Mostrar timestamps detectados
  - [x] Duración de cada escena
  - [x] IDs únicos para cada escena

- [x] **2.6** Debugging y corrección de bugs críticos
  - [x] Corrección del bug de session_state que reseteaba analysis_completed
  - [x] Implementación de logging detallado para debugging
  - [x] Validación de persistencia de estado entre re-renders
  - [x] Interfaz completamente funcional mostrando resultados

**Estado ETAPA 2:** ✅ Completado (Diciembre 2024)

---

## ⏱️ ETAPA 3: Timeline Interactivo Sincronizado
**Objetivo:** Crear un timeline horizontal estilo editor de video con sincronización en tiempo real

### 🎯 Funcionalidades Clave:
- **Timeline Horizontal:** Bloques de escenas proporcionales a su duración
- **Sincronización Video:** Resaltado automático de escena actual durante reproducción
- **Zoom Dinámico:** Acercar/alejar para edición fina o vista general
- **Navegación:** Click en escena para saltar en el video
- **Indicador de Progreso:** Línea vertical que sigue el playhead del video

### Tareas:
- [ ] **3.1** Crear `components/video_timeline.py`
  - [ ] Componente Streamlit personalizado con st.components.v1.html
  - [ ] Interfaz Python para pasar datos de escenas
  - [ ] Comunicación bidireccional JavaScript ↔ Python
  - [ ] Manejo de eventos de click y selección

- [ ] **3.2** Crear `assets/timeline.html`
  - [ ] Estructura HTML del timeline horizontal
  - [ ] Contenedor principal con scroll horizontal
  - [ ] Bloques de escenas con proporciones reales
  - [ ] Línea de progreso (playhead) sincronizada
  - [ ] Controles de zoom (+/-) y reset
  - [ ] Indicadores de tiempo (marcas cada 30s/1min)

- [ ] **3.3** Crear `assets/timeline.css`
  - [ ] Estilos para bloques de escenas (colores, bordes, sombras)
  - [ ] Efectos de hover y selección activa
  - [ ] Animaciones suaves para transiciones
  - [ ] Resaltado de escena actual (borde brillante + color)
  - [ ] Responsive design para diferentes tamaños
  - [ ] Estilos para controles de zoom

- [ ] **3.4** Crear `assets/timeline.js`
  - [ ] Renderizado dinámico de bloques basado en datos de escenas
  - [ ] Sistema de zoom (escala temporal ajustable)
  - [ ] Sincronización con tiempo del video (actualización del playhead)
  - [ ] Detección de escena activa basada en tiempo actual
  - [ ] Eventos de click para navegación en video
  - [ ] Scroll automático para seguir playhead
  - [ ] Comunicación con Streamlit via postMessage

- [ ] **3.5** Integrar reproductor de video en `app.py`
  - [ ] st.video() con controles personalizados
  - [ ] Captura de eventos de tiempo (currentTime)
  - [ ] Función de salto a timestamp específico
  - [ ] Sincronización bidireccional video ↔ timeline

- [ ] **3.6** Integrar timeline en `app.py`
  - [ ] Mostrar timeline debajo del reproductor
  - [ ] Pasar datos de escenas al componente JavaScript
  - [ ] Recibir eventos de selección desde timeline
  - [ ] Actualizar session_state con escena seleccionada
  - [ ] Manejo de zoom y navegación

- [ ] **3.7** Funcionalidades avanzadas
  - [ ] Zoom con rueda del mouse
  - [ ] Arrastrar timeline para navegación rápida
  - [ ] Tooltips con información de escena al hover
  - [ ] Marcadores de tiempo cada 30 segundos
  - [ ] Mini-mapa para navegación en videos largos

**Estado ETAPA 3:** ⏳ Pendiente - PRÓXIMA PRIORIDAD

---

## ✂️ ETAPA 4: Edición de Escenas
**Objetivo:** Implementar funcionalidades de trimming, merge y split

### Tareas:
- [ ] **4.1** Funcionalidad de Trimming
  - [ ] Detección de bordes de bloques
  - [ ] Cursor de redimensionamiento
  - [ ] Arrastrar para ajustar inicio/fin
  - [ ] Actualización en tiempo real

- [ ] **4.2** Funcionalidad de Merge (Fusión)
  - [ ] Selección múltiple (Ctrl+Click)
  - [ ] Botón "Juntar Escenas"
  - [ ] Combinación de bloques adyacentes
  - [ ] Validaciones de continuidad

- [ ] **4.3** Funcionalidad de Split (División)
  - [ ] Sincronización con reproductor de video
  - [ ] Botón "Dividir Escena en el Cabezal"
  - [ ] División en posición del playhead
  - [ ] Actualización de IDs

- [ ] **4.4** Integrar reproductor de video
  - [ ] `st.video` con controles
  - [ ] Sincronización con timeline
  - [ ] Salto a escena seleccionada

- [ ] **4.5** Validaciones y feedback
  - [ ] Prevenir operaciones inválidas
  - [ ] Mensajes de confirmación
  - [ ] Undo/Redo básico

**Estado ETAPA 4:** ⏳ Pendiente

---

## 📝 ETAPA 5: Panel de Anotación
**Objetivo:** Crear el panel contextual para anotar escenas seleccionadas

### Tareas:
- [ ] **5.1** Crear `components/annotation_panel.py`
  - [ ] Panel contextual reactivo
  - [ ] Información de escena seleccionada
  - [ ] Formularios de anotación

- [ ] **5.2** Vista previa de fotogramas
  - [ ] Extracción de primer/último frame
  - [ ] `st.image()` con thumbnails
  - [ ] Carga optimizada

- [ ] **5.3** Selector de personajes
  - [ ] `st.multiselect` con personajes de ST
  - [ ] Carga desde `characters.json`
  - [ ] Búsqueda y filtrado

- [ ] **5.4** Área de notas narrativas
  - [ ] `st.text_area` expandible
  - [ ] Placeholder con ejemplos
  - [ ] Contador de caracteres

- [ ] **5.5** Sistema de estados
  - [ ] Indicadores visuales de estado
  - [ ] "Sin procesar", "En cola", "Procesado"
  - [ ] Iconos y colores distintivos

- [ ] **5.6** Botón de procesamiento
  - [ ] Botón "🚀 Enviar a Procesamiento IA"
  - [ ] Validaciones antes del envío
  - [ ] Feedback visual

**Estado ETAPA 5:** ⏳ Pendiente

---

## 🤖 ETAPA 6: Pipeline de IA
**Objetivo:** Implementar el procesamiento completo con APIs de IA

### Tareas:
- [ ] **6.1** Crear `utils/video_processing.py`
  - [ ] Extracción de clips con MoviePy
  - [ ] Optimización de calidad/tamaño
  - [ ] Manejo de formatos

- [ ] **6.2** Crear `utils/ai_pipeline.py`
  - [ ] Integración con Google Gemini
  - [ ] Generación de prompts enriquecidos
  - [ ] Manejo de respuestas de IA

- [ ] **6.3** Función `process_scene()`
  - [ ] Pipeline completo de procesamiento
  - [ ] Extracción → Prompt → IA → Graphiti
  - [ ] Manejo de errores robusto

- [ ] **6.4** Integración con Graphiti
  - [ ] API calls para knowledge graph
  - [ ] Formato de datos apropiado
  - [ ] Confirmación de envío

- [ ] **6.5** Sistema de cola y batch processing
  - [ ] Procesamiento en background
  - [ ] Progress tracking
  - [ ] Logs de actividad

**Estado ETAPA 6:** ⏳ Pendiente

---

## 🔧 TAREAS ADICIONALES

### Optimización y Pulido:
- [ ] **OPT.1** Manejo de errores robusto
- [ ] **OPT.2** Optimización de performance
- [ ] **OPT.3** Documentación de código
- [ ] **OPT.4** Testing básico
- [ ] **OPT.5** Configuración de logging

### Features Opcionales:
- [ ] **EXT.1** Exportar/Importar configuraciones
- [ ] **EXT.2** Shortcuts de teclado
- [ ] **EXT.3** Temas visuales
- [ ] **EXT.4** Historial de cambios
- [ ] **EXT.5** Estadísticas del proyecto

---

## 📊 Resumen de Progreso

| Etapa | Descripción | Estado | Progreso |
|-------|-------------|--------|----------|
| 1 | Estructura Base y UI Básica | ✅ Completado | 100% |
| 2 | Detección de Escenas + Debugging | ✅ Completado | 100% |
| 3 | Timeline Interactivo Sincronizado | ⏳ Próxima Prioridad | 0% |
| 4 | Edición de Escenas | ⏳ Pendiente | 0% |
| 5 | Panel de Anotación | ⏳ Pendiente | 0% |
| 6 | Pipeline de IA | ⏳ Pendiente | 0% |

**Progreso Total:** 33.3% (2/6 etapas completadas)
**Estado Actual:** ✅ Detección de escenas funcionando perfectamente
**Próximo Objetivo:** 🎯 Timeline interactivo estilo editor de video

---

## 📝 Notas y Decisiones

### Decisiones Técnicas:
- **Framework UI:** Streamlit (confirmado)
- **Detección de Escenas:** PySceneDetect (confirmado)
- **Procesamiento Video:** MoviePy (confirmado)
- **IA:** Google Gemini (confirmado)
- **Gestión de Paquetes:** uv (según instrucciones)

### Próximos Pasos:
1. ✅ Crear este archivo TODO.md
2. ✅ Implementar estructura base del proyecto (ETAPA 1)
3. ✅ Implementar detección de escenas (ETAPA 2)
4. ✅ Debugging y corrección de bugs críticos
5. 🎯 **PRÓXIMO:** Implementar timeline interactivo sincronizado (ETAPA 3)

---

## 🎯 Objetivo Actual
**ETAPA 2 - ✅ COMPLETADA CON ÉXITO**
- ✅ Detección de escenas funcionando perfectamente
- ✅ Interfaz mostrando resultados correctamente
- ✅ Bugs críticos de session_state resueltos

**Próximo: ETAPA 3 - Timeline Interactivo Sincronizado**
- 🎯 Timeline horizontal estilo editor de video
- 🎯 Sincronización en tiempo real con reproductor
- 🎯 Zoom dinámico para edición fina
- 🎯 Navegación por click en escenas

*Última actualización: Diciembre 2024*