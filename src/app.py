from fastapi import FastAPI, HTTPException, Depends
import uvicorn 
import xgboost as xgb
import pandas as pd
import json
from datetime import datetime
# Import from another class
from labelStres import *

from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Pasien(BaseModel):
    name: str = Field(min_length=1)
    gsr: int = Field(gt=-1, lt=4)
    hr: int = Field(gt=-1, lt=4)
    bp: int = Field(gt=-1, lt=4)
    suhu: int = Field(gt=-1, lt=4)
    respirasi: int = Field(gt=-1, lt=3)
    tanggal_cek: Optional[datetime] = None 


PASIEN = []



# Load model 
model = xgb.XGBClassifier()
model.load_model("model.json")

@app.get("/")
def get_data_pasien(db: Session = Depends(get_db)):
    return db.query(models.Pasien).all()

@app.post("/")
def create_data_pasien(pasien: Pasien, db:Session = Depends(get_db)):
    pasien_model = models.Pasien()
    pasien_model.name = pasien.name
    pasien_model.gsr = pasien.gsr
    pasien_model.hr = pasien.hr
    pasien_model.bp = pasien.bp
    pasien_model.suhu = pasien.suhu
    pasien_model.respirasi = pasien.respirasi

    db.add(pasien_model)
    db.commit()
    return pasien

@app.put("/{pasien_id}")
def update_data_pasien(pasien_id: int, pasien: Pasien, db : Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.id == pasien_id).first()
    if pasien_model is None :
        raise HTTPException(
            status_code = 404,
            detail = f"ID {pasien_id} : Does not exist"
        )
    pasien_model.name = pasien.name
    pasien_model.gsr = pasien.gsr
    pasien_model.hr = pasien.hr
    pasien_model.bp = pasien.bp
    pasien_model.suhu = pasien.suhu
    pasien_model.respirasi = pasien.respirasi
    db.add(pasien_model)
    db.commit()
    return pasien

@app.delete("/{pasien_id}")
def delete_data_pasien(pasien_id: int, db: Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.id == pasien_id).first()
    
    if pasien_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Pasien with id : {pasien_id} : Does not exist"
        )
    
    db.query(models.Pasien).filter(models.Pasien.id == pasien_id).delete()
    db.commit()
    return f"Pasien with id : {pasien_id} deleted"



@app.get("/predict/{pasien_id}")
def predict(pasien_id: int, db: Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.id == pasien_id).first()
    
    if pasien_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Pasien with id : {pasien_id} : Does not exist"
        )
    
    data = {
        'GSR_label': [pasien_model.gsr],
        'HR_label': [pasien_model.hr],
        'BP_label': [pasien_model.bp],
        'SUHU_label': [pasien_model.suhu],
        'RESPIRASI_label': [pasien_model.respirasi],
    }
    df = pd.DataFrame(data)

    # data = {'GSR_label': [2,3,2,1,0,1], 'HR_label': [2,1,0,2,3,1], 'BP_label': [2,2,2,1,1,1], 'SUHU_label':[2,2,1,0,1,3], 'RESPIRASI_label':[2,0,0,1,1,1]}
    # # Create DataFrame.
    df = pd.DataFrame(data)
    result = model.predict(df)


    # all data in list
    gsr_list = data['GSR_label']
    hr_list = data['HR_label']
    bp_list = data['BP_label']
    suhu_list = data['SUHU_label']
    respirasi_list = data['RESPIRASI_label']
    result = result.tolist()

    # Change the label name
    gsr_list = ceklabelGSR(gsr_list)
    hr_list = ceklabelHR(hr_list)
    bp_list = ceklabelBP(bp_list)
    suhu_list = ceklabelSUHU(suhu_list)
    respirasi_list = ceklabelRESPIRASI(respirasi_list)
    result = ceklabelstres(result)

    list_dictionary = []
    
    for i in range(len(result)):
        rs = dict()
        rs['GSR_label'] = gsr_list[i]
        rs['HR_label'] = hr_list[i]
        rs['BP_label'] = bp_list[i]
        rs['SUHU_label'] = suhu_list[i]
        rs['RESPIRASI_label'] = respirasi_list[i]
        rs['RESULT_label'] = result[i]
        list_dictionary.append(rs) 
    # print(list_dictionary)
   

    return list_dictionary


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)