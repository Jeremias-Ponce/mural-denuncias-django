document.addEventListener("DOMContentLoaded", function() {
    const botones = document.querySelectorAll(".btn-filtro");
    const papelitos = document.querySelectorAll(".papelito");

    botones.forEach(boton => {
        boton.addEventListener("click", function() {
            const categoriaSeleccionada = this.getAttribute("data-categoria");

            papelitos.forEach(papelito => {
                const categoriaPapelito = papelito.getAttribute("data-categoria");

                if (categoriaSeleccionada === "TODOS" || categoriaPapelito === categoriaSeleccionada) {
                    papelito.classList.remove("ocultar");
                } else {
                    papelito.classList.add("ocultar");
                }
            });
        });
    });
});