# Consulta de Exoplanetas de la NASA 🌠

## Descripción

**Justificación del proyecto**

En la era actual de la astronomía, el número de exoplanetas descubiertos crece exponencialmente, superando los 5,000 confirmados. El Archivo de Exoplanetas de la NASA (NASA Exoplanet Archive) es la fuente más completa y confiable de datos sobre estos mundos lejanos, pero su acceso y consulta requieren conocimientos técnicos que limitan su uso por parte de estudiantes, divulgadores e investigadores no especializados en programación.

Este proyecto nace con el propósito de **democratizar el acceso a los datos astronómicos**, ofreciendo una herramienta de escritorio intuitiva y visualmente atractiva que permita:

- **Consultar** el archivo de exoplanetas sin necesidad de escribir código.
- **Filtrar** por criterios clave (año, método, estrella, instalación).
- **Visualizar** resultados de forma clara en una tabla interactiva.
- **Explorar** información detallada mediante enlaces directos a la NASA.
- **Ordenar** datos para facilitar el análisis comparativo.

De esta manera, la aplicación se convierte en un puente entre la ciencia de datos y la curiosidad humana, fomentando el aprendizaje y la divulgación científica en un área que despierta gran interés público.

## User Stories

- Como **investigador astronómico**, quiero **filtrar exoplanetas por año de descubrimiento** para **analizar la evolución de los hallazgos en el tiempo**.
- Como **estudiante de astronomía**, quiero **buscar por método de descubrimiento** para **estudiar las diferentes técnicas de detección de exoplanetas**.
- Como **divulgador científico**, quiero **consultar por estrella anfitriona** para **preparar material educativo sobre sistemas planetarios específicos**.
- Como **entusiasta de la astronomía**, quiero **ordenar los resultados por cualquier columna** para **explorar los datos desde diferentes perspectivas**.
- Como **usuario general**, quiero **hacer clic en el nombre de la estrella** para **acceder directamente a la página de la NASA con información detallada del planeta**.
- Como **investigador**, quiero **recibir un mensaje de error si intento buscar sin seleccionar criterios** para **saber que debo especificar al menos un filtro**.

## Metodología

**Kanban**

El proyecto se desarrolla bajo un enfoque **Kanban**, una metodología ágil que permite una entrega continua y rápida, ideal para proyectos con plazos ajustados. A diferencia de Scrum, Kanban no utiliza sprints fijos, lo que permite priorizar y ejecutar tareas de manera secuencial según su urgencia e importancia.

**Priorización de tareas (por orden de ejecución):**

🔴 **URGENTES (Mínimo Viable Producto):**
1. Descargar y cargar el CSV de la NASA
2. Panel de consulta con menús desplegables
3. Botones Buscar y Limpiar
4. Mostrar resultados en formato tabular
5. Validación de búsqueda vacía

🟡 **IMPORTANTES (si el tiempo lo permite):**
6. Ordenamiento con flechas ascendentes/descendentes
7. Enlaces a la página oficial de la NASA

🟢 **EXTRAS (mejoras adicionales):**
8. Mejorar estilos visuales
9. Mensajes de estado en tiempo real

## Tecnologías utilizadas

- **Python 3.8+** - Lenguaje de programación principal
- **Pandas** - Procesamiento y carga eficiente de datos CSV
- **NumPy** - Operaciones numéricas optimizadas
- **Tkinter** - Interfaz gráfica de usuario (incluida en Python)
- **Pytest** - Pruebas unitarias
- **Pillow** - Procesamiento de imágenes

## Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/Javiersan237/Consulta-de-Exoplanetas-de-la-NASA.git
cd Consulta-de-Exoplanetas-de-la-NASA