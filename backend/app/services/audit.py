from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.models.audit import AuditTrail


def log_audit(
    db: Session,
    user_id: Optional[int],
    action: str,
    resource_type: str,
    resource_id: Optional[int],
    description: Optional[str] = None,
    changes: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> AuditTrail:
    """
    Log an audit trail entry.

    Args:
        db: Database session
        user_id: User performing the action (None for system actions)
        action: Action performed (create, read, update, delete, etc.)
        resource_type: Type of resource (patient, user, clinical_note, etc.)
        resource_id: ID of the resource
        description: Human-readable description
        changes: Dictionary of changes (for updates)
        ip_address: Client IP address
        user_agent: Client user agent

    Returns:
        Created audit trail record
    """
    audit = AuditTrail(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        changes=changes,
        ip_address=ip_address,
        user_agent=user_agent
    )

    db.add(audit)
    db.commit()

    return audit
