import os
from fastapi import APIRouter

from app.schemas.template import Template

router = APIRouter(prefix="/templates", tags=["templates"])

@router.get("/", response_model=list[Template])
def list_templates():
    template_dir = "app/templates"
    templates = [Template(name=f.replace(".json", "")) for f in os.listdir(template_dir) if f.endswith(".json")]
    return templates