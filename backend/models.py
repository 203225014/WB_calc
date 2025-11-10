from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    calculations = relationship("Calculation", back_populates="owner")

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    purchase_price = Column(Float)
    desired_profit = Column(Float)
    length = Column(Float)
    width = Column(Float)
    height = Column(Float)
    commission_wb_percent = Column(Float)
    acquiring_percent = Column(Float)
    tax_percent = Column(Float)
    ads_percent = Column(Float)
    logistics_coefficient = Column(Float)
    return_cost = Column(Float)
    buyout_percent = Column(Float)
    storage_cost = Column(Float)
    # Результаты расчёта
    volume_liters = Column(Float)
    logistics_cost = Column(Float)
    total_logistics_cost = Column(Float)
    client_price = Column(Float)
    ads_cost = Column(Float)
    commission_wb_cost = Column(Float)
    acquiring_cost = Column(Float)
    tax_cost = Column(Float)
    storage_cost_result = Column(Float)
    final_cost = Column(Float)
    profit_per_unit = Column(Float)
    margin_percent = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="calculations")