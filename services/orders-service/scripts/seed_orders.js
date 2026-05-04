require('dotenv').config();

const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose');
const connectDB = require('../src/config/db');
const Order = require('../src/models/Order');

const TOTAL_FAKE_ORDERS = 20000;
const BATCH_SIZE = 1000;
const USER_IDS_FILE = path.resolve(__dirname, '../../user-service/scripts/generated_user_ids.json');

const PRODUCT_CATALOG = [
  { id: '1', nombre: 'ASUS X570 B550 B450', precio_unitario: 600.00 },
  { id: '2', nombre: 'MEMORIA DDR4 16GB 3200 CL16 FURY BEAST RGB BLACK', precio_unitario: 680.00 },
  { id: '3', nombre: 'MEMORIA DDR4 16GB 3200 CL16 XPG SPECTRIX D35G RGB', precio_unitario: 500.00 },
  { id: '4', nombre: 'TARJETA DE VIDEO GIGABYTE GEFORCE RTX 3070 GAMING OC 8G GDDR6', precio_unitario: 44000.00 },
  { id: '5', nombre: 'Tarjeta de video Gigabyte Aorus RTX 5090', precio_unitario: 18000.00 },
  { id: '6', nombre: 'Tarjeta Gráfica PNY GeForce RTX 5070', precio_unitario: 4000.00 },
  { id: '7', nombre: 'FUENTE 850W 80 plus', precio_unitario: 400.00 },
  { id: '8', nombre: 'FUENTE DE PODER EVGA 750 B5, 750W', precio_unitario: 450.00 },
  { id: '9', nombre: 'Gabinete Atx', precio_unitario: 400.00 },
  { id: '10', nombre: 'Gabinete Thermaltake V200 TG', precio_unitario: 360.00 },
  { id: '11', nombre: 'MSI GE66 Raider', precio_unitario: 1000.00	 },
  { id: '12', nombre: 'Placa Base Gigabyte X570 Aorus Master', precio_unitario: 920.00 },
  { id: '13', nombre: 'Procesador Amd Ryzen 9 7950x', precio_unitario: 860.00 },
  { id: '14', nombre: 'PROCESADOR AMD RYZEN 7 8700G', precio_unitario: 650.00 },
  { id: '15', nombre: 'Procesador Intel Core Ultra 5 225', precio_unitario: 850.00 },

];

const CITIES = [
  ['Madrid', 'Spain'],
  ['Lima', 'Peru'],
  ['Santiago', 'Chile'],
  ['Bogota', 'Colombia'],
  ['Buenos Aires', 'Argentina'],
  ['Sevilla', 'Spain'],
  ['Medellin', 'Colombia'],
  ['Valparaiso', 'Chile'],
  ['Arequipa', 'Peru'],
  ['Cordoba', 'Argentina'],
  ['Barcelona', 'Spain'],
  ['Quito', 'Ecuador'],
  ['Montevideo', 'Uruguay'],
  ['La Paz', 'Bolivia'],
  ['San Jose', 'Costa Rica'],
  ['Guadalajara', 'Mexico'],
  ['Cartagena', 'Colombia'],
  ['Cali', 'Colombia'],
  ['Trujillo', 'Peru'],
  ['Maracaibo', 'Venezuela'],
];

const STATES = ['pendiente', 'pagado', 'enviado', 'completado'];

function readUserIds() {
  if (!fs.existsSync(USER_IDS_FILE)) {
    throw new Error(
      `No se encontro ${USER_IDS_FILE}. Ejecuta primero el seed de users para generar los IDs.`
    );
  }

  const raw = fs.readFileSync(USER_IDS_FILE, 'utf-8');
  const parsed = JSON.parse(raw);
  const ids = parsed.generated_user_ids;

  if (!Array.isArray(ids) || ids.length === 0) {
    throw new Error('El archivo generated_user_ids.json no contiene user ids validos.');
  }

  return ids;
}

function randomItem(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function randomDate() {
  const start = new Date('2024-01-01T00:00:00Z');
  const end = new Date('2026-04-30T23:59:59Z');
  const time = start.getTime() + Math.random() * (end.getTime() - start.getTime());
  return new Date(time);
}

function buildOrder(orderNumber, userIds) {
  const product = randomItem(PRODUCT_CATALOG);
  const cantidad = Math.floor(Math.random() * 4) + 1;
  const subtotal = Number((product.precio_unitario * cantidad).toFixed(2));
  const [ciudad, pais] = randomItem(CITIES);

  return {
    user_id: randomItem(userIds),
    estado: randomItem(STATES),
    fecha: randomDate(),
    productos: [
      {
        product_id: product.id,
        nombre: product.nombre,
        precio_unitario: product.precio_unitario,
        cantidad,
        subtotal,
      },
    ],
    total: subtotal,
    direccion_envio: {
      direccion: `Calle ${orderNumber} #${Math.floor(Math.random() * 200) + 1}`,
      ciudad,
      pais,
      codigo_postal: `${Math.floor(Math.random() * 90000) + 10000}`,
    },
  };
}

async function main() {
  await connectDB();

  const userIds = readUserIds();
  const existingOrders = await Order.countDocuments();

  if (existingOrders >= TOTAL_FAKE_ORDERS) {
    console.log(`Ya existen ${existingOrders} ordenes. No se inserta nada.`);
    await mongoose.connection.close();
    return;
  }

  const toInsert = TOTAL_FAKE_ORDERS - existingOrders;
  console.log(`Insertando ${toInsert} ordenes fake...`);

  const docs = [];
  for (let index = 1; index <= toInsert; index += 1) {
    docs.push(buildOrder(existingOrders + index, userIds));

    if (docs.length === BATCH_SIZE) {
      await Order.insertMany(docs);
      console.log(`Insertadas ${existingOrders + index} ordenes...`);
      docs.length = 0;
    }
  }

  if (docs.length > 0) {
    await Order.insertMany(docs);
  }

  console.log('Seed de ordenes completado.');
  await mongoose.connection.close();
}

main().catch(async (error) => {
  console.error('Error en seed de ordenes:', error.message);
  if (mongoose.connection.readyState !== 0) {
    await mongoose.connection.close();
  }
  process.exit(1);
});
