function generateHash() {
    const msg = document.getElementById("msg").value;
    const algorithm = document.getElementById("algorithm").value;
    const statusEl = document.getElementById("status");

    if (!msg) {
        statusEl.textContent = "Por favor, ingresa un mensaje.";
        return;
    }

    statusEl.textContent = "Calculando hash...";

    fetch("/api/hash", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: msg, algorithm: algorithm })
    })
    .then(r => r.json())
    .then(d => {
        document.getElementById("output").value = d.hash;
        statusEl.textContent = "Algoritmo usado: " + d.algorithm;
    })
    .catch(err => {
        console.error(err);
        statusEl.textContent = "Ocurrió un error al calcular el hash.";
    });
}

function clearFields() {
    document.getElementById("msg").value = "";
    document.getElementById("output").value = "";
    document.getElementById("status").textContent = "";
}
