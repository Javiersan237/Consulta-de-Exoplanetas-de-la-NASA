# Consulta de Exoplanetas de la NASA 🌠

## Descripción

Aplicación de escritorio desarrollada en Python que permite consultar el Archivo de Exoplanetas de la NASA de manera rápida y eficiente. El sistema carga un archivo CSV con datos de exoplanetas descubiertos y proporciona una interfaz gráfica intuitiva con menús desplegables para filtrar la información por año de descubrimiento, método de detección, estrella anfitriona e instalación que realizó el descubrimiento. La herramienta está diseñada para investigadores, estudiantes y entusiastas de la astronomía que necesitan acceder a información actualizada sobre exoplanetas de forma ágil, mostrando los resultados en formato tabular con capacidades de ordenamiento y enlaces directos a la página oficial de la NASA para obtener información detallada de cada planeta confirmado.

## User Stories

- Como **investigador astronómico**, quiero **filtrar exoplanetas por año de descubrimiento** para **analizar la evolución de los hallazgos en el tiempo**.
- Como **estudiante de astronomía**, quiero **buscar por método de descubrimiento** para **estudiar las diferentes técnicas de detección de exoplanetas**.
- Como **divulgador científico**, quiero **consultar por estrella anfitriona** para **preparar material educativo sobre sistemas planetarios específicos**.
- Como **entusiasta de la astronomía**, quiero **ordenar los resultados por cualquier columna** para **explorar los datos desde diferentes perspectivas**.
- Como **usuario general**, quiero **hacer clic en el nombre de la estrella** para **acceder directamente a la página de la NASA con información detallada del planeta**.
- Como **investigador**, quiero **recibir un mensaje de error si intento buscar sin seleccionar criterios** para **saber que debo especificar al menos un filtro**.

## Metodología

**Ágil (Scrum)**

El proyecto se desarrolla bajo un enfoque ágil con entregas incrementales, priorizando las funcionalidades de mayor valor para el usuario. Las historias de usuario definen los requisitos y permiten una planificación flexible en sprints de 1 a 2 semanas, facilitando la adaptación a cambios y la retroalimentación continua.

**Sprints planificados:**
- **Sprint 1:** Carga eficiente de datos CSV con Pandas y estructura base del proyecto.
- **Sprint 2:** Panel de consulta con menús desplegables y botones Buscar/Limpiar.
- **Sprint 3:** Visualización de resultados en formato tabular.
- **Sprint 4:** Ordenamiento por columnas con flechas ascendentes/descendentes.
- **Sprint 5:** Enlaces a NASA y funcionalidades adicionales.

## Tecnologías utilizadas

- **Python 3.8+** - Lenguaje de programación principal
- **Pandas** - Procesamiento y carga eficiente de datos CSV
- **NumPy** - Operaciones numéricas optimizadas
- **Tkinter** - Interfaz gráfica de usuario (incluida en Python)
- **Pytest** - Pruebas unitarias

## Características principales

- 🔍 **Búsqueda multicriterio** por año, método, estrella anfitriona e instalación
- 📊 **Visualización en tabla** con los resultados de la consulta
- ⬆️⬇️ **Ordenamiento interactivo** ascendente/descendente por cualquier columna
- 🔗 **Enlaces directos** a la página oficial del Exoplanet Archive de NASA
- 🎯 **Interfaz intuitiva** con menús desplegables
- ⚡ **Carga eficiente** de grandes volúmenes de datos
- 🧹 **Botón Limpiar** para resetear búsquedas
- 🚨 **Validación** de búsqueda sin filtros seleccionados

## Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/exoplanet-consultor.git
cd exoplanet-consultor
