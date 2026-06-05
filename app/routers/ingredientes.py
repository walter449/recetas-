from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Ingrediente
from app.schemas.schemas import IngredienteCreate, IngredienteOut
from app.routers.auth import get_current_user

router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])

@router.post("/", response_model=IngredienteOut)
def crear(ing: IngredienteCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    nuevo = Ingrediente(**ing.dict(), usuario_id=current_user.id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[IngredienteOut])
def listar(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Ingrediente).filter(Ingrediente.usuario_id == current_user.id).all()

@router.delete("/{ing_id}")
def eliminar(ing_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ing = db.query(Ingrediente).filter(Ingrediente.id == ing_id, Ingrediente.usuario_id == current_user.id).first()
    if not ing:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    db.delete(ing)
    db.commit()
    return {"mensaje": "Ingrediente eliminado"}

@router.put("/{ing_id}", response_model=IngredienteOut)
def actualizar(ing_id: int, ing: IngredienteCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existente = db.query(Ingrediente).filter(Ingrediente.id == ing_id, Ingrediente.usuario_id == current_user.id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    for key, val in ing.dict().items():
        setattr(existente, key, val)
    db.commit()
    db.refresh(existente)
    return existente