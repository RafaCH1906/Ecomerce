import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import aggregator

load_dotenv()

app = FastAPI(
    title="Aggregator Service",
    description="Microservicio para agregar y orquestar datos de Users, Products y Orders",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de rutas
app.include_router(aggregator.router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "aggregator-service"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
