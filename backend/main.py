# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth
from .database import SessionLocal, engine, get_db
from .config import settings
from datetime import timedelta, datetime
from .calculator import perform_calculation
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

models.Base.metadata.create_all(bind=engine)


# Serve frontend static files (React build). Ensure Dockerfile copies frontend/build -> /app/frontend/build
app = FastAPI(title="WB Unit Calculator API")
# Serve frontend from final image path

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зависимость для получения сессии БД - УБРАЛИ отсюда, теперь в database.py

@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    """Serve React's index.html for any non-API GET request (SPA fallback).

    Tries the production build path (/app/frontend/build/index.html) first
    then falls back to the local frontend build relative path for local testing.
    """
    prod_index = "/app/frontend/build/index.html"
    if os.path.exists(prod_index):
        return FileResponse(prod_index, media_type="text/html")

    # Local dev path (when running backend locally and built frontend in repo)
    local_index = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "build", "index.html"))
    if os.path.exists(local_index):
        return FileResponse(local_index, media_type="text/html")

    # Nothing found — return 404 so API clients still get proper response
    raise HTTPException(status_code=404, detail="Frontend not found")
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): # Используем get_db из database
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/calculate/", response_model=schemas.Calculation)
async def calculate(
    calculation: schemas.CalculationCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Calculate unit economics and save results"""
    try:
        # Perform calculation
        result = perform_calculation(calculation)
        
        # Create calculation record
        db_calculation = crud.create_calculation(
            db=db,
            calculation={**calculation.dict(), **result},
            user_id=current_user.id
        )
        return db_calculation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Calculation error")

@app.get("/history/", response_model=list[schemas.Calculation])
async def get_calculation_history(
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's calculation history"""
    calculations = crud.get_user_calculations(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return calculations
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@app.post("/calculations/", response_model=schemas.Calculation)
def create_calculation(calculation: schemas.CalculationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    result = perform_calculation(calculation)
    # combine provided calculation and result fields for storage
    record = {**calculation.dict(), **result}
    return crud.create_calculation(db=db, calculation=record, user_id=current_user.id)


@app.get("/calculations/", response_model=list[schemas.Calculation])
def read_calculations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    calculations = crud.get_calculations(db, skip=skip, limit=limit)
    return calculations
