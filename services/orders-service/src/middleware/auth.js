const jwt = require('jsonwebtoken');

const auth = (req, res, next) => {
  const authHeader = req.header('Authorization');

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ 
      message: 'Acceso denegado. No se proporcionó un token de seguridad (Bearer).' 
    });
  }

  const token = authHeader.split(' ')[1];

  try {
    const verified = jwt.verify(token, process.env.JWT_SECRET, { algorithms: ['HS512'] });
    req.user = verified;
    next();
  } catch (error) {
    console.error('ERROR DE AUTENTICACIÓN EN ÓRDENES:', error.message);
    res.status(401).json({ message: 'Token no válido o expirado.' });
  }
};

const isAdmin = (req, res, next) => {
  if (req.user && (req.user.role === 'admin' || req.user.role === 'superadmin')) {
    next();
  } else {
    res.status(403).json({ message: 'Acceso denegado. Se requieren permisos de administrador.' });
  }
};

module.exports = { auth, isAdmin };
