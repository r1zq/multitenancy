from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB
from app.core.dependencies import switch_schema

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def switch_schema(tenant_id: int, db: Session = Depends(get_db)):
#     from app.models.tenant import Tenant
#     tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
#     if not tenant:
#         raise HTTPException(status_code=404, detail="Tenant not found")
#     db.execute(f"SET search_path TO {tenant.schema}")
#     return db

@router.post("/tenants/{tenant_id}/users", response_model=UserInDB)
async def create_user(
    tenant_id: int,
    user: UserCreate,
    db: Session = Depends(switch_schema),
    token: str = Depends(oauth2_scheme)
):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/tenants/{tenant_id}/users/{user_id}", response_model=UserInDB)
async def read_user(
    tenant_id: int,
    user_id: int,
    db: Session = Depends(switch_schema),
    token: str = Depends(oauth2_scheme)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/tenants/{tenant_id}/users/{user_id}")
async def get_user(tenant_id: int, user_id: int, db: Session = Depends(switch_schema)):
    # The schema will be automatically switched
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 