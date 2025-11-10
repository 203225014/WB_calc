# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime # Добавим импорт datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): # Добавляем этот класс
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class CalculationBase(BaseModel):
    purchase_price: float
    desired_profit: float
    length: float
    width: float
    height: float
    commission_wb_percent: float
    acquiring_percent: float
    tax_percent: float
    ads_percent: float
    logistics_coefficient: float
    return_cost: float
    buyout_percent: float
    storage_cost: float
    # Результаты
    volume_liters: float
    logistics_cost: float
    total_logistics_cost: float
    client_price: float
    ads_cost: float
    commission_wb_cost: float
    acquiring_cost: float
    tax_cost: float
    storage_cost_result: float
    final_cost: float
    profit_per_unit: float
    margin_percent: float

class CalculationCreate(CalculationBase):
    pass

class Calculation(CalculationBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True