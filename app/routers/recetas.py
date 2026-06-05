from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.database import get_db
from app.models.models import Receta, Ingrediente, Calificacion
from app.schemas.schemas import RecetaOut, CalificacionCreate
from app.services.llm_service import generar_receta
from app.routers.auth import get_current_user

router = APIRouter(prefix="/recetas", tags=["recetas"])

@router.post("/generar", response_model=RecetaOut)
def generar(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ingredientes = db.query(Ingrediente).filter(Ingrediente.usuario_id == current_user.id).all()
    if not ingredientes:
        raise HTTPException(status_code=400, detail="No tienes ingredientes en tu inventario")
    nombres = [i.nombre for i in ingredientes]
    receta_data = generar_receta(nombres)
    receta = Receta(
        nombre_plato=receta_data["nombre_plato"],
        ingredientes_json=json.dumps(receta_data["ingredientes"]),
        pasos_json=json.dumps(receta_data["pasos"]),
        tiempo_estimado=receta_data["tiempo_estimado"],
        dificultad=receta_data["dificultad"],
        usuario_id=current_user.id
    )
    db.add(receta)
    db.commit()
    db.refresh(receta)
    return receta

@router.get("/", response_model=list[RecetaOut])
def listar(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Receta).filter(Receta.usuario_id == current_user.id).all()

@router.delete("/{receta_id}")
def eliminar(receta_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    receta = db.query(Receta).filter(Receta.id == receta_id, Receta.usuario_id == current_user.id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    db.delete(receta)
    db.commit()
    return {"mensaje": "Receta eliminada"}

@router.post("/{receta_id}/calificar")
def calificar(receta_id: int, cal: CalificacionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not (1 <= cal.estrellas <= 5):
        raise HTTPException(status_code=400, detail="Las estrellas deben ser entre 1 y 5")
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    nueva_cal = Calificacion(estrellas=cal.estrellas, receta_id=receta_id, usuario_id=current_user.id)
    db.add(nueva_cal)
    db.commit()
    return {"mensaje": "Calificación guardada"}