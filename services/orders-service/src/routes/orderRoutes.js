const express = require('express');
const router = express.Router();
const orderController = require('../controllers/orderController');

const { auth, isAdmin } = require('../middleware/auth');

router.get('/', auth, isAdmin, orderController.getOrders); // Solo admin ve todas
router.post('/', auth, orderController.createOrder);     // Cualquier logueado crea
router.get('/:id', auth, orderController.getOrderById);
router.delete('/:id', auth, isAdmin, orderController.deleteOrder); // Solo admin borra
router.patch('/:id/status', auth, isAdmin, orderController.updateStatus); // Solo admin cambia estado
router.get('/user/:user_id', auth, orderController.getOrdersByUserId);

module.exports = router;
