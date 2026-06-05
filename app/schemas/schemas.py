from pydantic import BaseModel
from typing import Optional, List

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class IngredienteCreate(BaseModel):
    nombre: str
    cantidad: str
    unidad: str

class IngredienteOut(IngredienteCreate):
    id: int
    class Config:
        from_attributes = True

class RecetaOut(BaseModel):
    id: int
    nombre_plato: str
    ingredientes_json: str
    pasos_json: str
    tiempo_estimado: str
    dificultad: str
    class Config:
        from_attributes = True

class CalificacionCreate(BaseModel):
    estrellas: int