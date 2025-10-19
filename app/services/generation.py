# import io
# import os
# import json
# import pandas as pd
# from PIL import Image, ImageDraw, ImageFont
# import matplotlib.pyplot as plt
# from img2pdf import convert
# from fastapi import HTTPException
# from typing import Dict

# from app.core.config import settings
# from app.crud.asset import get_asset
# from app.db.session import SessionLocal

# def load_template(template_name: str):
#     template_path = os.path.join("app/templates", f"{template_name}.json")
#     if not os.path.exists(template_path):
#         raise HTTPException(404, detail="Template not found")
#     with open(template_path, "r") as f:
#         return json.load(f)

# def load_data(asset_id: int):
#     db = SessionLocal()
#     try:
#         asset = get_asset(db, asset_id)
#         if not asset or asset.asset_type != "data":
#             raise HTTPException(404, detail="Data asset not found")
#         path = asset.path
#         if path.endswith(".csv"):
#             df = pd.read_csv(path)
#         elif path.endswith(".json"):
#             df = pd.read_json(path)
#         else:
#             raise HTTPException(400, detail="Unsupported data format")
#         return df, asset
#     finally:
#         db.close()  # Close the session after loading

# def generate_chart(df: pd.DataFrame, config):  # config is a Pydantic ChartConfig object
#     # Use a default figsize since position size is handled during pasting/resizing
#     default_width, default_height = 6, 4  # Inches; will be resized later
#     fig, ax = plt.subplots(figsize=(default_width, default_height))
#     if config.chart_type == "bar":
#         df.plot.bar(x=config.x_col, y=config.y_col, ax=ax)
#     elif config.chart_type == "line":
#         df.plot.line(x=config.x_col, y=config.y_col, ax=ax)
#     else:
#         raise ValueError("Unsupported chart type")
#     ax.set_title(getattr(config, 'title', '') or '')  # Safe access for optional title
#     buf = io.BytesIO()
#     fig.savefig(buf, format="png", bbox_inches="tight")
#     plt.close(fig)
#     buf.seek(0)
#     return Image.open(buf)

# def generate_infographic(template: Dict, images: Dict[str, int], data_asset_id: int | None, charts: list):
#     size = (template["size"]["width"], template["size"]["height"])
#     bg_color = tuple(int(template.get("background_color", "#FFFFFF")[i:i+2], 16) for i in (1,3,5))
#     infographic = Image.new("RGB", size, bg_color)
#     draw = ImageDraw.Draw(infographic)
#     font = ImageFont.load_default()  # Simple font; can customize

#     df = None
#     if data_asset_id:
#         df, _ = load_data(data_asset_id)

#     chart_images = {}
#     for chart_config in charts:
#         if df is None or df.empty:
#             raise HTTPException(400, detail="Data required for charts")
#         chart_img = generate_chart(df, chart_config)
#         chart_images[getattr(chart_config, 'key', f'chart_{len(chart_images)}')] = chart_img  # Use attribute or fallback

#     db = SessionLocal()
#     try:
#         for element in template["elements"]:
#             pos = element["position"]
#             box = (pos["x"], pos["y"], pos["x"] + pos.get("w", 0), pos["y"] + pos.get("h", 0))
#             if element["type"] == "image":
#                 asset_id = images.get(element["key"])
#                 if not asset_id:
#                     continue
#                 asset = get_asset(db, asset_id)
#                 if not asset or asset.asset_type != "image":
#                     raise HTTPException(404, detail=f"Image asset {element['key']} not found")
#                 img = Image.open(asset.path)
#                 img = img.resize((pos["w"], pos["h"]))
#                 infographic.paste(img, (pos["x"], pos["y"]))
#             elif element["type"] == "text":
#                 if df is None or df.empty:
#                     text = "Default Text"
#                 else:
#                     if element["key"] in df.columns and len(df) > 0:
#                         text = str(df[element["key"]].iloc[0])
#                     else:
#                         text = "N/A"
#                 color = tuple(int(element.get("color", "#000000")[i:i+2], 16) for i in (1,3,5))
#                 draw.text((pos["x"], pos["y"]), text, fill=color, font=font)
#             elif element["type"] == "chart":
#                 chart_img = chart_images.get(element["key"])
#                 if chart_img:
#                     chart_img = chart_img.resize((pos["w"], pos["h"]))
#                     infographic.paste(chart_img, (pos["x"], pos["y"]))
#     finally:
#         db.close()  # Ensure DB session closes

#     buf = io.BytesIO()
#     infographic.save(buf, format="PNG")
#     buf.seek(0)
#     return buf

# def to_pdf(png_buf: io.BytesIO):
#     pdf_buf = io.BytesIO()
#     pdf_buf.write(convert(png_buf.getvalue()))
#     pdf_buf.seek(0)
#     return pdf_buf


# import io
# import os
# import json
# import matplotlib
# matplotlib.use('Agg')  # Set non-interactive backend before importing pyplot
# import pandas as pd
# from PIL import Image, ImageDraw, ImageFont
# import matplotlib.pyplot as plt
# from img2pdf import convert
# from fastapi import HTTPException
# from typing import Dict

# from app.core.config import settings
# from app.crud.asset import get_asset
# from app.db.session import SessionLocal

# def load_template(template_name: str):
#     template_path = os.path.join("app/templates", f"{template_name}.json")
#     if not os.path.exists(template_path):
#         raise HTTPException(404, detail="Template not found")
#     with open(template_path, "r") as f:
#         return json.load(f)

# def load_data(asset_id: int):
#     db = SessionLocal()
#     try:
#         asset = get_asset(db, asset_id)
#         if not asset or asset.asset_type != "data":
#             raise HTTPException(404, detail="Data asset not found")
#         path = asset.path
#         if path.endswith(".csv"):
#             df = pd.read_csv(path)
#         elif path.endswith(".json"):
#             df = pd.read_json(path)
#         else:
#             raise HTTPException(400, detail="Unsupported data format")
#         return df, asset
#     finally:
#         db.close()  # Close the session after loading

# def generate_chart(df: pd.DataFrame, config):  # config is a Pydantic ChartConfig object
#     # Use a default figsize since position size is handled during pasting/resizing
#     default_width, default_height = 6, 4  # Inches; will be resized later
#     fig, ax = plt.subplots(figsize=(default_width, default_height))
#     if config.chart_type == "bar":
#         df.plot.bar(x=config.x_col, y=config.y_col, ax=ax)
#     elif config.chart_type == "line":
#         df.plot.line(x=config.x_col, y=config.y_col, ax=ax)
#     else:
#         raise ValueError("Unsupported chart type")
#     ax.set_title(getattr(config, 'title', '') or '')  # Safe access for optional title
#     buf = io.BytesIO()
#     fig.savefig(buf, format="png", bbox_inches="tight")
#     plt.close(fig)
#     buf.seek(0)
#     return Image.open(buf)

# def generate_infographic(template: Dict, images: Dict[str, int], data_asset_id: int | None, charts: list):
#     size = (template["size"]["width"], template["size"]["height"])
#     bg_color = tuple(int(template.get("background_color", "#FFFFFF")[i:i+2], 16) for i in (1,3,5))
#     infographic = Image.new("RGB", size, bg_color)
#     draw = ImageDraw.Draw(infographic)
#     font = ImageFont.load_default()  # Simple font; can customize

#     df = None
#     if data_asset_id:
#         df, _ = load_data(data_asset_id)

#     chart_images = {}
#     for chart_config in charts:
#         if df is None or df.empty:
#             raise HTTPException(400, detail="Data required for charts")
#         chart_img = generate_chart(df, chart_config)
#         chart_images[getattr(chart_config, 'key', f'chart_{len(chart_images)}')] = chart_img  # Use attribute or fallback

#     db = SessionLocal()
#     try:
#         for element in template["elements"]:
#             pos = element["position"]
#             box = (pos["x"], pos["y"], pos["x"] + pos.get("w", 0), pos["y"] + pos.get("h", 0))
#             if element["type"] == "image":
#                 asset_id = images.get(element["key"])
#                 if not asset_id:
#                     continue
#                 asset = get_asset(db, asset_id)
#                 if not asset or asset.asset_type != "image":
#                     raise HTTPException(404, detail=f"Image asset {element['key']} not found")
#                 img = Image.open(asset.path)
#                 img = img.resize((pos["w"], pos["h"]))
#                 infographic.paste(img, (pos["x"], pos["y"]))
#             elif element["type"] == "text":
#                 if df is None or df.empty:
#                     text = "Default Text"
#                 else:
#                     if element["key"] in df.columns and len(df) > 0:
#                         text = str(df[element["key"]].iloc[0])
#                     else:
#                         text = "N/A"
#                 color = tuple(int(element.get("color", "#000000")[i:i+2], 16) for i in (1,3,5))
#                 draw.text((pos["x"], pos["y"]), text, fill=color, font=font)
#             elif element["type"] == "chart":
#                 chart_img = chart_images.get(element["key"])
#                 if chart_img:
#                     chart_img = chart_img.resize((pos["w"], pos["h"]))
#                     infographic.paste(chart_img, (pos["x"], pos["y"]))
#     finally:
#         db.close()  # Ensure DB session closes

#     buf = io.BytesIO()
#     infographic.save(buf, format="PNG")
#     buf.seek(0)
#     return buf

# def to_pdf(png_buf: io.BytesIO):
#     pdf_buf = io.BytesIO()
#     pdf_buf.write(convert(png_buf.getvalue()))
#     pdf_buf.seek(0)
#     return pdf_buf


import io
import os
import json
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend before importing pyplot
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from img2pdf import convert
from fastapi import HTTPException
from typing import Dict

from app.core.config import settings
from app.crud.asset import get_asset
from app.db.session import SessionLocal

def load_template(template_name: str):
    template_path = os.path.join("app/templates", f"{template_name}.json")
    if not os.path.exists(template_path):
        raise HTTPException(404, detail="Template not found")
    with open(template_path, "r") as f:
        return json.load(f)

def load_data(asset_id: int):
    db = SessionLocal()
    try:
        asset = get_asset(db, asset_id)
        if not asset or asset.asset_type != "data":
            raise HTTPException(404, detail="Data asset not found")
        path = asset.path
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        elif path.endswith(".json"):
            df = pd.read_json(path)
        else:
            raise HTTPException(400, detail="Unsupported data format")
        return df, asset
    finally:
        db.close()  # Close the session after loading

def generate_chart(df: pd.DataFrame, config):  # config is a Pydantic ChartConfig object
    # Validate required columns exist
    if not df.empty and config.x_col in df.columns and config.y_col in df.columns:
        pass
    else:
        raise HTTPException(400, detail=f"Data missing required columns: '{config.x_col}' (x) or '{config.y_col}' (y). Available: {list(df.columns)}")
    
    # Use a default figsize since position size is handled during pasting/resizing
    default_width, default_height = 6, 4  # Inches; will be resized later
    fig, ax = plt.subplots(figsize=(default_width, default_height))
    if config.chart_type == "bar":
        df.plot.bar(x=config.x_col, y=config.y_col, ax=ax)
    elif config.chart_type == "line":
        df.plot.line(x=config.x_col, y=config.y_col, ax=ax)
    else:
        raise ValueError("Unsupported chart type")
    ax.set_title(getattr(config, 'title', '') or '')  # Safe access for optional title
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

def generate_infographic(template: Dict, images: Dict[str, int], data_asset_id: int | None, charts: list):
    size = (template["size"]["width"], template["size"]["height"])
    bg_color = tuple(int(template.get("background_color", "#FFFFFF")[i:i+2], 16) for i in (1,3,5))
    infographic = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(infographic)
    font = ImageFont.load_default()  # Simple font; can customize

    df = None
    if data_asset_id:
        df, _ = load_data(data_asset_id)

    chart_images = {}
    for chart_config in charts:
        if df is None or df.empty:
            raise HTTPException(400, detail="Data required for charts")
        chart_img = generate_chart(df, chart_config)
        chart_images[getattr(chart_config, 'key', f'chart_{len(chart_images)}')] = chart_img  # Use attribute or fallback

    db = SessionLocal()
    try:
        for element in template["elements"]:
            pos = element["position"]
            box = (pos["x"], pos["y"], pos["x"] + pos.get("w", 0), pos["y"] + pos.get("h", 0))
            if element["type"] == "image":
                asset_id = images.get(element["key"])
                if not asset_id:
                    continue
                asset = get_asset(db, asset_id)
                if not asset or asset.asset_type != "image":
                    raise HTTPException(404, detail=f"Image asset {element['key']} not found")
                img = Image.open(asset.path)
                img = img.resize((pos["w"], pos["h"]))
                infographic.paste(img, (pos["x"], pos["y"]))
            elif element["type"] == "text":
                if df is None or df.empty:
                    text = "Default Text"
                else:
                    if element["key"] in df.columns and len(df) > 0:
                        text = str(df[element["key"]].iloc[0])
                    else:
                        text = "N/A"
                color = tuple(int(element.get("color", "#000000")[i:i+2], 16) for i in (1,3,5))
                draw.text((pos["x"], pos["y"]), text, fill=color, font=font)
            elif element["type"] == "chart":
                chart_img = chart_images.get(element["key"])
                if chart_img:
                    chart_img = chart_img.resize((pos["w"], pos["h"]))
                    infographic.paste(chart_img, (pos["x"], pos["y"]))
    finally:
        db.close()  # Ensure DB session closes

    buf = io.BytesIO()
    infographic.save(buf, format="PNG")
    buf.seek(0)
    return buf

def to_pdf(png_buf: io.BytesIO):
    pdf_buf = io.BytesIO()
    pdf_buf.write(convert(png_buf.getvalue()))
    pdf_buf.seek(0)
    return pdf_buf