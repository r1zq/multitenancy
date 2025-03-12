from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.models.tenant import Tenant

def switch_schema(tenant_id: int, db: Session = Depends(get_db)):
    """
    Global dependency to switch between tenant schemas.
    Usage: 
        @router.get("/endpoint")
        async def your_endpoint(db: Session = Depends(switch_schema)):
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    db.execute(text(f"SET search_path TO {tenant.schema}"))
    return db 