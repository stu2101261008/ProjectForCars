from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.garage import Garage
from schemas.garage import GarageCreate, GarageUpdate, GarageResponse
from typing import List
from sqlalchemy import func
from schemas.garage import GarageFilter, GarageDailyReport, GarageReportRequest
from typing import List, Optional


router = APIRouter(
    prefix="/garages",
    tags=["Garages"]
)

# Функция за достъп до сесията на базата данни
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Създаване на гараж
@router.post("/", response_model=GarageResponse)
def create_garage(garage: GarageCreate, db: Session = Depends(get_db)):
    db_garage = Garage(**garage.dict())
    db.add(db_garage)
    db.commit()
    db.refresh(db_garage)
    return db_garage

# Извличане на всички гаражи
@router.get("/", response_model=List[GarageResponse])
def get_all_garages(db: Session = Depends(get_db)):
    return db.query(Garage).all()

# Извличане на гараж по ID
@router.get("/{garage_id}", response_model=GarageResponse)
def get_garage(garage_id: int, db: Session = Depends(get_db)):
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return garage

# Обновяване на гараж
@router.put("/{garage_id}", response_model=GarageResponse)
def update_garage(garage_id: int, garage: GarageUpdate, db: Session = Depends(get_db)):
    db_garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not db_garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    for key, value in garage.dict().items():
        setattr(db_garage, key, value)
    db.commit()
    db.refresh(db_garage)
    return db_garage

# Изтриване на гараж
@router.delete("/{garage_id}")
def delete_garage(garage_id: int, db: Session = Depends(get_db)):
    db_garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not db_garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    db.delete(db_garage)
    db.commit()
    return {"detail": "Garage deleted successfully"}

# Филтриране на сервизи по град
@router.get("/filter/", response_model=List[GarageResponse])
def get_garages_by_city(city: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Garage)
    if city:
        query = query.filter(Garage.city == city)
    return query.all()

from datetime import date

# Справка за сервиз по диапазон от дати
@router.post("/report/", response_model=List[GarageDailyReport])
def get_garage_report(report_request: GarageReportRequest, db: Session = Depends(get_db)):
    # Примерна симулация на заявки и капацитет (замести с реални заявки, ако има)
    report = []
    current_date = report_request.start_date
    while current_date <= report_request.end_date:
        requests_count = db.query(func.count()).filter(
            Garage.id == report_request.garage_id,
            func.date('2024-12-10') == current_date  # Заменете с реална таблица за заявки
        ).scalar() or 0
        
        garage = db.query(Garage).filter(Garage.id == report_request.garage_id).first()
        available_capacity = garage.capacity - requests_count if garage else 0
        
        report.append({
            "date": current_date,
            "requests": requests_count,
            "available_capacity": available_capacity
        })
        current_date += timedelta(days=1)
    
    return report