from sqlalchemy import (
create_engine, Column, Integer, String, Date, ForeignKey
)
from sqlalchemy.orm import relationship
from db_conector import Base  # Asegúrate que el archivo se llame exactamente db_conector.py

class Tabla(Base):
    __tablename__ = 'tabla'
    
    columna1 = Column(String(50), primary_key=True)
    columna2 = Column(Date, nullable=False)

    tablarelacion = relationship("tablalrelacion", back_populates='columnarelacion')

    def __repr__(self):
        return f"<columna1={self.columna1}, columna2={self.columna2}>"
