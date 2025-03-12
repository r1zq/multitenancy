from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.tenant_config import TenantConfig
from app.schemas.tenant_config import TenantConfigCreate, TenantConfigUpdate, TenantConfigInDB
from app.core.dependencies import switch_schema

router = APIRouter()

@router.get("/tenants/{tenant_id}/config", response_model=TenantConfigInDB)
async def get_tenant_config(tenant_id: int, db: Session = Depends(switch_schema)):
    # Set schema for multi-tenant isolation
    # db.execute(text(f"SET search_path TO tenant_{tenant_id}"))
    
    # Query using SQLAlchemy model
    config = db.query(TenantConfig).first()
    # config = db.execute(text("SELECT * FROM tenant_config")).fetchone()
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config

@router.put("/tenants/{tenant_id}/config", response_model=TenantConfigInDB)
async def update_tenant_config(
    tenant_id: int, 
    config: TenantConfigUpdate,
    db: Session = Depends(switch_schema)
):
    # Set schema for multi-tenant isolation
    db.execute(text(f"SET search_path TO tenant_{tenant_id}"))
    
    # Get existing config or create new one
    db_config = db.query(TenantConfig).first()
    if not db_config:
        db_config = TenantConfig()
        db.add(db_config)
    
    # Update fields from request
    for field, value in config.dict(exclude_unset=True).items():
        setattr(db_config, field, value)
    
    db.commit()
    db.refresh(db_config)
    return db_config