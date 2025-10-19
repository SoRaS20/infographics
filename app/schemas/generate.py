from typing import Dict, List, Optional
from pydantic import BaseModel

class ChartConfig(BaseModel):
    key: str
    chart_type: str  # "bar" or "line"
    x_col: str
    y_col: str
    title: Optional[str] = None

class GenerateRequest(BaseModel):
    template: str  # template name without .json
    images: Dict[str, int]  # key: asset_id
    data_asset_id: Optional[int] = None
    charts: List[ChartConfig] = []
    format: str = "png"  # "png" or "pdf"