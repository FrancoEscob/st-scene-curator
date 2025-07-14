Eres un desarrollador de software Full-Stack con experiencia senior en Python, Streamlit, y diseño de interfaces de usuario interactivas. Tu misión es construir una aplicación web completa y funcional llamada "ST Scene Curator" basada en un mockup de diseño y un prototipo de código que te serán proporcionados. La aplicación debe permitir a un usuario humano curar y anotar escenas de video detectadas automáticamente, transformando una segmentación técnica en una semántica y narrativa.
Concepto Central del Producto:
El flujo de trabajo principal de la aplicación es: Detectar -> Curar -> Anotar -> Exportar.
Detectar: Un video es analizado por PySceneDetect para generar una lista inicial de "micro-escenas" (planos técnicos).
Curar: El usuario edita esta lista directamente en la interfaz, agrupando (Group) planos cortos en escenas narrativas más largas, y dividiendo (Cut) planos largos en escenas más específicas.
Anotar: Para cada escena curada, el usuario añade metadatos ricos, como los personajes presentes y un resumen narrativo.
Exportar: El resultado final, una lista de escenas semánticamente curadas, se exporta como un archivo JSON.
Requisitos Funcionales Detallados (Basados en el Mockup):
Por favor, implementa la siguiente arquitectura y funcionalidades.

1. Estructura y Gestión de Estado:
   Layout Principal: La aplicación debe tener un layout de dos columnas: una columna principal a la izquierda (70% del ancho) y una columna secundaria a la derecha (30%).
   Gestión de Estado Centralizada: Utiliza st.session_state como única fuente de verdad. Las claves esenciales a gestionar son:
   st.session_state.scenes: Una lista de diccionarios, donde cada diccionario representa una escena. Esta es la lista que se cargará y modificará.
   st.session_state.selected_scene_id: String que almacena el ID de la escena actualmente seleccionada por el usuario. Su valor será None si no hay ninguna selección.
   st.session_state.video_path: La ruta al archivo de video cargado y analizado.
2. Columna Izquierda: Reproductor y Herramientas de Edición:
   Reproductor de Video (st.video):
   El reproductor de video debe estar en la parte superior.
   Sincronización: El video debe saltar automáticamente al timestamp de inicio (start_time) de la escena almacenada en st.session_state.selected_scene_id cada vez que esta cambie.
   Timeline Interactiva (Implementación con "Chips"):
   Debajo del video, renderiza la "Timeline". NO uses gráficos de Plotly. En su lugar, itera sobre st.session_state.scenes.
   Para cada escena en la lista, crea un st.button que actúe como un "chip". El texto del botón debe mostrar el id de la escena y su duration (ej: "Escena 3\n15s").
   Usa st.columns para disponer los botones en una fila horizontal. Esto permitirá el scroll horizontal si hay muchas escenas.
   Lógica de Selección: Al hacer clic en un botón/chip, actualiza st.session_state.selected_scene_id con el ID de esa escena.
   Feedback Visual de Selección: La escena actualmente seleccionada debe estar visualmente resaltada. El método más efectivo en Streamlit es deshabilitar el botón del chip seleccionado (disabled=True) y usar CSS para darle un estilo de "activo" (color de fondo diferente).
   Herramientas de Edición (Debajo de la Timeline):
   Group (Unir):
   Implementa un widget st.multiselect que muestre los IDs de todas las escenas actuales. El usuario seleccionará aquí las escenas a unir.
   Un botón "🔗 Group" ejecutará la lógica de fusión sobre los IDs seleccionados en el multiselect. La lógica debe:
   Identificar las escenas a fusionar.
   Calcular el start_time mínimo y el end_time máximo.
   Crear una nueva escena fusionada.
   Eliminar las escenas originales de st.session_state.scenes.
   Añadir la nueva escena a la lista.
   Ordenar la lista por start_time y llamar a st.rerun().
   Cut (Dividir):
   Esta herramienta solo debe mostrarse si una escena está seleccionada (st.session_state.selected_scene_id no es None).
   Proporciona un st.number_input para que el usuario especifique el timestamp exacto del corte.
   Un botón "✂️ Cut" ejecutará la lógica de división, que debe:
   Encontrar la escena a dividir.
   Validar que el timestamp de corte esté dentro de la duración de la escena.
   Crear dos nuevas escenas con los tiempos recalculados.
   Eliminar la escena original y añadir las dos nuevas.
   Ordenar la lista y llamar a st.rerun().
3. Columna Derecha: Panel de Anotación:
   Este panel debe ser dinámico y basarse en st.session_state.selected_scene_id.
   Estado por Defecto: Si no hay ninguna escena seleccionada, debe mostrar un mensaje como "Selecciona una escena para anotarla".
   Estado Activo (Escena Seleccionada):
   Muestra el ID de la escena que se está editando.
   Personajes (st.multiselect): Permite al usuario seleccionar múltiples personajes de una lista predefinida. La selección actual de la escena debe mostrarse por defecto.
   Contexto Narrativo (st.text_area): Un campo de texto grande para las notas. El contenido actual de las notas de la escena debe mostrarse por defecto.
   Guardado Automático: Cualquier cambio en estos widgets debe actualizar inmediatamente el diccionario de la escena correspondiente dentro de la lista st.session_state.scenes. No se necesita un botón de "Guardar".
4. Funcionalidad de Exportación:
   En la barra lateral o en un lugar prominente, añade un botón st.download_button llamado "Exportar Datos (JSON)".
   Al hacer clic, este botón debe convertir la lista st.session_state.scenes (con todas las curaciones y anotaciones) a una cadena de texto JSON y ofrecerla para su descarga.
   Contexto Adicional:
   Al final de este prompt, te proporcionaré un código de ejemplo que ya he desarrollado. Este código es un prototipo básico de la visión. Úsalo como inspiración y punto de partida para la estructura y la lógica, pero siéntete libre de mejorarlo para construir la aplicación final y completamente funcional que he descrito. El objetivo es pasar de ese prototipo a una implementación robusta del mockup.
