document.getElementById("myButton").addEventListener("click", function() {
    alert("¡Hola! Esto es JavaScript funcionando en Flask.");
});

fetch('/db_table/${rack}') 
.then(response => response.json())
.then(data => {
    console.log(data);
});
