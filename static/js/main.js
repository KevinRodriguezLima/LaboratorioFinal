function generateSHA1() {
    const msg = document.getElementById("msg").value;

    fetch("/api/sha1", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({message: msg})
    })
    .then(r => r.json())
    .then(d => {
        document.getElementById("output").value = d.hash;
    });
}
