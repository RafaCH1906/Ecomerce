# E-commerce Backend (Microservicios)

Este repositorio documenta el backend de e-commerce basado en microservicios y su despliegue en AWS EC2.

## Resumen de arquitectura

El backend esta organizado para desplegarse en 2 instancias EC2:

1. EC2 de bases de datos.
2. EC2 de servicios de aplicacion.

### EC2 de bases de datos

Levanta unicamente motores de datos:

- PostgreSQL (users-service)
- MySQL (products-service)
- MongoDB (orders-service)

Archivo usado:

- `services/docker-compose.ec2-db.yml`

### EC2 de aplicacion

Levanta los microservicios backend:

- users-service
- products-service
- orders-service
- aggregator-service
- analytics-service

Archivo usado:

- `services/docker-compose.ec2.yml`

## Estructura relevante del backend

- `services/.env.ec2.example`: plantilla versionada de variables de entorno.
- `services/docker-compose.ec2-db.yml`: compose para bases de datos.
- `services/docker-compose.ec2.yml`: compose para servicios backend.
- `services/user-service/`: microservicio de usuarios (Python/FastAPI).
- `services/products-service/`: microservicio de productos (Java/Spring Boot).
- `services/orders-service/`: microservicio de ordenes (Node.js/Express).
- `services/aggregator-service/`: agregador de APIs (Python/FastAPI).
- `services/analytics-service/`: analitica y consultas (Python/FastAPI + Athena).

## Flujo de despliegue EC2

## 1) Levantar bases en la EC2 de DB

En la instancia de bases:

```bash
cd /home/ubuntu/Ecomerce/services
cp .env.ec2.example .env.ec2
# Editar credenciales y valores de DB

docker compose --env-file .env.ec2 -f docker-compose.ec2-db.yml up -d
```

## 2) Configurar hosts en la EC2 de apps

En la instancia de apps, usando la IP fija de la EC2 de bases:

```env
USERS_DB_HOST=IP_FIJA_EC2_DB
PRODUCTS_DB_HOST=IP_FIJA_EC2_DB
ORDERS_DB_HOST=IP_FIJA_EC2_DB
```

Luego levantar servicios:

```bash
cd /home/ubuntu/Ecomerce/services
cp .env.ec2.example .env.ec2
# Editar variables generales y credenciales

docker compose --env-file .env.ec2 -f docker-compose.ec2.yml up -d
```

## 3) Verificacion

En la EC2 de apps:

```bash
docker ps
```

Contenedores esperados:

- users-service
- products-service
- orders-service
- aggregator-service
- analytics-service

En la EC2 de DB:

- users-db
- products-db
- orders-db

## Endpoints principales (EC2 de apps)

- Users: `http://IP_EC2_APPS:8000/docs`
- Products: `http://IP_EC2_APPS:8081/swagger-ui.html`
- Orders: `http://IP_EC2_APPS:3003/api-docs`
- Aggregator: `http://IP_EC2_APPS:8005/docs`
- Analytics: `http://IP_EC2_APPS:8006/docs`

## Variables y seguridad

- Subir solo `services/.env.ec2.example` al repositorio.
- Mantener `services/.env.ec2` fuera de Git.
- No versionar secretos reales.
- Usar IP fija (Elastic IP o privada estable) para la EC2 de bases.
