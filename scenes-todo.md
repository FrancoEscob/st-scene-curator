# ST Scene Curator - Plan de Implementación por Etapas

## 🎯 Objetivo
Transformar el `app.py` actual para que coincida exactamente con el mockup proporcionado, implementando una timeline de "chips" y un panel de anotación completo.

## 📋 TO-DO List por Etapas

### ✅ ETAPA 0: Análisis y Planificación
- [x] Analizar archivos existentes (Proyect.md, escenes.md, app-demo.py, app.py)
- [x] Identificar funcionalidades a mantener vs eliminar
- [x] Crear plan de implementación por etapas

### ✅ ETAPA 1: Limpieza del Código Actual - COMPLETADA
- [x] **1.1** Eliminar imports relacionados con Plotly:
  - `from streamlit_plotly_events import plotly_events`
  - `import plotly.express as px`
  - `from datetime import datetime, timedelta`
- [x] **1.2** Eliminar función `display_interactive_timeline(scenes)`
- [x] **1.3** Eliminar función `handle_scene_merging(selected_points, scenes)`
- [x] **1.4** Cambiar `st.session_state.selected_scene` por `st.session_state.selected_scene_id`
- [x] **1.5** Actualizar función `initialize_session_state()` para usar `selected_scene_id`
- [x] **1.6** Limpiar la función `main()` eliminando referencias a timeline antigua

### 🎨 ETAPA 2: Implementar Nueva Timeline de Chips
- [ ] **2.1** Crear función `render_timeline_chips(scenes)` basada en app-demo.py
- [ ] **2.2** Agregar CSS personalizado para styling de chips (botones)
- [ ] **2.3** Implementar lógica de selección con `st.columns` y `st.button`
- [ ] **2.4** Agregar feedback visual para chip seleccionado (disabled + CSS)
- [ ] **2.5** Implementar sincronización automática del video con escena seleccionada

### 🛠️ ETAPA 3: Herramientas de Edición (Group & Cut)
- [ ] **3.1** Crear función `render_editing_tools()`
- [ ] **3.2** Implementar herramienta "Group" (🔗):
  - `st.multiselect` para seleccionar escenas a unir
  - Botón "🔗 Group" con lógica de fusión
  - Validación de mínimo 2 escenas seleccionadas
- [ ] **3.3** Implementar herramienta "Cut" (✂️):
  - Solo mostrar cuando hay escena seleccionada
  - `st.number_input` para timestamp de corte
  - Botón "✂️ Cut" con lógica de división
  - Validación de timestamp dentro del rango de la escena

### 📝 ETAPA 4: Panel de Anotación Completo
- [ ] **4.1** Crear función `render_annotation_panel()` completa
- [ ] **4.2** Implementar estado dinámico basado en `selected_scene_id`
- [ ] **4.3** Agregar mensaje por defecto cuando no hay escena seleccionada
- [ ] **4.4** Implementar selector de personajes:
  - `st.multiselect` con lista de personajes de ST
  - Cargar desde `data/characters.json`
  - Guardado automático en `st.session_state.scenes`
- [ ] **4.5** Implementar área de notas narrativas:
  - `st.text_area` grande para contexto semántico
  - Guardado automático en `st.session_state.scenes`
- [ ] **4.6** Mostrar información de la escena (ID, duración, timestamps)

### 📤 ETAPA 5: Funcionalidad de Exportación
- [ ] **5.1** Agregar botón de exportación en sidebar
- [ ] **5.2** Implementar `st.download_button` para exportar JSON
- [ ] **5.3** Crear función para convertir `st.session_state.scenes` a JSON
- [ ] **5.4** Agregar validación y formato del archivo exportado

### 🎨 ETAPA 6: Refinamiento Visual y UX
- [ ] **6.1** Ajustar layout para coincidir exactamente con mockup (70%-30%)
- [ ] **6.2** Mejorar CSS para que los chips se vean como en el mockup
- [ ] **6.3** Agregar colores y estilos consistentes
- [ ] **6.4** Optimizar responsive design
- [ ] **6.5** Agregar iconos y elementos visuales del mockup

### 🧪 ETAPA 7: Testing y Validación
- [ ] **7.1** Probar flujo completo: Cargar video → Analizar → Curar → Anotar → Exportar
- [ ] **7.2** Validar sincronización de video con selección de escenas
- [ ] **7.3** Probar herramientas de edición (Group y Cut)
- [ ] **7.4** Verificar guardado automático de anotaciones
- [ ] **7.5** Probar exportación de datos

## 📋 Notas de Implementación

### Funcionalidades a Mantener del app.py Actual:
- ✅ Toda la lógica de PySceneDetect (`detect_scenes_streamlit`)
- ✅ Carga y validación de archivos de video
- ✅ Gestión de `st.session_state` para persistencia
- ✅ Configuración de sidebar con threshold y análisis
- ✅ Función `load_characters_data()` para personajes
- ✅ Logging y manejo de errores

### Funcionalidades a Eliminar:
- ❌ Timeline de Plotly (`display_interactive_timeline`)
- ❌ Lógica de fusión antigua (`handle_scene_merging`)
- ❌ Imports de Plotly y streamlit_plotly_events
- ❌ Panel de anotación placeholder ("se implementará en ETAPA 2")

### Funcionalidades Nuevas a Implementar:
- 🆕 Timeline de chips con `st.columns` y `st.button`
- 🆕 Herramientas de edición visual (Group/Cut)
- 🆕 Panel de anotación completo y funcional
- 🆕 Exportación de datos curados
- 🆕 Sincronización automática video-escena

## 🚀 Próximo Paso
**ETAPA 2: Implementar Nueva Timeline de Chips** - Crear timeline con botones de escenas basada en app-demo.py y mockup.

---
*Creado: $(date)*
*Proyecto: ST Scene Curat-o-matic*