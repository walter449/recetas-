from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    ingredientes = relationship("Ingrediente", back_populates="usuario")
    recetas = relationship("Receta", back_populates="usuario")

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    cantidad = Column(String(50))
    unidad = Column(String(30))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="ingredientes")

class Receta(Base):
    __tablename__ = "recetas"
    id = Column(Integer, primary_key=True, index=True)
    nombre_plato = Column(String(200), nullable=False)
    ingredientes_json = Column(Text)   # JSON string
    pasos_json = Column(Text)          # JSON string
    tiempo_estimado = Column(String(50))
    dificultad = Column(String(30))
    creada_en = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="recetas")
    calificaciones = relationship("Calificacion", back_populates="receta")

class Calificacion(Base):
    __tablename__ = "calificaciones"
    id = Column(Integer, primary_key=True, index=True)
    estrellas = Column(Integer, nullable=False)  # 1 a 5
    receta_id = Column(Integer, ForeignKey("recetas.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    receta = relationship("Receta", back_populates="calificaciones")