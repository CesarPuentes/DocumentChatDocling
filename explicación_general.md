¡Hola! Bienvenido a clase 👨‍🏫.

Hoy vamos a diseccionar el proyecto ChatWithDocumentsDocling. Como tu profesor, mi objetivo no es que memorices cada línea de código, sino que entiendas la arquitectura y las decisiones de diseño que hacen que este sistema sea especial en comparación con un "Chat con PDF" genérico.

Vamos a dividir el análisis en tres grandes bloques lógicos:

La Ingesta (El Desafío Visual): Cómo leemos realmente un documento.
El Cerebro (RAG Híbrido): Cómo encontramos la aguja en el pajar.
La Orquestación (Agentes): Cómo pensamos la respuesta.
Parte 1: La Ingesta - "No leas, mira"
Empecemos por el principio. Cuando tú abres un PDF, ves títulos, columnas, tablas y gráficos. Pero un ordenador "clásico" solo ve una sopa de letras.

El Problema Teórico: Si usas herramientas tradicionales (como PyPDF2), el ordenador lee el archivo línea por línea de izquierda a derecha.

¿Qué pasa con una tabla? Se mezcla todo.
¿Qué pasa con una nota al pie? Se mete en medio de una frase.
¿Qué pasa con un título? Se convierte en una frase más.
Esto destruye el contexto estructural. Sin estructura, el LLM (la IA) no entiende nada.

La Solución del Proyecto (Enfoque Moderno): Este proyecto utiliza una filosofía "Layout-Aware" (consciente del diseño) mediante una librería llamada Docling. En lugar de solo "leer texto", la herramienta "ve" el documento (casi como si usara visión por computador) para entender qué es una tabla, qué es un título y qué es un párrafo.

Vemos el Código Clave 🧐
El archivo mágico aquí es document_processor/file_handler.py.

Mira esta función (simplificada para la clase):

python
# En document_processor/file_handler.py
def _process_file(self, file) -> List:
    # 1. Convertimos el documento visual a Markdown Estructurado
    converter = DocumentConverter() 
    markdown = converter.convert(file.name).document.export_to_markdown()
    
    # 2. Dividimos el texto respetando esa estructura
    splitter = MarkdownHeaderTextSplitter(self.headers)
    return splitter.split_text(markdown)
¿Por qué esto es brillante?

DocumentConverter(): Transforma el PDF complejo en Markdown. El Markdown es genial porque conserva la jerarquía (# Título, | Tabla |) de una forma que los LLMs entienden perfectamente.
MarkdownHeaderTextSplitter: En lugar de cortar el texto cada 1000 caracteres (lo que podría cortar una frase a la mitad), cortamos el documento por Secciones (Títulos).
En resumen: En esta fase, no hemos perdido información. Hemos traducido un documento visual a un formato estructurado que la IA puede "digerir".

Dime "continua" cuando hayas asimilado esta primera parte y pasaremos a ver cómo almacenamos y buscamos esta información (El Cerebro).


-----------------------

🧠 Guía Detallada del Flujo de Ejecución: ChatWithDocumentsDocling
Esta guía disecciona el proyecto archivo por archivo, siguiendo el viaje de una pregunta desde que el usuario la escribe hasta que recibe una respuesta verificada.

🏗️ 1. La Estructura General
El proyecto sigue una arquitectura moderna de Micro-Agentes. En lugar de un solo script gigante, cada carpeta tiene un rol específico:

app.py
: La Cara (Interfaz de Usuario).
document_processor/: El Ojo (Lectura y Parseo).
retriever/
: La Memoria (Búsqueda Híbrida).
agents/: El Cerebro (Lógica, Razonamiento y Verificación).
config/: Las Reglas (Configuración).
🔄 2. El Flujo Paso a Paso (Trace)
Paso 1: El Inicio (
app.py
)
Todo comienza aquí. Es el punto de entrada.

Rol: Levanta la interfaz web con Gradio.
Lo que hace:
Crea la variable session_state para guardar los documentos subidos en memoria.
Define la interfaz visual (cajas de texto, botones).
Cuando el usuario pulsa "Submit", llama a la función 
process_question
.
Clave: Orquesta todo. Llama primero al processor (para leer), luego al retriever_builder (para indexar) y finalmente al 
workflow
 (para pensar).
Paso 2: La Ingesta Visual (
document_processor/file_handler.py
)
Antes de poder contestar, hay que leer.

Rol: Convertir PDFs difíciles (tablas, columnas) en texto estructurado limpio.
La Magia (Docling): Usa DocumentConverter para "ver" el documento.
La Clave (Chunking): No corta por caracteres al azar. Usa MarkdownHeaderTextSplitter para cortar por Secciones (Títulos). Esto mantiene el contexto unido.
Resultado: Devuelve una lista de chunks (fragmentos de texto) que entienden a qué sección pertenecen.
Paso 3: La Indexación Híbrida (
retriever/builder.py
)
Ahora que tenemos texto, ¿cómo lo buscamos rápido?

Rol: Construir el motor de búsqueda.
Estrategia Dual (Hybrid Search):
Vector Store (Chroma & Watsonx Embeddings): Convierte el texto en números. Encuentra conceptos relacionados (Semántica).
BM25 (Palabras Clave): Busca coincidencias exactas. Importante para nombres, fechas o códigos específicos.
Resultado: Un objeto ensemble_retriever que combina lo mejor de ambos mundos.
Paso 4: El Cerebro de Agentes (
agents/workflow.py
)
Aquí es donde este proyecto brilla. No es una simple llamada a "preguntar". Es un Grafo de Decisiones (usando LangGraph).

Rol: El Director de Orquesta de los agentes.
El Flujo Lógico:
Inicio -> Llama a Relevance Checker.
Decisión: ¿Es relevante?
No -> Fin (Responde: "No tengo info").
Sí -> Pasa a Research Agent.
Investigación -> Genera un borrador de respuesta.
Verificación -> Pasa a Verification Agent.
Decisión Final: ¿Está verificada?
Sí -> Fin (Entrega respuesta).
No (Parcial) -> Podría volver a investigar (Loop) o avisar del error.
Paso 5: Los Especialistas (La Carpeta agents/)
A. El Portero (
agents/relevance_checker.py
)
Modelo: Granite 3.0 8B (Rápido y ligero).
Misión: Mirar los documentos recuperados y decir: ¿Aquí hay información para contestar esto?
Por qué existe: Para evitar alucinaciones. Si no hay info, corta el flujo antes de que el modelo grande empiece a inventar.
B. El Investigador (
agents/research_agent.py
)
Modelo: Llama 3.2 90B Vision (Potente y creativo).
Misión: Leer los documentos seleccionados y redactar una respuesta completa y bien estructurada.
Detalle: Usa un prompt diseñado para ser "preciso y factual".
C. El Auditor (
agents/verification_agent.py
)
Modelo: Granite 3.0 Guardian o similar (Especializado en seguir instrucciones estrictas).
Misión: Comparar la Respuesta del Investigador contra los Documentos Originales.
Salida: Un "Informe de Verificación" (Verification Report) que dice:
✅ Soportado: Sí/No
❌ Alucinaciones encontradas: [Lista]
⚠️ Contradicciones: [Lista]
Paso 6: Los Cimientos (config/ y 
requirements.txt
)
Aunque no "ejecutan" lógica, sin ellos nada funciona.

config/settings.py
: El Centro de Control. Define:
Qué modelo de IA usar (Llama 3, Granite).
Las llaves de API.
Umbrales de similitud para la búsqueda.
requirements.txt
: La lista de ingredientes.
docling: Para leer PDFs.
langgraph: Para la orquestación.
chromadb: Base de datos vectorial.
gradio: Para la web.
Paso 7: Los Datos de Prueba (examples/)
Contiene PDFs reales para probar el sistema sin tener que buscar uno tuyo.

Ejemplo: Google 2024 Environmental Report. Un reporte complejo ideal para probar si el sistema entiende tablas y datos numéricos.
📝 Resumen del Valor
Este sistema no solo "chatea". Lee con ojos de visión artificial, busca con doble criterio, y piensa en tres pasos (filtro, redacción, auditoría) para garantizar que lo que te dice es cierto.