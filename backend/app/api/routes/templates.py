from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.core.security import get_current_active_user, require_role
from app.models.user import User
from app.models.template import Template, TemplateType

router = APIRouter()


@router.get("", response_model=List[dict])
async def list_templates(
    template_type: Optional[TemplateType] = None,
    is_active: bool = True,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List all available templates.

    Args:
        template_type: Optional filter by template type
        is_active: Filter by active status
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of templates
    """
    query = db.query(Template).filter(Template.is_active == is_active)

    if template_type:
        query = query.filter(Template.template_type == template_type)

    templates = query.all()

    return [{
        "id": t.id,
        "name": t.name,
        "template_type": t.template_type,
        "description": t.description,
        "structure_json": t.structure_json,
        "specialty": t.specialty,
        "version": t.version,
        "is_system": t.is_system,
        "created_at": t.created_at
    } for t in templates]


@router.get("/{template_id}", response_model=dict)
async def get_template(
    template_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get template by ID.

    Args:
        template_id: Template ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Template information

    Raises:
        HTTPException: If template not found
    """
    template = db.query(Template).filter(Template.id == template_id).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    return {
        "id": template.id,
        "name": template.name,
        "template_type": template.template_type,
        "description": template.description,
        "structure_json": template.structure_json,
        "specialty": template.specialty,
        "version": template.version,
        "is_system": template.is_system,
        "sections": [{
            "id": s.id,
            "section_name": s.section_name,
            "section_type": s.section_type,
            "description": s.description,
            "order": s.order,
            "required": s.required,
            "field_schema": s.field_schema,
            "ai_prompt": s.ai_prompt
        } for s in template.sections]
    }
