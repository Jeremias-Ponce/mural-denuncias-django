// 1. Esperamos a que todo el HTML de la página web termine de cargar de forma segura
document.addEventListener("DOMContentLoaded", function() {
    
    // 2. Buscamos en la pantalla y agrupamos en listas todos los botones y todos los papelitos
    const botones = document.querySelectorAll(".btn-filtro");
    const papelitos = document.querySelectorAll(".papelito");

    // 3. Recorremos la lista de botones, uno por uno
    botones.forEach(boton => {
        
        // 4. A cada botón le asignamos un "vigilante" que reacciona cuando le hacen "click"
        boton.addEventListener("click", function() {
            
            // 5. Cuando hacen click, leemos y guardamos la etiqueta de ese botón (ej: "URG" o "TODOS")
            const categoriaSeleccionada = this.getAttribute("data-categoria");

            // 6. Ahora vamos a la pila de papelitos y los revisamos uno por uno
            papelitos.forEach(papelito => {
                
                // 7. Leemos la etiqueta secreta del papelito actual para saber de qué tipo es
                const categoriaPapelito = papelito.getAttribute("data-categoria");

                // 8. Decisión: ¿El botón dice "TODOS" o la categoría del papelito coincide con el botón?
                if (categoriaSeleccionada === "TODOS" || categoriaPapelito === categoriaSeleccionada) {
                    
                    // Si coincide: le quitamos la clase CSS que lo oculta (¡Se hace visible!)
                    papelito.classList.remove("ocultar");
                    
                } else {
                    
                    // Si NO coincide: le agregamos la clase CSS para esconderlo (¡Se hace invisible!)
                    papelito.classList.add("ocultar");
                }
            });
        });
    });
});