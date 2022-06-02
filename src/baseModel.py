from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Pasien(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class Kriteria(BaseModel):
    gsr: int = Field(gt=-1, lt=4)
    hr: int = Field(gt=-1, lt=4)
    bp: int = Field(gt=-1, lt=4)
    suhu: int = Field(gt=-1, lt=4)
    respirasi: int = Field(gt=-1, lt=3)
    tanggal_cek: Optional[datetime] = None 
    id_pasien: int = Field(default=None, foreign_key="pasien.id")

