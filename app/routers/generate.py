from fastapi import APIRouter, Depends, Response
from app.schemas.generate import GenerateRequest
from app.services.generation import load_template, generate_infographic, to_pdf
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/generate", tags=["generate"])

@router.post("/")
def generate(request: GenerateRequest, current_user: User = Depends(get_current_user)):
    template = load_template(request.template)
    png_buf = generate_infographic(template, request.images, request.data_asset_id, request.charts)
    
    if request.format == "pdf":
        pdf_buf = to_pdf(png_buf)
        return Response(content=pdf_buf.getvalue(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=infographic.pdf"})
    else:
        return Response(content=png_buf.getvalue(), media_type="image/png", headers={"Content-Disposition": "attachment; filename=infographic.png"})