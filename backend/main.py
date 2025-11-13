from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import os

from . import crud, models, schemas, auth
from .database import SessionLocal, engine, get_db
from .config import settings
from .calculator import perform_calculation

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WB Unit Calculator API")

# ---------------------- CORS ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- FRONTEND STATIC ----------------------
FRONTEND_DIR = "/app/frontend/build"
FRONTEND_INDEX = os.path.join(FRONTEND_DIR, "index.html")

# Serve /static/* (JS, CSS)
if os.path.exists(FRONTEND_DIR):
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")),
        name="static"
    )


# ---------------------- AUTH ----------------------
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# ---------------------- CALCULATIONS ----------------------
@app.post("/calculate/", response_model=schemas.Calculation)
async def calculate(
    calculation: schemas.CalculationCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        result = perform_calculation(calculation)
        db_calculation = crud.create_calculation(
            db=db,
            calculation={**calculation.dict(), **result},
            user_id=current_user.id
        )
        return db_calculation

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Calculation error")


@app.get("/history/", response_model=list[schemas.Calculation])
async def get_calculation_history(
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_calculations(
        db, user_id=current_user.id, skip=skip, limit=limit
    )


@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@app.post("/calculations/", response_model=schemas.Calculation)
def create_calculation(
    calculation: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    result = perform_calculation(calculation)
    record = {**calculation.dict(), **result}
    return crud.create_calculation(db=db, calculation=record, user_id=current_user.id)


@app.get("/calculations/", response_model=list[schemas.Calculation])
def read_calculations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_calculations(db, skip=skip, limit=limit)


# ---------------------- HEALTH ----------------------
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# ---------------------- SPA FALLBACK (ДОЛЖЕН БЫТЬ ПОСЛЕДНИМ!) ----------------------
@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    """
    Serve React index.html for any non-API request.
    """
    if os.path.exists(FRONTEND_INDEX):
        return FileResponse(FRONTEND_INDEX)
    raise HTTPException(404, "Frontend not found")
