from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

from database import engine, Base
from models import user as md_user
from models import address as md_address
from routers import users, addresses

# Crear tablas en caso de no usar Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users Service", description="Microservicio de usuarios y direcciones")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.error(f"Error detectado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Ocurrió un error interno en el servidor."}
    )


app.include_router(users.router)
app.include_router(addresses.router)
