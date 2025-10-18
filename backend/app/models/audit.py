from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class AuditTrail(Base):
    """Audit trail for all system actions (HIPAA compliance)."""

    __tablename__ = "audit_trail"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)  # Nullable for system actions
    action = Column(String(100), nullable=False, index=True)  # e.g., "create", "read", "update", "delete"
    resource_type = Column(String(100), nullable=False, index=True)  # e.g., "patient", "clinical_note"
    resource_id = Column(Integer, nullable=True, index=True)
    description = Column(Text, nullable=True)
    changes = Column(JSON, nullable=True)  # Before/after values for updates
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional context
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditTrail(id={self.id}, action={self.action}, resource={self.resource_type}:{self.resource_id})>"
