from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import importlib
import os
from database import engine, Base

# Recorrer todas las entidades e importar dinámicamente los modelos
entities_path = "./entities"
for entity_name in os.listdir(entities_path):
    entity_folder = os.path.join(entities_path, entity_name)
    models_path = os.path.join(entity_folder, "models.py")
    if os.path.isdir(entity_folder) and os.path.exists(models_path):
        module_name = f"entities.{entity_name}.models"
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError as e:
            print(f"Error al importar el modelo {module_name}: {e}")

# Crear las tablas automáticamente después de importar todos los modelos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar automáticamente todos los routers desde entities
for entity_name in os.listdir(entities_path):
    entity_folder = os.path.join(entities_path, entity_name)
    router_path = os.path.join(entity_folder, "router.py")
    if os.path.isdir(entity_folder) and os.path.exists(router_path):
        module_name = f"entities.{entity_name}.router"
        try:
            module = importlib.import_module(module_name)
            app.include_router(module.router)
        except ModuleNotFoundError as e:
            print(f"Error al importar el router {module_name}: {e}")