const Order = require('../models/Order');
const axios = require('axios');

class OrderService {
  async getAllOrders() {
    return await Order.find();
  }

  async getOrderById(id) {
    return await Order.findById(id);
  }

  async createOrder(orderData) {
    // 1. Validar que el usuario existe en el Users Service
    try {
      await axios.get(`${process.env.USER_SERVICE_URL}/${orderData.user_id}`);
    } catch (error) {
      console.error('Error al validar usuario:', error.message);
      throw new Error(`El usuario con ID ${orderData.user_id} no existe en el sistema de usuarios.`);
    }

    // 2. Validar que cada producto existe en el Products Service
    for (const producto of orderData.productos) {
      try {
        await axios.get(`${process.env.PRODUCT_SERVICE_URL}/${producto.product_id}`);
      } catch (error) {
        console.error(`Error al validar producto ${producto.product_id}:`, error.message);
        throw new Error(`El producto con ID ${producto.product_id} no existe o no está disponible.`);
      }
    }

    // 3. Calcular subtotales y total
    const productos = orderData.productos.map(p => ({
      ...p,
      subtotal: p.precio_unitario * p.cantidad
    }));
    
    const total = productos.reduce((acc, p) => acc + p.subtotal, 0);

    const order = new Order({
      ...orderData,
      productos,
      total
    });

    return await order.save();
  }

  async deleteOrder(id) {
    return await Order.findByIdAndDelete(id);
  }

  async updateOrderStatus(id, status) {
    return await Order.findByIdAndUpdate(
      id,
      { estado: status },
      { new: true, runValidators: true }
    );
  }

  async getOrdersByUserId(userId) {
    return await Order.find({ user_id: userId });
  }
}

module.exports = new OrderService();
