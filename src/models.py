from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Pasien(Base):
    __tablename__ = "pasien"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    gsr = Column(Integer)
    hr = Column(Integer)
    bp = Column(Integer)
    suhu = Column(Integer)
    respirasi = Column(Integer)
    tanggal_cek = Column(DateTime, default=datetime.now)