# Retrospectiva del Proyecto - Consulta de Exoplanetas de la NASA

## ✅ ¿Qué funcionó bien?

1. **Organización con Kanban:** Los issues (#1 al #8) permitieron avanzar de forma estructurada y medible.
2. **Carga eficiente con Pandas:** 40,106 exoplanetas cargados en ~1.8 segundos con tipos optimizados.
3. **Interfaz atractiva:** Colores oficiales NASA, imagen de fondo y bordes remarcados.
4. **Funcionalidad completa:** Búsqueda, ordenamiento, enlaces a NASA y validaciones.
5. **Control de versiones con Git:** Commits por issue y subida a GitHub con rama `main`.

## ❌ ¿Qué no funcionó / qué nos costó trabajo?

1. **Subir el CSV a GitHub:** El archivo de 132 MB excedía el límite de 100 MB. Se resolvió con `.gitignore` y script de descarga automática.
2. **Mostrar la imagen de fondo:** El orden de creación en Tkinter era incorrecto. Se resolvió usando Canvas y `lower()`.
3. **Ordenamiento con mayúsculas:** Distinguía entre mayúsculas y minúsculas. Se resolvió con `.str.lower()` en `sort_dataframe()`.
4. **Conflicto de ramas:** `master` vs `main`. Se resolvió renombrando la rama local y cambiando la predeterminada en GitHub.
5. **Tiempo de carga inicial:** 1.8 segundos (aceptable, pero mejorable con caché).

## 🔄 ¿Qué haríamos distinto la próxima vez?

1. **Validar columnas del CSV antes de codificar** para evitar sorpresas.
2. **Usar `git filter-repo` desde el inicio** para evitar problemas con archivos grandes.
3. **Escribir pruebas unitarias junto con el código (TDD)** para detectar errores temprano.
4. **Agregar exportación a CSV** para facilitar el análisis externo.
5. **Incluir capturas de pantalla en el README** desde el principio.
6. **Manejar errores con logs más detallados** para facilitar la depuración.
