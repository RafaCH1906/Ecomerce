# E-commerce Backend y Frontend

Este repositorio contiene el backend dividido en microservicios, el frontend y la configuración de despliegue para AWS Academy.

## Estructura principal

### Backend

- `services/docker-compose.ec2-db.yml`: levanta solo las bases de datos.
- `services/docker-compose.ec2.yml`: levanta los microservicios de aplicación.
- `services/.env.ec2.example`: plantilla de variables para despliegue.

### Frontend

- `Ecomerce-front/`: aplicación web en React.

## Despliegue recomendado en AWS Academy

La forma correcta de montarlo es con 2 EC2 separadas:

1. Una EC2 para bases de datos.
2. Una EC2 para los microservicios de backend.

Si quieres, el frontend puede ir luego en otra EC2 o en un hosting separado, pero el backend ya queda ordenado con esta separación.

---

## 0. Crear las 2 instancias en AWS Academy (paso a paso)

Esta sección es desde cero, directamente en la consola de AWS Academy.

### 0.1 Entrar al laboratorio

1. Abre AWS Academy Learner Lab.
2. Inicia el laboratorio y entra a AWS Console.
3. Verifica la región activa en la esquina superior derecha y usa siempre la misma para todo.

### 0.2 Crear Key Pair

1. Ve a EC2.
2. En el menú lateral abre Key Pairs.
3. Crea una nueva llave, por ejemplo: `ecommerce-key`.
4. Tipo recomendado: RSA.
5. Formato: `.pem`.
6. Descarga el archivo y guárdalo en tu PC de forma segura.

### 0.3 Crear Security Groups

Crea 2 grupos de seguridad para separar responsabilidades.

#### A) SG para base de datos

Nombre sugerido: `sg-ecommerce-db`.

Reglas de entrada recomendadas:

- PostgreSQL TCP 5432 con origen: Security Group de aplicaciones.
- MySQL TCP 3306 con origen: Security Group de aplicaciones.
- MongoDB TCP 27017 con origen: Security Group de aplicaciones.
- SSH TCP 22 con origen: tu IP pública (solo para administración).

#### B) SG para aplicaciones

Nombre sugerido: `sg-ecommerce-apps`.

Reglas de entrada recomendadas:

- SSH TCP 22 con origen: tu IP pública.
- TCP 8000 con origen: 0.0.0.0/0 (si quieres exponer Users públicamente).
- TCP 8081 con origen: 0.0.0.0/0 (Products).
- TCP 3003 con origen: 0.0.0.0/0 (Orders).
- TCP 8005 con origen: 0.0.0.0/0 (Aggregator).
- TCP 8006 con origen: 0.0.0.0/0 (Analytics).

Si prefieres más seguridad, en lugar de 0.0.0.0/0 usa solo tu IP o un balanceador.

### 0.4 Lanzar instancia 1 (bases)

1. EC2 > Instances > Launch instances.
2. Name: `ecommerce-db-ec2`.
3. AMI: Ubuntu Server 22.04 LTS (recomendado).
4. Instance type: `t2.micro` o el permitido por el laboratorio.
5. Key pair: selecciona `ecommerce-key`.
6. Network settings: selecciona `sg-ecommerce-db`.
7. Storage: deja el valor por defecto o sube a 16 GB si lo necesitas.
8. Launch instance.

### 0.5 Lanzar instancia 2 (apps)

1. EC2 > Instances > Launch instances.
2. Name: `ecommerce-apps-ec2`.
3. AMI: Ubuntu Server 22.04 LTS.
4. Instance type: `t2.micro` o el permitido.
5. Key pair: `ecommerce-key`.
6. Network settings: selecciona `sg-ecommerce-apps`.
7. Storage: recomendado 16 GB o más para imágenes Docker.
8. Launch instance.

### 0.6 Asignar IP fija a la EC2 de bases

1. Ve a EC2 > Elastic IPs.
2. Allocate Elastic IP address.
3. Selecciona la nueva Elastic IP y pulsa Associate.
4. Asóciala a la instancia `ecommerce-db-ec2`.
5. Copia esa IP, porque se usará en `USERS_DB_HOST`, `PRODUCTS_DB_HOST` y `ORDERS_DB_HOST`.

Si tu laboratorio no permite Elastic IP, usa IP privada fija dentro de la VPC y asegúrate que ambas instancias estén en la misma red y con rutas válidas.

### 0.7 Conexión SSH a cada instancia

Desde tu terminal local:

```bash
ssh -i /ruta/a/ecommerce-key.pem ubuntu@IP_PUBLICA_DE_LA_EC2
```

Ejemplo de rutas en Windows con Git Bash:

```bash
ssh -i /c/Users/TU_USUARIO/Downloads/ecommerce-key.pem ubuntu@IP_PUBLICA_DE_LA_EC2
```

---

## 1. EC2 de bases de datos

### Qué corre aquí

- PostgreSQL para users.
- MySQL para products.
- MongoDB para orders.

### Ruta dentro de la EC2

Supongamos que clonas el repo en:

```bash
/home/ubuntu/Ecomerce
```

Entonces los archivos importantes quedan en:

- `/home/ubuntu/Ecomerce/services/docker-compose.ec2-db.yml`
- `/home/ubuntu/Ecomerce/services/.env.ec2`

### Paso a paso

1. Entra a la carpeta del proyecto.

```bash
cd /home/ubuntu/Ecomerce/services
```

2. Crea el archivo de variables a partir del ejemplo.

```bash
cp .env.ec2.example .env.ec2
```

3. Edita `.env.ec2` y completa las credenciales de las bases.

4. Levanta solo las bases de datos.

```bash
docker compose --env-file .env.ec2 -f docker-compose.ec2-db.yml up -d
```

### Puertos de esta EC2

Abre solo lo necesario en el Security Group de la EC2 de bases:

- `5432` para PostgreSQL
- `3306` para MySQL
- `27017` para MongoDB

### Importante

La EC2 de bases debe tener IP fija. Lo ideal es un Elastic IP o una IP privada fija si ambas máquinas están dentro de la misma red.

---

## 2. EC2 de aplicaciones

### Qué corre aquí

- `users-service`
- `products-service`
- `orders-service`
- `aggregator-service`
- `analytics-service`

### Rutas dentro de la EC2

Si el repo está clonado en:

```bash
/home/ubuntu/Ecomerce
```

los archivos usados aquí son:

- `/home/ubuntu/Ecomerce/services/docker-compose.ec2.yml`
- `/home/ubuntu/Ecomerce/services/.env.ec2`

### Paso a paso

1. Entra a la carpeta de servicios.

```bash
cd /home/ubuntu/Ecomerce/services
```

2. Copia la plantilla de variables.

```bash
cp .env.ec2.example .env.ec2
```

3. Edita `.env.ec2` y reemplaza estos hosts con la IP fija de la EC2 de bases:

```env
USERS_DB_HOST=IP_FIJA_DE_LA_EC2_DE_BD
PRODUCTS_DB_HOST=IP_FIJA_DE_LA_EC2_DE_BD
ORDERS_DB_HOST=IP_FIJA_DE_LA_EC2_DE_BD
```

4. Verifica también las credenciales compartidas:

```env
JWT_SECRET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SESSION_TOKEN=
AWS_REGION=
S3_BUCKET=
ATHENA_DATABASE=
ATHENA_OUTPUT_LOCATION=
```

5. Levanta los microservicios.

```bash
docker compose --env-file .env.ec2 -f docker-compose.ec2.yml up -d
```

---

## 3. URLs y rutas de acceso

Si la EC2 de aplicaciones tiene IP pública, estos son los accesos principales:

- Users Service: `http://IP_EC2_APPS:8000/docs`
- Products Service: `http://IP_EC2_APPS:8081/swagger-ui.html`
- Orders Service: `http://IP_EC2_APPS:3003/api-docs`
- Aggregator Service: `http://IP_EC2_APPS:8005/docs`
- Analytics Service: `http://IP_EC2_APPS:8006/docs`

Si pruebas desde dentro de la misma EC2, también puedes usar `localhost`:

- `http://localhost:8000/docs`
- `http://localhost:8081/swagger-ui.html`
- `http://localhost:3003/api-docs`
- `http://localhost:8005/docs`
- `http://localhost:8006/docs`

---

## 4. Orden recomendado de despliegue

1. Sube primero la EC2 de bases de datos.
2. Verifica que PostgreSQL, MySQL y MongoDB estén arriba.
3. Asigna IP fija a esa EC2.
4. Configura la EC2 de backend con esa IP en `.env.ec2`.
5. Sube la EC2 de aplicaciones.
6. Abre los puertos públicos solo de los servicios backend.

---

## 5. Archivos de entorno y GitHub

No subas el `.env` real a GitHub.

Lo correcto es:

- subir `services/.env.ec2.example`
- mantener `services/.env.ec2` fuera del repositorio
- guardar secretos reales solo en la EC2 o en GitHub Secrets

### Sobre Deploy Keys

El apartado de Deploy Keys de GitHub no sirve para guardar variables `.env`.

Sirve para dar acceso SSH a un repositorio privado desde una máquina o automatización.

---

## 6. Verificación rápida

En la EC2 de aplicaciones corre:

```bash
docker ps
```

Y revisa que estén estos contenedores:

- `users-service`
- `products-service`
- `orders-service`
- `aggregator-service`
- `analytics-service`

En la EC2 de bases revisa:

- `users-db`
- `products-db`
- `orders-db`

---

## 7. Notas finales

- La base de datos no debe quedar mezclada con los microservicios si el objetivo es simular un despliegue real en AWS Academy.
- La IP de la EC2 de bases debe ser estable.
- El archivo `.env.ec2.example` es plantilla, no secreto.
- Si luego quieres automatizar todo, el siguiente paso natural es usar GitHub Actions o scripts de despliegue.