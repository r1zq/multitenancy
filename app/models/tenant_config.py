from sqlalchemy import Column, String, JSON, Integer
from app.db.base import Base

class TenantConfig(Base):
    __tablename__ = "tenant_config"
    
    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String, index=True)
    language = Column(String, index=True)
    feature_flags = Column(JSON, default={})