const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema({
  user_id: {
    type: Number,
    required: [true, 'El user_id es obligatorio']
  },
  estado: {
    type: String,
    enum: ['pendiente', 'pagado', 'enviado', 'completado', 'cancelado'],
    default: 'pendiente'
  },
  fecha: {
    type: Date,
    default: Date.now
  },
  productos: [{
    product_id: {
      type: String,
      required: true
    },
    nombre: {
      type: String,
      required: true
    },
    precio_unitario: {
      type: Number,
      required: true
    },
    cantidad: {
      type: Number,
      required: true,
      min: 1
    },
    subtotal: {
      type: Number,
      required: true
    }
  }],
  total: {
    type: Number,
    required: true
  },
  direccion_envio: {
    direccion: { type: String, required: true },
    ciudad: { type: String, required: true },
    pais: { type: String, required: true },
    codigo_postal: { type: String, required: true }
  }
}, {
  timestamps: { createdAt: 'created_at', updatedAt: false }
});

const Order = mongoose.model('Order', orderSchema);

module.exports = Order;
