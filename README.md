# 🧩 Sudoku Multi-Variante con Algoritmo Genético

Proyecto desarrollado como demo interactiva de **Sudoku** en distintos tamaños (4×4, 6×6, 9×9, 12×12 y 16×16), con generación de tableros mediante un **Algoritmo Genético (GA)** y visualización en vivo de la evolución.

Incluye validación de unicidad de solución en tableros hasta 12×12. Para 16×16 se ofrece en versión **beta**.

---

## ✨ Características

- 🎨 **Interfaz limpia y responsive** (modo claro/oscuro).
- 🧠 **Generación de tableros con GA** (fitness = número de conflictos).
- 📊 **Monitor de evolución** en tiempo real (gráfica + log de generaciones).
- ✅ **Validación de unicidad** con solver backtracking (hasta 12×12).
- ⏱ **Cronómetro integrado** y control de dificultad (Fácil/Medio/Difícil/Experto).
- ♻️ **Fallback seguro**: si el GA no converge, usa un patrón latino válido.
- 🌓 **Tema guardado en localStorage** (persistencia del modo oscuro/claro).

---

## 📂 Estructura del proyecto

```
AppSudoku.html    # Único archivo del proyecto (HTML + CSS + JS embebidos)
```

---

## ⚙️ Instalación y ejecución

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Bxstix1010/E6-SUDOKU
   cd <repositorio>
   ```

2. No requiere dependencias externas. Solo abre el archivo:

   - Windows: `start AppSudoku.html`
   - macOS: `open AppSudoku.html`
   - Linux: `xdg-open AppSudoku.html`

3. Disfruta el juego directamente en tu navegador moderno (Chrome, Firefox, Edge).

---

## 🕹️ Uso

1. Selecciona **tamaño** y **nivel de dificultad**.
2. Haz clic en **Generar Sudoku**.
3. (Opcional) Activa el **monitor del GA** para ver cómo evoluciona la población.
4. Completa el tablero manualmente:
   - Los números fijos no pueden modificarse.
   - Usa teclado numérico o escribe en cada celda.
5. Presiona **Verificar** para comprobar si la solución es correcta.

---

## 📊 Tecnologías

- **HTML**  
- **CSS**  
- **JavaScript**  
- Canvas API (para gráfica del monitor)  
- LocalStorage (para persistencia del tema)  

---

## 🚧 Limitaciones actuales

- 🔹 En tableros **16×16** no siempre se garantiza unicidad (modo beta).  
- 🔹 El **Algoritmo Genético** puede tardar en converger en tamaños grandes.  
- 🔹 Falta soporte completo de accesibilidad (teclado y lector de pantalla).  

---

## 💡 Próximas mejoras

- Optimizar rendimiento del GA en tableros grandes.  
- Añadir **guardado/carga de partidas**.  
- Implementar **navegación por teclado** y anotaciones (candidatos).  
- Mejorar estadísticas y tiempos por nivel.  

---

## 👥 Autores

- Paula Alcarás  
- Bastián González  
- Hugo Serón  
- Fernanda Vásquez  
- Benjamín Zúñiga  

Proyecto desarrollado en el contexto académico de la carrera **Ingeniería Civil Informática – UNAB**.

---
