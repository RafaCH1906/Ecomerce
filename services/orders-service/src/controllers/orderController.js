const orderService = require('../services/orderService');

exports.getOrders = async (req, res) => {
  try {
    const orders = await orderService.getAllOrders();
    res.status(200).json(orders);
  } catch (error) {
    res.status(500).json({ message: 'Error al obtener las órdenes', error: error.message });
  }
};

exports.getOrderById = async (req, res) => {
  try {
    const order = await orderService.getOrderById(req.params.id);
    if (!order) {
      return res.status(404).json({ message: 'Orden no encontrada' });
    }
    res.status(200).json(order);
  } catch (error) {
    res.status(500).json({ message: 'Error al obtener la orden', error: error.message });
  }
};

exports.createOrder = async (req, res) => {
  try {
    const newOrder = await orderService.createOrder(req.body);
    res.status(201).json(newOrder);
  } catch (error) {
    res.status(400).json({ message: 'Error al crear la orden', error: error.message });
  }
};

exports.deleteOrder = async (req, res) => {
  try {
    const deletedOrder = await orderService.deleteOrder(req.params.id);
    if (!deletedOrder) {
      return res.status(404).json({ message: 'Orden no encontrada' });
    }
    res.status(200).json({ message: 'Orden eliminada con éxito' });
  } catch (error) {
    res.status(500).json({ message: 'Error al eliminar la orden', error: error.message });
  }
};

exports.updateStatus = async (req, res) => {
  try {
    const { estado } = req.body;
    if (!estado) {
      return res.status(400).json({ message: 'El campo estado es obligatorio' });
    }
    const updatedOrder = await orderService.updateOrderStatus(req.params.id, estado);
    if (!updatedOrder) {
      return res.status(404).json({ message: 'Orden no encontrada' });
    }
    res.status(200).json(updatedOrder);
  } catch (error) {
    res.status(500).json({ message: 'Error al actualizar el estado de la orden', error: error.message });
  }
};

exports.getOrdersByUserId = async (req, res) => {
  try {
    const userId = Number(req.params.user_id);
    if (isNaN(userId)) {
      return res.status(400).json({ message: 'El user_id debe ser un número' });
    }
    const orders = await orderService.getOrdersByUserId(userId);
    res.status(200).json(orders);
  } catch (error) {
    res.status(500).json({ message: 'Error al obtener las órdenes del usuario', error: error.message });
  }
};
