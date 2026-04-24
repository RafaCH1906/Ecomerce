require('dotenv').config();
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');
const orderRoutes = require('./routes/orderRoutes');
const swaggerUi = require('swagger-ui-express');
const yaml = require('yamljs');
const path = require('path');

const app = express();

const corsOptions = {
  origin: ['http://localhost:5173', 'http://127.0.0.1:5173'],
  methods: ['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
};

// Conectar a la base de datos
connectDB();

// Middlewares
app.use(cors(corsOptions));
app.options('*', cors(corsOptions));
app.use(express.json());

// Swagger setup (opcional pero recomendado como pediste)
try {
  const swaggerDocument = yaml.load(path.join(__dirname, '../swagger.yaml'));
  app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
} catch (error) {
  console.log('Swagger no configurado o archivo swagger.yaml no encontrado.');
}

// Rutas
app.use('/api/orders', orderRoutes);

const PORT = process.env.PORT || 3003;

app.listen(PORT, () => {
  console.log(`Orders Service corriendo en el puerto ${PORT}`);
});
