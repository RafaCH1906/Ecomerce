from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

from database import engine, Base, SessionLocal
from models import user as md_user
from models import address as md_address
from routers import users, addresses, auth
from services.auth import get_password_hash
from sqlalchemy import text

# Crear tablas en caso de no usar Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users Service", description="Microservicio de usuarios y direcciones con Auth integrada")

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Migración cruda: asegurarse de que existan columnas nuevas si la tabla ya estaba creada antes
        try:
            db.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'user';"))
            db.commit()
            logging.info("Columna 'role' añadida a la base de datos satisfactoriamente.")
        except Exception as e:
            db.rollback()
            logging.info("La columna 'role' ya existe u ocurrió un error menor ignorado.")
        
        # Generar usuario superadmin si no existe
        superadmin = db.query(md_user.User).filter(md_user.User.nombre == "rafael").first()
        if not superadmin:
            logging.info("Creando usuario superadmin 'rafael' por primera vez...")
            admin_user = md_user.User(
                nombre="rafael",
                email="rafael@superadmin.com",
                password=get_password_hash("admin123"),
                role="superadmin",
                activo=True
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.error(f"Error detectado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Ocurrió un error interno en el servidor."}
    )


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(addresses.router)
