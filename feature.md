Prompt para la IA de Programación
Rol y Objetivo:
Eres un desarrollador experto en Python, especializado en la creación de aplicaciones interactivas con Streamlit y visualización de datos con Plotly. Tu tarea es mejorar una aplicación Streamlit existente, st-scene-curator, implementando una funcionalidad de edición de escenas de video mediante una línea de tiempo interactiva. El objetivo principal es permitir a los usuarios fusionar múltiples escenas detectadas por PySceneDetect en una sola escena semántica.
Contexto del Proyecto:
El repositorio de GitHub https://github.com/FrancoEscob/st-scene-curator contiene una aplicación Streamlit que ya utiliza PySceneDetect para detectar cortes de escena en un archivo de video. El resultado de esta detección es una lista de muchos "micro-planos" o "shots". La aplicación actual carece de una interfaz que permita al usuario editar o curar esta lista.
El Desafío Técnico a Resolver:
Streamlit no soporta de forma nativa componentes de UI complejos como una línea de tiempo de edición de video tradicional. Por lo tanto, nuestra estrategia será crear una "timeline virtual" utilizando un diagrama de Gantt de Plotly. Haremos este gráfico interactivo para que el usuario pueda seleccionar planos directamente sobre él y luego aplicar acciones de edición mediante botones de Streamlit.
Requisitos Detallados de Implementación:
Por favor, implementa los siguientes cambios y funcionalidades en el código base del repositorio.

1. Gestión de Dependencias:
   Asegúrate de que el archivo requirements.txt incluya las siguientes librerías:
   Generated code
   streamlit
   pandas
   plotly
   streamlit-plotly-events
   scenedetect[opencv]
   Use code with caution.
2. Gestión del Estado de la Aplicación:
   Toda la lógica de edición debe operar sobre una lista de escenas almacenada en st.session_state. Asegúrate de que, tras la detección inicial de escenas con PySceneDetect, la lista resultante se guarde en st.session_state['scenes']. Esto es crucial para que los cambios persistan entre las interacciones del usuario.
3. Creación de la Timeline Interactiva (Componente Principal):
   Crea una función (por ejemplo, display_interactive_timeline) que tome la lista de escenas de st.session_state['scenes'].
   Dentro de esta función, convierte la lista de escenas en un DataFrame de Pandas, preparándolo para un diagrama de Gantt de Plotly. Cada fila debe representar una escena. Las columnas necesarias son: Scene ID, Start (timestamp de inicio), Finish (timestamp de fin) y Duration (s).
   Importante: Plotly px.timeline requiere datos de fecha/hora. Convierte los timestamps en segundos a objetos datetime. Puedes usar una fecha base arbitraria (ej: datetime(2024, 1, 1)) y añadir los segundos usando timedelta.
   Utiliza plotly.express.timeline para crear el gráfico. Configúralo con las siguientes características:
   Ejes: x_start="Start", x_end="Finish", y="Scene ID".
   Interactividad: Muestra la duración en segundos al pasar el mouse sobre una barra (hover_data).
   Estética: Invierte el eje Y (yaxis_autorange="reversed") para que la primera escena aparezca arriba. Formatea el eje X para mostrar el tiempo en formato Minuto:Segundo (xaxis=dict(tickformat="%M:%S")). Oculta las etiquetas del eje Y para una apariencia más limpia (yaxis=dict(showticklabels=False)).
   Utiliza la librería streamlit-plotly-events para mostrar el gráfico y capturar las selecciones del usuario. El componente debe configurarse para capturar eventos de selección de rango (caja o lazo).
   Generated python

# Ejemplo de cómo usar el componente:

from streamlit_plotly_events import plotly_events

selected_points = plotly_events(
fig, # Tu figura de Plotly
select_event=True,
key="scene_selector_timeline" # Usa una clave única y descriptiva
)
Use code with caution.
Python
Esta función debe devolver los selected_points capturados. 4. Implementación de la Lógica de Fusión ("Merge"):
Crea un botón llamado "🔗 Unir Escenas Seleccionadas".
La lógica de este botón debe ejecutarse solo si selected_points contiene más de un punto.
Proceso de Fusión:
Extrae los Scene ID de los selected_points.
Obtén los diccionarios de escena completos de st.session_state['scenes'] que corresponden a esos IDs.
Valida que las escenas seleccionadas sean contiguas en el tiempo (opcional pero recomendado para una mejor UX). Si no lo son, muestra un st.warning.
Determina el start_time mínimo y el end_time máximo de todas las escenas seleccionadas.
Crea un nuevo diccionario de escena para la escena fusionada. Asígnale un ID único (ej: merged_scene_1), y los start_time y end_time calculados.
Modifica st.session_state['scenes']:
Elimina todos los diccionarios de escena originales que fueron seleccionados.
Añade el nuevo diccionario de la escena fusionada.
Crucial: Después de modificar la lista, ordénala de nuevo por start_time para mantener la consistencia.
Crucial: Al final de la lógica del botón, llama a st.rerun() para forzar un refresco completo de la aplicación y volver a renderizar la timeline con los cambios. 5. Interfaz de Usuario y Experiencia (UX):
Cuando el usuario seleccione escenas en el gráfico, muestra un mensaje informativo debajo, como st.info(f"Escenas seleccionadas: {lista_de_ids}").
El botón "Unir" debe estar deshabilitado o mostrar un help si no hay suficientes escenas seleccionadas.
Proporciona feedback al usuario. Después de una fusión exitosa, muestra un st.success("¡Escenas unidas correctamente!") justo antes de llamar a st.rerun().
Resumen del Flujo de Usuario a Implementar:
El usuario carga un video y se ejecuta PySceneDetect (funcionalidad existente).
La lista de planos se guarda en st.session_state['scenes'].
La aplicación muestra la timeline interactiva (el Gantt de Plotly).
El usuario hace clic y arrastra para seleccionar varias barras (planos) en el gráfico.
La aplicación muestra qué escenas ha seleccionado.
El usuario hace clic en el botón "Unir Escenas Seleccionadas".
La lógica de fusión se ejecuta, actualiza st.session_state['scenes'], y la aplicación se refresca.
El usuario ve la timeline actualizada, ahora con una sola barra más grande donde antes había varias pequeñas.
Por favor, asegúrate de que el código sea limpio, bien comentado (especialmente la lógica de fusión) y se integre de forma coherente con la estructura existente del proyecto.
