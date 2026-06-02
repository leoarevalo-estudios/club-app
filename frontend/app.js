/*************************************************
 * � CREDENCIALES (demo local)
 *************************************************/
const USUARIO_VALIDO = "admin";
const PASSWORD_VALIDA = "admin";

/*************************************************
 * � ESTADO GLOBAL DE LA APP
 *************************************************/
let editandoId = null;
let sociosCache = [];

/*************************************************
 * � ELEMENTOS DEL DOM (UI)
 *************************************************/
const pantallaInicio = document.getElementById("pantalla-inicio");
const pantallaLogin = document.getElementById("pantalla-login");
const dashboard = document.getElementById("dashboard");

const btnLogin = document.getElementById("btn-login");
const btnLogout = document.getElementById("btn-logout");

const btnNuevo = document.getElementById("btn-nuevo");
const formSocio = document.getElementById("form-socio");
const btnGuardar = document.getElementById("btn-guardar");
const buscador = document.getElementById("buscador");

/*************************************************
 * � INICIO DE LA APP (pantalla inicial)
 *************************************************/
pantallaInicio.addEventListener("click", () => {
    pantallaInicio.classList.add("oculto");
    pantallaLogin.classList.remove("oculto");
});

/*************************************************
 * � LOGIN
 *************************************************/
btnLogin.addEventListener("click", () => {

    const usuario = document.getElementById("usuario").value.trim();
    const password = document.getElementById("password").value.trim();

    if (usuario !== USUARIO_VALIDO || password !== PASSWORD_VALIDA) {
        alert("Usuario o contraseña incorrectos");
        return;
    }

    sessionStorage.setItem("logueado", "true");

    pantallaLogin.classList.add("oculto");
    dashboard.classList.remove("oculto");

    cargarSocios();
});

/*************************************************
 * � LOGOUT
 *************************************************/
btnLogout.addEventListener("click", () => {

    sessionStorage.removeItem("logueado");

    dashboard.classList.add("oculto");
    pantallaLogin.classList.remove("oculto");

    document.getElementById("usuario").value = "";
    document.getElementById("password").value = "";
});

/*************************************************
 * � CARGA DE SOCIOS (API)
 *************************************************/
async function cargarSocios() {

    const res = await fetch("http://127.0.0.1:8000/socios");
    const data = await res.json();

    sociosCache = data;

    renderSocios(data);
}

/*************************************************
 * � RENDER DE LISTA (UI)
 *************************************************/
function renderSocios(data) {

    const lista = document.getElementById("lista-socios");
    lista.innerHTML = "";

    data.forEach((socio) => {

        const div = document.createElement("div");
        div.classList.add("socio-item");

        div.innerHTML = `
        <div class="socio-row">

            <div class="col id">
                #${socio.numero_socio}
            </div>

            <div class="col nombre">
                ${socio.nombre} ${socio.apellido}
            </div>

            <div class="col dni">
                ${socio.dni}
            </div>

            <div class="col edad">
                ${calcularEdad(socio.fecha_nacimiento)}
            </div>

            <div class="col fecha">
                ${socio.fecha_nacimiento.split("-").reverse().join("/")}
            </div>

            <div class="col acciones">
                <button class="btn-editar" data-id="${socio.numero_socio}">
                    Editar
                </button>
                <button class="btn-eliminar" data-id="${socio.numero_socio}">
                    Eliminar
                </button>
            </div>

        </div>
        `;

        lista.appendChild(div);
    });

    activarBotones();
}

/*************************************************
 * �️ BOTONES DINÁMICOS (editar / eliminar)
 *************************************************/
function activarBotones() {

    document.querySelectorAll(".btn-eliminar").forEach(btn => {

        btn.addEventListener("click", async () => {

            const id = btn.dataset.id;

            if (!confirm(`¿Eliminar socio ${id}?`)) return;

            await fetch(`http://127.0.0.1:8000/socios/${id}`, {
                method: "DELETE"
            });

            cargarSocios();
        });
    });

    document.querySelectorAll(".btn-editar").forEach(btn => {

        btn.addEventListener("click", () => {

            const id = btn.dataset.id;

            const socio = sociosCache.find(s => s.numero_socio == id);

            document.getElementById("nombre").value = socio.nombre;
            document.getElementById("apellido").value = socio.apellido;
            document.getElementById("dni").value = socio.dni;
            document.getElementById("fecha").value = socio.fecha_nacimiento;

            formSocio.classList.remove("oculto");

            editandoId = id;
        });
    });
}

/*************************************************
 * ➕ CREAR / EDITAR SOCIO
 *************************************************/
btnGuardar.addEventListener("click", async () => {

    const nombre = document.getElementById("nombre").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const dni = document.getElementById("dni").value.trim();
    const fecha = document.getElementById("fecha").value;

    // VALIDACIÓN
    if (!nombre || !apellido || !dni || !fecha) {
        alert("Completa todos los campos");
        return;
    }

    const hoy = new Date();
    const nacimiento = new Date(fecha);

    if (nacimiento > hoy) {
        alert("Fecha de nacimiento inválida");
        return;
    }

    const edad = calcularEdad(fecha);

    if (edad < 0 || edad > 120) {
        alert("Edad inválida");
        return;
    }

    // EDITAR
    if (editandoId) {

        await fetch(`http://127.0.0.1:8000/socios/${editandoId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, apellido, dni, fecha_nacimiento: fecha })
        });

        editandoId = null;
    }

    // CREAR
    else {

        await fetch("http://127.0.0.1:8000/socios", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, apellido, dni, fecha_nacimiento: fecha })
        });
    }

    // RESET UI
    formSocio.classList.add("oculto");
    limpiarFormulario();
    cargarSocios();
});

/*************************************************
 * � FORMULARIO
 *************************************************/
btnNuevo.addEventListener("click", () => {

    const oculto = formSocio.classList.contains("oculto");

    if (oculto) {
        formSocio.classList.remove("oculto");
        limpiarFormulario();
        editandoId = null;
    } else {
        formSocio.classList.add("oculto");
    }
});

function limpiarFormulario() {
    document.getElementById("nombre").value = "";
    document.getElementById("apellido").value = "";
    document.getElementById("dni").value = "";
    document.getElementById("fecha").value = "";
}

/*************************************************
 * � UTILIDAD: EDAD
 *************************************************/
function calcularEdad(fechaNacimiento) {

    const hoy = new Date();
    const nacimiento = new Date(fechaNacimiento);

    let edad = hoy.getFullYear() - nacimiento.getFullYear();

    const mes = hoy.getMonth() - nacimiento.getMonth();

    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--;
    }

    return edad;
}

/*************************************************
 * � BUSCADOR
 *************************************************/
buscador.addEventListener("input", () => {

    let valor = buscador.value.replace(/\D/g, "");
    buscador.value = valor;

    if (!sociosCache.length) return;

    if (valor === "") {
        renderSocios(sociosCache);
        return;
    }

    const filtrados = sociosCache.filter(s =>
        s.numero_socio == Number(valor)
    );

    renderSocios(filtrados);
});