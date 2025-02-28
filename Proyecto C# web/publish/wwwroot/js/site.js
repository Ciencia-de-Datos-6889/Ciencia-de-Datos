// Please see documentation at https://learn.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.




    // Evento global para manejar clics en "Agregar Usuario" y "Editar Usuario"
    document.addEventListener('click', function (event) {
        const target = event.target;

        if (target.id === 'agregar-usuario' || target.classList.contains('editar-usuario')) {
            event.preventDefault();
            const url = target.getAttribute('href');

            fetch(url)
                .then(response => response.text())
                .then(data => {
                    document.getElementById('content').innerHTML = data;
                })
                .catch(error => console.error('Error:', error));
        }
    });

    // Manejo del enlace "Usuarios" para cargar la vista CRUD
    document.getElementById('usuarios-link').addEventListener('click', function(event) {
        event.preventDefault();

        fetch('@Url.Action("Crud", "Auth")')
            .then(response => response.text())
            .then(data => {
                document.getElementById('content').innerHTML = data;
            })
            .catch(error => console.error('Error:', error));
    });
