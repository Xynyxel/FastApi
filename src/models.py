from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Pasien(Base):
    __tablename__ = "pasien"

    id_pasien = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    parent = relationship("Kriteria", back_populates="children")
    
    

class Kriteria(Base):
    __tablename__ = "kriteria"

    id_kriteria = Column(Integer, primary_key=True, index=True)
    gsr = Column(Integer)
    hr = Column(Integer)
    bp = Column(Integer)
    suhu = Column(Integer)
    respirasi = Column(Integer)
    tanggal_cek = Column(DateTime, default=datetime.now)
    tingkat_stress = Column(String)
    id_pasien = Column(Integer, ForeignKey("pasien.id_pasien"))

    child = relationship("Pasien", back_populates="parent")

    