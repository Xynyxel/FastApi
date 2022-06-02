from fastapi import FastAPI, HTTPException, Depends
import uvicorn 
import xgboost as xgb
import pandas as pd
import json

# Import from another class
from labelStres import *
from baseModel import *


import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


PASIEN = []
KRITERIA = []


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
    pasien_model.email = pasien.email
    pasien_model.password = pasien.password

    db.add(pasien_model)
    db.commit()
    return pasien

@app.put("/{pasien_id}")
def update_data_pasien(pasien_id: int, pasien: Pasien, db : Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.id_pasien == pasien_id).first()
    if pasien_model is None :
        raise HTTPException(
            status_code = 404,
            detail = f"Pasien ID {pasien_id} : Does not exist"
        )
    pasien_model = models.Pasien()
    pasien_model.name = pasien.name
    pasien_model.email = pasien.email
    pasien_model.password = pasien.password
    db.add(pasien_model)
    db.commit()
    return pasien

@app.delete("/{pasien_id}")
def delete_data_pasien(pasien_id: int, db: Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.id_pasien == pasien_id).first()
    
    if pasien_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Pasien with id : {pasien_id} : Does not exist"
        )
    
    db.query(models.Pasien).filter(models.Pasien.id == pasien_id).delete()
    db.commit()
    return f"Pasien with id : {pasien_id} deleted"

@app.get("/kriteria_pasien")
def get_data_kriteria_pasien(db: Session = Depends(get_db)):
    return db.query(models.Kriteria).all()

@app.post("/kriteria_pasien")
def create_data_kriteria_pasien(pasien_kriteria: Kriteria, db:Session = Depends(get_db)):
    pasien_kriteria_model = models.Kriteria()
    pasien_kriteria_model.gsr = pasien_kriteria.gsr
    pasien_kriteria_model.hr = pasien_kriteria.hr
    pasien_kriteria_model.bp = pasien_kriteria.bp
    pasien_kriteria_model.suhu = pasien_kriteria.suhu
    pasien_kriteria_model.respirasi = pasien_kriteria.respirasi
    pasien_kriteria_model.id_pasien = pasien_kriteria.id_pasien

    db.add(pasien_kriteria_model)
    db.commit()
    return pasien_kriteria_model

@app.put("/{kriteria_id}")
def update_data_kriteria_pasien(kriteria_id: int, pasien_kriteria: Kriteria, db : Session = Depends(get_db)):
    pasien_model = db.query(models.Kriteria).filter(models.Kriteria.id_kriteria == kriteria_id).first()
    if pasien_model is None :
        raise HTTPException(
            status_code = 404,
            detail = f"Kriteria ID {kriteria_id} : Does not exist"
        )
    pasien_kriteria_model = models.Kriteria()
    pasien_kriteria_model.gsr = pasien_kriteria.gsr
    pasien_kriteria_model.hr = pasien_kriteria.hr
    pasien_kriteria_model.bp = pasien_kriteria.bp
    pasien_kriteria_model.suhu = pasien_kriteria.suhu
    pasien_kriteria_model.respirasi = pasien_kriteria.respirasi
    pasien_kriteria_model.id_pasien = pasien_kriteria.id_pasien
    db.commit()
    return pasien_kriteria_model

@app.delete("/{kriteria_id}")
def delete_data_kriteria_pasien(kriteria_id: int, db: Session = Depends(get_db)):
    pasien_model = db.query(models.Kriteria).filter(models.Kriteria.id_kriteria == kriteria_id).first()
    
    if pasien_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Kriteria Pasien with id : {kriteria_id} : Does not exist"
        )
    
    db.query(models.Pasien).filter(models.Kriteria.id_kriteria == kriteria_id).delete()
    db.commit()
    return f"Kriteria Pasien with id : {kriteria_id} deleted"

# @app.post("/")
# def create_data_pasien(pasien: Pasien, db:Session = Depends(get_db)):
#     pasien_model = models.Pasien()
#     pasien_model.name = pasien.name
#     pasien_model.gsr = pasien.gsr
#     pasien_model.hr = pasien.hr
#     pasien_model.bp = pasien.bp
#     pasien_model.suhu = pasien.suhu
#     pasien_model.respirasi = pasien.respirasi

#     db.add(pasien_model)
#     db.commit()
#     return pasien

# @app.put("/{pasien_id}")
# def update_data_pasien(pasien_id: int, pasien: Pasien, db : Session = Depends(get_db)):
#     pasien_model = db.query(models.Pasien).filter(models.Pasien.id == pasien_id).first()
#     if pasien_model is None :
#         raise HTTPException(
#             status_code = 404,
#             detail = f"ID {pasien_id} : Does not exist"
#         )
#     pasien_model.name = pasien.name
#     pasien_model.gsr = pasien.gsr
#     pasien_model.hr = pasien.hr
#     pasien_model.bp = pasien.bp
#     pasien_model.suhu = pasien.suhu
#     pasien_model.respirasi = pasien.respirasi
#     db.add(pasien_model)
#     db.commit()
#     return pasien

# @app.delete("/{pasien_id}")
# def delete_data_pasien(pasien_id: int, db: Session = Depends(get_db)):
#     pasien_model = db.query(models.Pasien).filter(models.Pasien.id == pasien_id).first()
    
#     if pasien_model is None:
#         raise HTTPException(
#             status_code = 404,
#             detail = f"Pasien with id : {pasien_id} : Does not exist"
#         )
    
#     db.query(models.Pasien).filter(models.Pasien.id == pasien_id).delete()
#     db.commit()
#     return f"Pasien with id : {pasien_id} deleted"



# @app.get("/predict/{pasien_id}")
# def predict(pasien_id: int, db: Session = Depends(get_db)):
#     pasien_model = db.query(models.Pasien).filter(models.Pasien.id == pasien_id).first()
    
#     if pasien_model is None:
#         raise HTTPException(
#             status_code = 404,
#             detail = f"Pasien with id : {pasien_id} : Does not exist"
#         )
#     name = pasien_model.name
#     data = {
#         'GSR_label': [pasien_model.gsr],
#         'HR_label': [pasien_model.hr],
#         'BP_label': [pasien_model.bp],
#         'SUHU_label': [pasien_model.suhu],
#         'RESPIRASI_label': [pasien_model.respirasi],
#     }
#     df = pd.DataFrame(data)

#     # data = {'GSR_label': [2,3,2,1,0,1], 'HR_label': [2,1,0,2,3,1], 'BP_label': [2,2,2,1,1,1], 'SUHU_label':[2,2,1,0,1,3], 'RESPIRASI_label':[2,0,0,1,1,1]}
#     # # Create DataFrame.
#     df = pd.DataFrame(data)
#     result = model.predict(df)


#     # all data in list
#     gsr_list = data['GSR_label']
#     hr_list = data['HR_label']
#     bp_list = data['BP_label']
#     suhu_list = data['SUHU_label']
#     respirasi_list = data['RESPIRASI_label']
#     result = result.tolist()

#     # Change the label name
#     gsr_list = ceklabelGSR(gsr_list)
#     hr_list = ceklabelHR(hr_list)
#     bp_list = ceklabelBP(bp_list)
#     suhu_list = ceklabelSUHU(suhu_list)
#     respirasi_list = ceklabelRESPIRASI(respirasi_list)
#     result = ceklabelstres(result)

#     list_dictionary = []
    
#     for i in range(len(result)):
#         rs = dict()
#         rs['GSR_label'] = gsr_list[i]
#         rs['HR_label'] = hr_list[i]
#         rs['BP_label'] = bp_list[i]
#         rs['SUHU_label'] = suhu_list[i]
#         rs['RESPIRASI_label'] = respirasi_list[i]
#         rs['RESULT_label'] = result[i]
#         rs['Name'] = name
#         list_dictionary.append(rs) 
#     # print(list_dictionary)
   
#     return list_dictionary


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)