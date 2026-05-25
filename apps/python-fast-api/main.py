from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import logging
import time
from config import settings

# Configuração básica de logging (preparada para OTel/JSON posteriormente)
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, version="1.0.0")

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float

# Simulação de base de dados em memória
items_db = []

@app.get("/health")
def health_check():
    logger.info("Healthcheck requested")
    return {"status": "ok", "version": "1.0.0", "env": settings.app_env}

@app.get("/api/v1/items")
def list_items(limit: int = Query(default=10, le=100), offset: int = Query(default=0, ge=0)):
    logger.info(f"List items: limit={limit}, offset={offset}")
    return items_db[offset:offset+limit]

@app.post("/api/v1/items")
def create_item(item: Item):
    logger.info(f"Create item: {item.name}")
    time.sleep(0.05)  # Simula processamento
    new_item = item.model_dump()
    new_item["id"] = len(items_db) + 1
    items_db.append(new_item)
    return new_item