const API = '/api/peliculas'

const tabla = document.getElementById('tablaPeliculas')
c

async function listar(){
    const res = await fetch(API + '/');
    const peliculas = await res.json();

    tabla.innerHTML = ''
    peliculas.forEach(p => {
        const tr = document.createElement('tr');

        [p.id, p.nombre, p.genero, p.director, p.duracion].forEach(valor => {
            const td = document.createElement('td');
            td.textContent = valor;
            tr.appendChild(td);
        });

        tabla.appendChild(tr);
    });
}

listar();