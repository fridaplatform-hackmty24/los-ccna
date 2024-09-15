const express = require('express');
const cors = require('cors');

const app = express();
const port = 5000;

// Habilitar CORS (para permitir solicitudes desde el frontend React)
app.use(cors());

// Rutas API
app.get('/api/inventarios', (req, res) => {
    const inventarios = [
        { id: 1, producto: 'Laptop', cantidad: 20 },
        { id: 2, producto: 'Teclado', cantidad: 50 },
        { id: 3, producto: 'Monitor', cantidad: 15 },
    ];
    res.json(inventarios);
});

app.listen(port, () => {
    console.log(`Servidor backend ejecutándose en http://localhost:${port}`);
});
