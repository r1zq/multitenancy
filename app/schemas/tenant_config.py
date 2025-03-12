from pydantic import BaseModel
from typing import Dict, Optional

class TenantConfigBase(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    feature_flags: Dict[str, bool] = {}

class TenantConfigCreate(TenantConfigBase):
    pass

class TenantConfigUpdate(TenantConfigBase):
    pass

class TenantConfigInDB(TenantConfigBase):
    id: int

    # Enable ORM mode for Pydantic to work with SQLAlchemy models
    class Config:
        from_attributes = True  # newer version of orm_mode 