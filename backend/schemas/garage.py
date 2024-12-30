from sqlite3 import Date
from pydantic import BaseModel
from typing import Optional

# Базова схема за гараж
class GarageBase(BaseModel):
    name: str
    location: str
    city: str
    capacity: int

# Схема за създаване на гараж
class GarageCreate(GarageBase):
    pass

# Схема за обновяване на гараж
class GarageUpdate(GarageBase):
    pass

# Схема за отговор (съдържа ID)
class GarageResponse(GarageBase):
    id: int

    class Config:
        from_attributes = True

# Филтър по град
class GarageFilter(BaseModel):
    city: Optional[str] = None

# Схема за дневна статистика на сервиз
class GarageDailyReport(BaseModel):
    date: Date
    requests: int
    available_capacity: int

# Схема за справка по сервиз и диапазон от дати
class GarageReportRequest(BaseModel):
    garage_id: int
    start_date: Date
    end_date: Date